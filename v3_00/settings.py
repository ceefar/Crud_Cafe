import pygame as pg
vec = pg.math.Vector2

# -- Colours (R, G, B) --
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
SILVER = (211, 211, 211)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
ORANGE = (255,100,10)
BLUEGREEN = (0,255,170)
MARROON = (115,0,0)
LIME = (180,255,100)
PRINT = (255,100,180)           # pink af  
PURPLE = (240,0,255)  
GREY = (127,127,127)
NICEGREY = (69,69,69)
MAGENTA = (255,0,230)
BROWN = (100,40,0)
FORESTGREEN = (0,50,0)
NAVYBLUE = (0,0,100)
RUST = (210,150,75)             # gold af
BRIGHTYELLOW = (255,200,0)
HIGHLIGHTER = (255,255,100)     # yellow af
SKYBLUE = (0,255,255)
MIDGREY = (128,128,128)     
COFFEE =(200,190,140)             
MOONGLOW = (235,245,255)        
BROWNTONE = (123,111,100)    
BROWNPALE =  (215,195,163)
BLUEMIDNIGHT = (0,51,102)
GOOGLEMAPSBLUE = (187,197,233)
DARKRED = (139,0,0)
PALEGREEN = (177, 237, 171)

# -- New Test Vars For Colour Shades -- 
# ideally write a function to do this dynamically
# - tan -
TAN = (230,220,170)       
TAN_DARKER_1 = (213,196,111)
TAN_ANALOGOUS_1 = (230,190,170)
TAN_ANALOGOUS_2 = (210,230,170) # - icky green, dont use, left to show kewl differences in colour patterns, good start point colours for creating a dynamic function to handle colour palette
TAN_COMPLIMENTARY_1 = (170,180,230)

# -- New Potentially Finalised Colour Palette Colours --
CUSTOMERTAN = (241,217,208)

# - not really finalised palette but is the current colour in the images for these post-its so using for now -
ORDERPOSTITBLUE = (32,41,149) 
# - test colour for payment window 
SUCCESSGREEN = (21,151,76)
# - test colour for default tab bg 
TABBLUE = (203,220,247)
# - test -
VLIGHTGREY = (234,234,234)

# -- General --
WIDTH = 1600 # 16:9  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 900 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Crud Cafe - Demo"
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# -- Scene x General Images --
SCENE_IMG = "crud_cafe_scene.png" 
SCENE_INFO_PINBOARD_IMG = "info_sidebar_concept_img.png" 
SCENE_PINBOARD_PAPER_IMG = "continous_paper_bg.png" 
SCENE_PINBOARD_ICON_1_IMG = "emoji_1.png"
SCENE_PINBOARD_ICON_2_IMG = "emoji_2.png"
SCENE_PINBOARD_ICON_3_IMG = "emoji_3.png"
SCENE_PINBOARD_ICON_4_IMG = "emoji_4.png"
SCENE_PINBOARD_ICON_5_IMG = "emoji_5.png"

# -- Faux OS Element Images --
WINDOW_IMG = "window_blank_img.png" 
WINDOW_BORDER_1_IMG = "window_blank_border_test_img.png" 
WINDOW_BORDER_HL_1_IMG = "window_blank_border_h1_1_img.png" 
WINDOW_BORDER_HL_2_IMG = "window_blank_border_h1_2_img.png" 
WINDOW_HL_1_IMG = "window_blank_highlight_1_img.png" 
WINDOW_HL_2_IMG = "window_blank_highlight_2_img.png" 
WINDOW_SHELVED_1_IMG = "window_blank_shelved_test_img.png" 
WINDOW_SHELVED_HL_1_IMG = "window_blank_shelved_test_hl_img.png" 

# -- More Faux OS Element Images - Windows --
PAYMENT_PENDING_IMG_1 = "payment_pending_blank_img_1.png" # PAYMENT_PENDING_IMG_1 = "payment_pending_test_img.png"
PAYMENT_SUCCESS_IMG_1 = "payment_pending_blank_success_img_1.png" 

# -- Tab Bar Faux OS Elements - Login -- 
START_LOGIN_IMG_1 = "login_screen_1.png"

# -- Tab Bar Faux OS Elements -- 
TAB_BAR_PREPARING_IMG = "tab_bar_prep_img.png"
TAB_BAR_ORDERING_IMG = "tab_bar_take_img.png"


# -- Map Test Images -- 
MAP_TEST_IMG_1 = "test_map_1.png" 
