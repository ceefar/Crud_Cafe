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
        self.draw_items()

    def wipe_surface(self):
        self.image.fill(WHITE)            

    def draw_to_pc(self):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.my_tab_name}", True, DARKGREY) 
        self.image.blit(title, (50,30))  
        self.game.pc_screen_surf.blit(self.image, (0, self.game.tab_bar_height)) # 50 is the top tabs area, need to hard code this once added it in 

    def draw_items(self):
        row_count, column_count, padding = 3, 5, 50 
        item_container_height = 50
        item_container_width = int((self.width - (padding * 2)) / row_count) - padding # this needs to be done better, isnt truly dynamic? 0 idk gotta check by running diff rows and cols duh
        for row in range(0, row_count):
            for col in range(0, column_count):
                # -- make dis a function --
                y_pos = 80 + (col * 50)
                x_pos = 50 + (row * 50)
                # 
                dest_rect = pg.Rect(x_pos + ((row * item_container_width)), y_pos + (col * 20), item_container_width, item_container_height)
                #
                true_dest_rect = pg.draw.rect(self.image, BLUEMIDNIGHT, dest_rect)
                # -- title --
                title = self.game.FONT_BOHEMIAN_TYPEWRITER_14.render(f"Item {col + ((row * 1) * column_count) + 1}.", True, WHITE)
                self.image.blit(title, (true_dest_rect.x + 5, true_dest_rect.y + 5)) 
                # -- button --
                btn_size = 20
                btn_x_padding = 10
                btn_y_padding = int((item_container_height - btn_size) / 2)
                btn_rect = pg.Rect(dest_rect.x + item_container_width - btn_size - btn_x_padding, dest_rect.y + btn_y_padding, btn_size, btn_size)
                true_btn_rect = pg.draw.rect(self.image, RED, btn_rect)
                true_btn_rect.move_ip(self.game.pc_screen_surf_x, self.game.pc_screen_surf_true_y) # adjust to the screen pos - yanno for refactor just make this a game function duh (or even settings!! << dis)                
                if true_btn_rect.collidepoint(pg.mouse.get_pos()):
                    pg.draw.rect(self.image, GREEN, btn_rect)
                    if self.game.mouse_click_up:
                        print(f"Click! >> {true_dest_rect}")
                # -- dest rect for mouse collision --
                true_dest_rect.move_ip((WIDTH / 2) - (self.game.pc_screen_surf_width / 2), 150)
         

# -- Browser Tab Children --
class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)


class Chats_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)
       

# -- Customer Initial First Test Implementation --
class Chatbox(pg.sprite.Sprite):
    layers_counter = 1
    chatbox_id_counter = 1

    def __init__(self, game):
        # -- init setup --
        self.groups = game.chatboxes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self._layer = Chatbox.layers_counter
        Chatbox.layers_counter += 1
        # -- general vars --
        self.my_id = Chatbox.chatbox_id_counter
        Chatbox.chatbox_id_counter += 1
        # -- open dimensions and surf setup --         
        self.open_width, self.open_height = 300, 300
        cascading_offset = self.my_id * 50
        self.image = pg.Surface((self.open_width, self.open_height))
        if self.my_id % 2 == 0:
            self.image.fill(LIGHTGREY)
        else:
            self.image.fill(DARKGREY)
        # -- position setup -- 
        self.pos = (50 + cascading_offset, 50 + cascading_offset)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos)
        self.x, self.y = self.rect.x, self.rect.y
        # -- state --
        self.chatbox_state = "opened" # inactive, opened, shelved (and maybe completed?)        
        # quick test
        self.chatbox_move_activated = False
        
    def __repr__(self):
        return f"Chatbox ID: {self.my_id}, layer: {self._layer}"

    def update(self):
        # figure it out for put down pick up
        # then straight onto order tings
        # - note just check old flow if you have to change things slightly (e.g. just for one seperate ting) its fine

                
        # print(f"{self} -> {self.rect} {self.x = } {self.y = }")
        print(f"{self.game.is_player_moving_chatbox = }")
        self.true_dest_rect = self.rect.copy()
        self.true_dest_rect.move_ip(self.open_width, self.open_height - 150)

        if self.game.mouse_click_up:
            if self.chatbox_move_activated:
                self.chatbox_move_activated = False
                self.game.is_player_moving_chatbox = False
            else:
                if not self.game.is_player_moving_chatbox:
                    if self.true_dest_rect.collidepoint(pg.mouse.get_pos()):
                        print(f"Clicked => {self}")
                        self.chatbox_move_activated = self  
                        self.game.is_player_moving_chatbox = self
                        # bring to front on click window by using change_layer
                        pg.sprite.LayeredUpdates.change_layer(self.game.chatbox_layers, self, Chatbox.chatbox_id_counter)
                        print(f"Updated Layer => {self._layer}")
                
        # if the item set to the selected (moving) chatbox instance is this instance, then update its rect position to the mouse position
        if self.game.is_player_moving_chatbox is self:
            print("Moving Self")
            mouse_pos = pg.mouse.get_pos()
            self.rect.x, self.rect.y = mouse_pos[0] - self.game.pc_screen_surf_x, mouse_pos[1] - self.game.pc_screen_surf_true_y
        
            # if self.game.mouse_click_up:
            #     print(f"Clicked While Holding {self.my_id}")
            #     self.game.is_player_moving_chatbox = False
      
                    

            
        # if hover print hover
        # if click print click
        # if click move layer to front
        # - colour them ALL seperately duh!
        # - blit the id too!



# -- Customer Initial First Test Implementation --
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
        self.chatbox_position = (50, 50) # initial position, tho this will (shortly) get updated if there is a window already there 
        self.chatbox_destination_rect = False
        self.chatbox_move_activated = False
        self.minimise_btn_destination_rect = False   
