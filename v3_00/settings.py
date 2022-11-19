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
TAN = (230,220,170)            
COFFEE =(200,190,140)             
MOONGLOW = (235,245,255)        
BROWNTONE = (123, 111, 100)    
BROWNPALE =  (215, 195, 163)
BLUEMIDNIGHT = (0, 51, 102)
GOOGLEMAPSBLUE = (187,197,233)

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

# -- Faux OS Element Images --
WINDOW_IMG = "window_blank_img.png" 
WINDOW_HL_1_IMG = "window_blank_highlight_1_img.png" 
WINDOW_HL_2_IMG = "window_blank_highlight_2_img.png" 
WINDOW_SHELVED_1_IMG = "window_blank_shelved_test_img.png" 
WINDOW_SHELVED_HL_1_IMG = "window_blank_shelved_test_hl_img.png" 
