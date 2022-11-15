# -- imports --
import pygame as pg
from random import choice, randint # uniform
from settings import *
vec = pg.math.Vector2


# -- Browser Tab Parent -- 
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
        # --
        self.is_active_tab = True if isinstance(self, New_Orders_Tab) else False # basically just true is active and false is hidden
    
    def __repr__(self):
        return f"Tab {self.my_tab_name} : is active? - {self.is_active_tab}"
                
    def set_tab_name(self):
        if isinstance(self, New_Orders_Tab):
            return "New Orders"
        else:
            return "Chats"

    def update(self):
        self.wipe_surface()

    def wipe_surface(self):
        self.image.fill(WHITE)            

    def draw_to_pc(self):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.my_tab_name}", True, DARKGREY) 
        self.image.blit(title, (50,30))  
        self.game.pc_screen_surf.blit(self.image, (0, 50)) # 50 is the top tabs area, need to hard code this once added it in 


# -- Browser Tab Children --
class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)


class Chats_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)
       



# -- NEW INITIAL FIRST TEST IMPLEMENTATION --
class Customer(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.customers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- general stuff - will section better shortly --
        self.my_id = len(game.customers) # will start at 1
        self.game_state = "active"
        self.chatbox_state = "opened" # opened or shelved
        self.my_name = choice(["James","Jim","John","Jack","Josh","Tim","Tom","Jonathon","Steve","Carl","Mike","Brian"])
        self.my_name += " " + choice(["A","B","C","D","E","F","G","H","I","J","K","L"]) # add a display id - e.g KX139 or sumnt (have it be zones or sumnt but its slightly obscure so you dont twig it for a while, maybe like EWSN for cardinal directions)
        # -- chatbox specific vars --         
        self.shelved_chat_width = 200 
        self.shelved_chat_height = 50
        
    def draw_open_chatbox(self, surf:pg.Surface): 
        # -- main open chatbox bg surf and dimensions --
        self.opened_chat_width = 400
        self.opened_chat_height = 300 # will want this to be dynamic obvs but unsure as per the spec so just doing whatever and will refactor it all tomo
        self.chat_box_surf = pg.Surface((self.opened_chat_width, self.opened_chat_height))
        # -- alternate colours -- 
        self.chat_box_surf.fill(GREY) # GREY # DARKGREY
        # -- draw the chatters name to the shelved chatbox surf --
        chatbox_title = self.game.FONT_VETERAN_TYPEWRITER_26.render(f"{self.my_name}", True, WHITE)
        self.chat_box_surf.blit(chatbox_title, (10, 10))
        # -- store the chatbox position --
        self.chatbox_position = (200, 200)
        # -- minimise button --
        minimise_btn_size = 20
        self.opened_chat_minimise_button_surf = pg.Surface((minimise_btn_size, minimise_btn_size))
        self.opened_chat_minimise_button_surf.fill(RED)
        self.opened_chat_minimise_button_rect = pg.Rect(self.opened_chat_width - minimise_btn_size - 5, 5, minimise_btn_size, minimise_btn_size)
        self.chat_box_surf.blit(self.opened_chat_minimise_button_surf, self.opened_chat_minimise_button_rect)
        self.true_minimise_button_rect = self.opened_chat_minimise_button_rect.copy()
        self.true_minimise_button_rect.move_ip(self.chatbox_position)
        self.true_minimise_button_rect.move_ip(WIDTH - surf.get_width(), HEIGHT - surf.get_height())
        # -- final blit to the given (active) Tab surface --
        surf.blit(self.chat_box_surf, self.chatbox_position) 

    # then in update set the position by click stuff
