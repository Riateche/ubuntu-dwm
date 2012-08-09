#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gtalk.py v0.10.3
# Google Talk mail notification client library
#
# Copyright (c) 2009-2010, Alexander Hungenberg <alexander.hungenberg@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from threading import Event

from twisted.words.protocols.jabber import xmlstream, client, jid
from twisted.words.xish import domish
from twisted.internet import reactor, task

_DEBUG = False
COLOR_GREEN = "\033[92m"
COLOR_END = "\033[0m"
def DEBUG(msg):
    if _DEBUG: print COLOR_GREEN + str(msg) + COLOR_END

class GTalkClientFactory(xmlstream.XmlStreamFactory):
    def __init__(self, jid, password):
        a = client.XMPPAuthenticator(jid, password)
        xmlstream.XmlStreamFactory.__init__(self, a)
        
        self.reconnect = True
    
    def clientConnectionLost(self, connector, reason):
        if self.reconnect: xmlstream.XmlStreamFactory.clientConnectionLost(self, connector, reason)

class MailChecker():
    def __init__(self, jid, password, labels=[], cb_new=None, cb_count=None):
        self.host = "talk.google.com"
        self.port = 5222
        self.jid = jid
        self.password = password
        self.cb_new = cb_new
        self.cb_count = cb_count
        self.cb_auth_successful = None
        self.cb_auth_failed = None
        
        self.last_tids = {}
        self.labels = labels
        self.labels_iter = iter(self.labels)
        self.count = {}
        self.mails = []
        
        # indicates whether we are in a state ready for complete interaction
        # (Authentication and Usersetting finished)
        # not disconnected, no query running
        self.ready_for_query_state = False
        self.timeout_call_id = None
        self.disconnected = True
    
    def die(self):
        self.factory.reconnect = False
        self.query_task.stop()
        self.connector.disconnect()
    
    def connect(self):
        self.factory = GTalkClientFactory(self.jid, self.password)
        self.factory.addBootstrap(xmlstream.STREAM_END_EVENT, self.disconnectCB)
        self.factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, self.disconnectCB)
        self.factory.addBootstrap(xmlstream.INIT_FAILED_EVENT, self.init_failedCB)
        self.factory.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.connectedCB)
        self.factory.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.authenticationCB)
        
        self.factory.reconnect = True
        
        self.query_task = task.LoopingCall(self.queryInbox)
        self.query_task.start(60)
        
        self.connector = reactor.connectTCP(self.host, self.port, self.factory)
    
    def reply_timeout(self):
        self.connector.disconnect() # Our reconnecting factory will try the reconnecting

    def send_callback_handler(self, data, callback=None, **kargs):
        self.timeout_call_id.cancel()
        if callback:
            callback(data, **kargs)
        else:
            DEBUG("got no callback in send_callback_handler")
            self.connector.disconnect()
    
    def send(self, data, event, callback, **kargs):
        """Emulates a ping like behaviour - adds a timeout for each response
        
        data: Data to be send - e.g. an IQ object (domish.Element)
        event: Event on which the callback should be called (e.g. "/iq")
        callback: callback that gets called when the event occurs
        """
        
        self.timeout_call_id = reactor.callLater(5, self.reply_timeout)
        self.xmlstream.addOnetimeObserver(event, self.send_callback_handler, callback=callback, **kargs)
        self.xmlstream.send(data)
    
    def disconnectCB(self, xmlstream):
        self.ready_for_query_state = False
        self.disconnected = True
        DEBUG("disconnected")
    
    def init_failedCB(self, xmlstream):
        if self.cb_auth_failed: self.cb_auth_failed()
        self.disconnectCB(xmlstream)
    
    def authenticationCB(self, xmlstream):
        if self.cb_auth_successful: self.cb_auth_successful()
        self.factory.resetDelay()
        
        # We set the usersetting mail-notification
        iq = domish.Element((None, "iq"), attribs={"type": "set", "id": "user-setting-3"})
        usersetting = iq.addElement(("google:setting", "usersetting"))
        mailnotifications = usersetting.addElement((None, "mailnotifications"))
        mailnotifications.attributes['value'] = "true"
        self.send(iq, "/iq", self.usersettingIQ)
    
    def usersettingIQ(self, iq):
        self.ready_for_query_state = True
        self.queryInbox()
    
    def queryInbox(self):
        if not self.ready_for_query_state: return
        if self.disconnected:
            self.connector.connect()
            return
        self.ready_for_query_state = False
        
        self.xmlstream.removeObserver("/iq", self.gotNewMail)
        
        iq = domish.Element((None, "iq"), attribs={"type": "get", "id": "mail-request-1"})
        query = iq.addElement(("google:mail:notify", "query"))
        self.send(iq, "/iq", self.gotLabel)
    
    def queryLabel(self):
        try:
            label = self.labels_iter.next()
            
            iq = domish.Element((None, "iq"), attribs={"type": "get", "id": "mail-request-1"})
            query = iq.addElement(("google:mail:notify", "query"))
            query.attributes['q'] = "label:%s AND is:unread" % label
            self.send(iq, "/iq", self.gotLabel, label=label)
        except StopIteration:
            self.labels_iter = iter(self.labels)
            self.xmlstream.addObserver("/iq", self.gotNewMail)
            if self.cb_count: self.cb_count(self.count)
            if self.mails and self.cb_new: self.cb_new(self.mails)
            self.mails = []
            self.ready_for_query_state = True
    
    def gotLabel(self, iq, label="inbox"):
        if iq.firstChildElement() and iq.firstChildElement().name == "mailbox":
            mailbox = iq.firstChildElement()
            if label in self.count and self.count[label] < int(mailbox.attributes['total-matched']):
                self.query_new_mail = True
            self.count[label] = int(mailbox.attributes['total-matched'])
            
            # Aggregating titles, summaries etc.
            threads = mailbox.children
            if threads:
                for thread in threads:
                    if not label in self.last_tids or thread['tid'] > self.last_tids[label]:
                        mail = {}
                        for child in thread.children:
                            if child.name == "senders":
                                for sender in child.children:
                                    if "address" in sender.attributes:
                                        mail['sender_address'] = unicode(sender.attributes['address'])
                                    if "name" in sender.attributes:
                                        mail['sender_name'] = unicode(sender.attributes['name'])
                            elif child.name == "labels":
                                mail['labels'] = unicode(child).split("|")
                            elif child.name == "subject":
                                mail['subject'] = unicode(child)
                            elif child.name == "snippet":
                                mail['snippet'] = unicode(child)
                        self.mails.append(mail)
                self.last_tids[label] = unicode(threads[0].attributes['tid'])
                
            self.queryLabel()
        else:
            DEBUG("ERROR: received unexpected iq after querying for INBOX")
            self.connector.disconnect()
    
    def gotNewMail(self, iq=None):
        if not iq or (iq.firstChildElement() and iq.firstChildElement().name == "new-mail"):
            self.xmlstream.removeObserver("/iq", self.gotNewMail)
            
            # Acknowledge iq
            if iq:
                iq = domish.Element((None, "iq"), attribs={"type": "result", "id": iq.attributes['id']})
                self.xmlstream.send(iq)
            
            # Get the new mail
            self.queryInbox()
        else:
            DEBUG("this was no new mail iq / ignoring it")
    
    def gotNewMailQueryResult(self, iq):
        if iq.firstChildElement() and iq.firstChildElement().name == "mailbox":
            mailbox = iq.children[0]
            threads = mailbox.children
            if threads:
                newest = threads[0]
                self.newest_tid = unicode(newest.attributes['tid'])
                
                mails = []
                
                for thread in threads:
                    mail = {}
                    for child in thread.children:
                        if child.name == "senders":
                            for sender in child.children:
                                if "address" in sender.attributes:
                                    mail['sender_address'] = unicode(sender.attributes['address'])
                                if "name" in sender.attributes:
                                    mail['sender_name'] = unicode(sender.attributes['name'])
                        elif child.name == "labels":
                            mail['labels'] = unicode(child).split("|")
                        elif child.name == "subject":
                            mail['subject'] = unicode(child)
                        elif child.name == "snippet":
                            mail['snippet'] = unicode(child)
                    mails.append(mail)
                
                self.cb_new(mails)
        
        self.ready_for_query_state = True
        if iq: self.queryInbox()
    
    def rawDataIn(self, buf):
        print u"< %s" % unicode(buf, "utf-8")
    
    def rawDataOut(self, buf):
        print u"> %s" % unicode(buf, "utf-8")
    
    def connectedCB(self, xmlstream):
        self.xmlstream = xmlstream
        self.disconnected = False
        
        if _DEBUG:
            xmlstream.rawDataInFn = self.rawDataIn
            xmlstream.rawDataOutFn = self.rawDataOut
