/* appearance */
static const char font[]            = "fixed";
static const char normbordercolor[] = "#cccccc";
static const char normbgcolor[]     = "#cccccc";
static const char normfgcolor[]     = "#000000";
static const char selbordercolor[]  = "#0066ff";
static const char selbgcolor[]      = "#0066ff";
static const char selfgcolor[]      = "#000000";
static unsigned int borderpx        = 0;
static unsigned int snap            = 32;
static Bool showbar                 = False;
static Bool topbar                  = False;

/* tagging */
static const char *tags[] = { "web" };

static Rule rules[] = {
	{0}
};

/* layout(s) */
static float mfact      = 0.55;
static const int nmaster      = 1;    /* number of clients in master area */
static Bool resizehints = False; /* False means respect size hints in tiled resizals */

Layout layouts[] = {
	/* symbol		function */
	{ "[M]",		monocle },
};

/* key definitions */
#define MODKEY Mod1Mask
Key keys[] = { \
	/* modifier			key		function	argument */ \
	{ MODKEY|ShiftMask, XK_c,   killclient,     {0} },
	{ MODKEY,		    XK_q,   killclient,		{0} }, \
	{ MODKEY,		    XK_F4,  killclient,		{0} }, \
};

static Button buttons[] = {
	{0}
};
