# -- imports --
import pygame as pg
from random import uniform
from settings import *
vec = pg.math.Vector2


# need to do a screen bg image first here but guna grab a munch quickly first 
# yh still try use this concept of tabs tho

# do the screen img bg stuff first
# - get it formatted decent and should be legit 2 variables to move its position without incident
# - make the game window bigger too btw

# then the old stuff reimplemented
# - with blitting to tab proper (will itself be blitting to the computer_screen - see [important-notes] in notes) 
#   - means browser tabs basically needs a full refactor so pretty much just do that, gut it and change as much as needed
# - with ordering ting
# - with the moveable windows ting

# big note
# - when doing customers add a nice repr (tbf everything duh!) 


class Browser_Tab(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.browser_tabs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- positioning -- 
        self.width, self.height = game.pc_screen_surf_width, game.pc_screen_surf_height - 50 # same size as the screen except the tabs bar height off the top (might do off the bottom for chat windows too tho btw - should also hard code both)
        self.x, self.y = 0, 0 # we're blitting to the pc screen surface so we dont need to worry about the position its already handled
        self.pos = vec(self.x, self.y)
        # -- image and rect --
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos # align to top right - for align to center use -> self.rect.centerx = self.rect.x + (self.width / 2) 
        # -- tab class variables --
        self.my_tab_name = self.set_tab_name()
    
    # def __repr__(self):
                
    def set_tab_name(self):
        if isinstance(self, New_Orders_Tab):
            return "New Orders"
        else:
            return "Chats"

    def update(self):
        self.wipe_surface()

    def wipe_surface(self):
        self.image.fill(WHITE)            

    def draw(self):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        title = self.game.FONT_VETERAN_TYPEWRITER_26.render(f"{self.my_tab_name}", True, BLUEMIDNIGHT) # FONT_VETERAN_TYPEWRITER_26 # FONT_BOHEMIAN_TYPEWRITER_26
        self.image.blit(title, (30,30))  
        rv = self.game.pc_screen_surf.blit(self.image, (0, 50)) # 50 is the top tabs area, need to hard code this once added it in 
        print(f"{rv = }")

class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)