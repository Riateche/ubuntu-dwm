/* See LICENSE file for copyright and license details. */

/* appearance */
static const char font[]            = "-*-*-medium-*-*-*-14-*-*-*-*-*-iso10646-*"; // this font supports unicode
static const char normbordercolor[] = "#444444";
static const char normbgcolor[]     = "#222222";
static const char normfgcolor[]     = "#bbbbbb";
static const char selbordercolor[]  = "#00ff00";
static const char selbgcolor[]      = "#001000";
static const char selfgcolor[]      = "#eeeeee";
static const unsigned int borderpx  = 4;        /* border pixel of windows */
static const unsigned int snap      = 32;       /* snap pixel */
static const Bool showbar           = True;     /* False means no bar */
static const Bool topbar            = True;     /* False means bottom bar */

/* tagging */
#define MAX_TAGLEN 16
static char tags[][MAX_TAGLEN] = { "1", "2", "3", "4", "5", "6", "7", "8", "9" };

static const Rule rules[] = {
  /* class      instance    title       tags mask     isfloating   monitor */
  { "Pidgin",     NULL,       NULL,       1 << 3,     False,       -1 },
  { "stalonetray",NULL,       NULL,       1 << 8,     False,       -1 },
//  { "Firefox",  NULL,       NULL,       1 << 8,       False,       -1 },
};

/* layout(s) */
static const float mfact      = 0.55; /* factor of master area size [0.05..0.95] */
static const int nmaster      = 1;    /* number of clients in master area */
static const Bool resizehints = True; /* True means respect size hints in tiled resizals */

static const Layout layouts[] = {
  /* symbol     arrange function */
  { "[T]",      tile },    /* first entry is default */
  { "[F]",      NULL },    /* no layout function means floating behavior */
  { "[M]",      monocle },
};

/* key definitions */
#define MODKEY Mod4Mask
#define TAGKEYS(KEY,TAG) \
  { MODKEY,                       KEY,       view,           {.ui = 1 << TAG} }, \
  { MODKEY|ControlMask,           KEY,       toggleview,     {.ui = 1 << TAG} }, \
  { Mod1Mask|MODKEY,              KEY,       tag,            {.ui = 1 << TAG} }, \
  { Mod1Mask|MODKEY|ControlMask,  KEY,       toggletag,      {.ui = 1 << TAG} },

/* helper for spawning shell commands in the pre dwm-5.0 fashion */
#define SHCMD(cmd) { .v = (const char*[]){ "/bin/sh", "-c", cmd, NULL } }

/* commands */
static const char *dmenucmd[] = { "dmenu_run", "-fn", font, "-nb", normbgcolor, "-nf", normfgcolor, "-sb", selbgcolor, "-sf", selfgcolor, NULL };
static const char *termcmd[]  = { "x-terminal-emulator", NULL };

static Key keys[] = {
  /* modifier                     key        function        argument */
//{ MODKEY,                       XK_p,      spawn,          {.v = dmenucmd } },
//{ Mod1Mask,                     XK_F2,     spawn,          {.v = dmenucmd } },
//{ MODKEY|ShiftMask,             XK_Return, spawn,          {.v = termcmd } },
  { MODKEY,                       XK_b,      togglebar,      {0} },
  { MODKEY,                       XK_Down,   focusstack,     {.i = +1 } },
  { MODKEY,                       XK_Up,     focusstack,     {.i = -1 } },
  // count of windows in master area
  { MODKEY,                       XK_i,      incnmaster,     {.i = +1 } }, 
  { MODKEY,                       XK_k,      incnmaster,     {.i = -1 } }, 

  //size of master area
  { MODKEY,                       XK_Left,   setmfact,       {.f = -0.05} },
  { MODKEY,                       XK_Right,  setmfact,       {.f = +0.05} },
  
  //send window to master area
  { MODKEY,                       XK_Return, zoom,           {0} }, 
//{ MODKEY,                       XK_Tab,    view,           {0} },
  { MODKEY,                       XK_Escape, killclient,     {0} },

  { MODKEY,                       XK_t,      setlayout,      {.v = &layouts[0]} },
  { MODKEY,                       XK_f,      setlayout,      {.v = &layouts[1]} },
  { MODKEY,                       XK_m,      setlayout,      {.v = &layouts[2]} },
//{ MODKEY,                       XK_space,  setlayout,      {0} },
  { MODKEY,                       XK_space,  togglefloating, {0} },
  { MODKEY,                       XK_0,      view,           {.ui = ~0 } },
  { MODKEY|ShiftMask,             XK_0,      tag,            {.ui = ~0 } },
  { MODKEY,                       XK_Page_Up,    focusmon,   {.i = -1 } },
  { MODKEY,                       XK_Page_Down,  focusmon,   {.i = +1 } },
  { MODKEY|Mod1Mask,              XK_Page_Up,    tagmon,     {.i = -1 } },
  { MODKEY|Mod1Mask,              XK_Page_Down,  tagmon,     {.i = +1 } },
  
  //nametag patch
  { MODKEY,                       XK_F2,     nametag,        {0} },

  //moveresize patch
  { MODKEY|Mod1Mask,              XK_Down,   moveresize,     {.v = (int []){ 0, 25, 0, 0 }}},
  { MODKEY|Mod1Mask,              XK_Up,     moveresize,     {.v = (int []){ 0, -25, 0, 0 }}},
  { MODKEY|Mod1Mask,              XK_Right,  moveresize,     {.v = (int []){ 25, 0, 0, 0 }}},
  { MODKEY|Mod1Mask,              XK_Left,   moveresize,     {.v = (int []){ -25, 0, 0, 0 }}},
  { MODKEY|ShiftMask,             XK_Down,   moveresize,     {.v = (int []){ 0, 0, 0, 25 }}},
  { MODKEY|ShiftMask,             XK_Up,     moveresize,     {.v = (int []){ 0, 0, 0, -25 }}},
  { MODKEY|ShiftMask,             XK_Right,  moveresize,     {.v = (int []){ 0, 0, 25, 0 }}},
  { MODKEY|ShiftMask,             XK_Left,   moveresize,     {.v = (int []){ 0, 0, -25, 0 }}},


  TAGKEYS(                        XK_q,                      0)
  TAGKEYS(                        XK_w,                      1)
  TAGKEYS(                        XK_e,                      2)
  TAGKEYS(                        XK_a,                      3)
  TAGKEYS(                        XK_s,                      4)
  TAGKEYS(                        XK_d,                      5)
  TAGKEYS(                        XK_z,                      6)
  TAGKEYS(                        XK_x,                      7)
  TAGKEYS(                        XK_c,                      8)
  { MODKEY|ShiftMask,             XK_q,      quit,           {0} }, //restart
};

/* button definitions */
/* click can be ClkLtSymbol, ClkStatusText, ClkWinTitle, ClkClientWin, or ClkRootWin */
static Button buttons[] = {
  /* click                event mask      button          function        argument */
  { ClkLtSymbol,          0,              Button1,        setlayout,      {0} },
  { ClkLtSymbol,          0,              Button3,        setlayout,      {.v = &layouts[2]} },
  { ClkWinTitle,          0,              Button2,        zoom,           {0} },
  { ClkStatusText,        0,              Button2,        spawn,          {.v = termcmd } },
  { ClkClientWin,         MODKEY,         Button1,        movemouse,      {0} },
  { ClkClientWin,         MODKEY,         Button2,        togglefloating, {0} },
  { ClkClientWin,         MODKEY,         Button3,        resizemouse,    {0} },
  { ClkTagBar,            0,              Button1,        view,           {0} },
  { ClkTagBar,            0,              Button3,        toggleview,     {0} },
  { ClkTagBar,            MODKEY,         Button1,        tag,            {0} },
  { ClkTagBar,            MODKEY,         Button3,        toggletag,      {0} },
};



