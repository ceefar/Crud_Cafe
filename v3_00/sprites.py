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
        self.width, self.height = game.pc_screen_surf_width, game.pc_screen_surf_height - self.game.tab_bar_height # same size as the screen except the tabs bar height off the top (might do off the bottom for chat windows too tho btw - should also hard code both)
        self.x, self.y = 0, 0 # we're blitting to the pc screen surface so we dont need to worry about the position its already handled
        self.pos = vec(self.x, self.y)
        # -- image and rect --
        self.image = pg.Surface((self.width, self.height))
        
        self.set_bg_colour()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos # align to top right - for align to center use -> self.rect.centerx = self.rect.x + (self.width / 2) 
        # -- tab class variables --
        self.my_tab_name = self.get_tab_name()
        # --
        self.is_active_tab = True if isinstance(self, New_Orders_Tab) else False # basically just true is active and false is hidden
    
    def __repr__(self):
        return f"Tab {self.my_tab_name}"
                
    def get_tab_name(self):
        if isinstance(self, New_Orders_Tab):
            return "New Orders"
        else:
            return "Chats"
                
    def set_bg_colour(self):
        if isinstance(self, New_Orders_Tab):
            self.image.fill(WHITE)
        else:
            self.image.fill(TAN)

    def update(self):
        self.wipe_surface()

    def wipe_surface(self):
        self.set_bg_colour()    

    def draw_tab_to_pc(self):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.my_tab_name} {len(self.game.all_active_customers)}", True, DARKGREY) 
        self.image.blit(title, (50,30))  
        self.game.pc_screen_surf.blit(self.image, (0, self.game.tab_bar_height)) # 50 is the top tabs area, need to hard code this once added it in 


# -- Browser Tab Children --
class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)


class Chats_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)
       

# ---- End Browser Tabs ----


# -- Customer Initial First Test Implementation --
class Customer(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.customers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- general stuff - should section better tho --
        self.my_id = len(game.customers) # will start at 1
        self.customer_state = "inactive" # active or completed or cancelled
        self.chatbox_state = "opened" # opened or shelved, have them start shelved - only relevant when customer is active (for now anyways) 
        self.my_name = choice(["James","Jim","John","Jack","Josh","Tim","Tom","Jonathon","Steve","Carl","Mike","Brian"])
        self.my_name += " " + choice(["A","B","C","D","E","F","G","H","I","J","K","L"]) # add a display id - e.g KX139 or sumnt (have it be zones or sumnt but its slightly obscure so you dont twig it for a while, maybe like EWSN for cardinal directions)
 
    def __repr__(self):
        return f"Customer ID.{self.my_id} : {self.my_name}"


# -- Customer Initial First Test Implementation --
class Chatbox(pg.sprite.Sprite):
    layers_counter = 1

    def __init__(self, game, associated_customer:Customer):
        # -- init setup --
        self.groups = game.chatboxes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.my_customer = associated_customer
        self._layer = Chatbox.layers_counter
        Chatbox.layers_counter += 1
        # -- id --
        self.my_id = self.my_customer.my_id # this is the best way 100
        # -- open and shelved dimensions --         
        self.opened_chat_width = 300 
        self.opened_chat_height = 250
        self.shelved_chat_width = 200 
        self.shelved_chat_height = 50
        # -- initial default positions --
        self.opened_pos = vec(50, 100)
        # -- image surf setup --         
        self.image = pg.Surface((self.opened_chat_width, self.opened_chat_height)) # starting shelved but we need sumnt to handle this toggle too
        self.my_bg_colour = LIGHTGREY if self.my_id % 2 == 0 else DARKGREY
        self.image.fill(self.my_bg_colour)
        # -- set positions -- 
        initial_pos = (-500, -500) # initial position offscreen
        self.rect = self.image.get_rect()
        self.rect.move_ip(initial_pos)
        self.x, self.y = self.rect.x, self.rect.y
        # -- test flags --
        self.is_at_offscreen_position = True # always starts at the initial position when drawn (in reference to when drawn on screen not off screen at runtime)
        # -- chatbox states --
        # self.chatbox_state = "opened" # inactive, opened, shelved (and maybe completed?)        
        # self.chatbox_move_activated = False
        # self.chatbox_is_hovered = False # test tho

    # ---- End Init ----
        
    # -- Draw, Update, & Repr --

    def update(self):
        if self.my_customer.customer_state == "active":

            if self.game.mouse_click_up: # if there was a click this frame check to see if it collided with the chatbox rect (temp - will do new top title bar in a sec)
                self.true_chatbox_window_rect = self.get_true_rect(self.rect)
                if self.true_chatbox_window_rect.collidepoint(pg.mouse.get_pos()): # if mouse collided with this chatboxs rect
                    print(f"Updating {self} = > {Chatbox.layers_counter = }\n") #  {self.my_customer}
                    pg.sprite.LayeredUpdates.change_layer(self.game.chatbox_layers, self, Chatbox.layers_counter) 
                    print(f"New Layer = {self}\n")
                    for a_chatbox in self.game.chatboxes:
                        print(f"All Layers = {a_chatbox}")
                    print(f"")
                    # self.reorder_all_window_layers(self)  
                    
            if self.my_customer.chatbox_state == "opened":
                if self.is_at_offscreen_position:
                    self.set_opened_chatbox_initial_position()
                    self.game.opened_chatbox_offset_counter += 1
                    self.wipe_image()
                    self.draw_name_to_chatbox()
    
    def __repr__(self):
        return f"Chatbox ID: {self.my_id}, layer: {self._layer}"

    # -- Blitting To This Chatbox Image Functs --
    def wipe_image(self):
        """ run this each frame before drawing anything to our image - runs in update but we draw to this image in update then draw this actual image to the screen in draw, by self._layer """
        self.image.fill(self.my_bg_colour)

    def draw_name_to_chatbox(self): # chat this to draw text to chatbox btw!
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.my_customer.my_name} - Layer: {self._layer}", True, WHITE) 
        self.image.blit(title, (90, 20))  

    # -- Repositioning Functs --
    def set_opened_chatbox_initial_position(self):
        opened_chatboxes_offset = 50 * self.game.opened_chatbox_offset_counter # do need to check the positions tho remember (maybe do this before and not in loop) - skipping for like 2 mins tho
        self.x, self.y = self.opened_pos.x + opened_chatboxes_offset, self.opened_pos.y + opened_chatboxes_offset
        self.rect.x, self.rect.y = self.x, self.y

    def get_true_rect(self, a_rect:pg.Rect):
        """ update a given rect position by offsetting it from the pc_screen x and y pos """
        moved_rect = a_rect.copy()
        moved_rect.move_ip(self.game.pc_screen_surf_x, self.game.pc_screen_surf_true_y)
        return moved_rect
        
        

# in update()
# - handle toggle opened or shelved, handle inactive and completed too now tho! - should be simply tbf just check if opened or shelved or only send opened or shelved
#       - maybe best as sumnt like update_active_chatbox, could then even run that in update if .state == active  