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
        ...
        row_count = 3
        column_count = 5
        padding = 50 
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
                # title
                title = self.game.FONT_BOHEMIAN_TYPEWRITER_14.render(f"Item {col + ((row * 1) * column_count) + 1}.", True, WHITE)
                self.image.blit(title, (true_dest_rect.x + 5, true_dest_rect.y + 5)) 
                # button 
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
                # dest rect for mouse collision
                true_dest_rect.move_ip((WIDTH / 2) - (self.game.pc_screen_surf_width / 2), 150)
                # if true_dest_rect.collidepoint(pg.mouse.get_pos()):
                #     print(f"Collide! >> {true_dest_rect}")

        # so legit rnrn
        # save to repo
        # quickly bosh out side orders menu and click to button and then maybe with send to a customers chatbox
        # but can cut early after clicking adds to sidebar order
        # and go straight to refactor
        # which really wont be at all as long as you think
        # as we can keep a lot 
        # and literally all of the setup stuff
        # so just bosh it out!
        #   - for once save at a nice blank slate state

        # add the button
        # add the sidebar orders thing
        # have click button add to that order
        # have multi bottom button select different order i.e. 1 - 5 thing
        # have send order to selected / entered customer number and it shows up on their chatbox

        # i mean if u get all that done fairs
        # then its just the refactor tbh - actually hyped for it yanno as feels like it will be the final refactor for stucture
        # and i actually really like the fact that ive done it at the start of all 3 kick off days 
        # as its like actively ironing out the kinks while testing early
        # is better than rushing through have having to undo the tech debt, i really do get that now

        # for / if page x ...
        # for item in amount_cols
        # - for ... amount_rows
        # draw item name x info
        # draw item button



# -- Browser Tab Children --
class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)


class Chats_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)
       

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

    def draw_open_chatbox(self, surf:pg.Surface, index): 
        # -- main open chatbox bg surf and dimensions --
        self.opened_chat_width = 400
        self.opened_chat_height = 300 # will want this to be dynamic obvs but unsure as per the spec so just doing whatever and will refactor it all tomo
        self.chat_box_surf = pg.Surface((self.opened_chat_width, self.opened_chat_height))
        # -- alternate colours -- 
        if index % 2 == 0:
            self.chat_box_surf.fill(GREY) # GREY # DARKGREY
        else:
            self.chat_box_surf.fill(DARKGREY) # GREY # DARKGREY
        # -- draw the chatters name to the shelved chatbox surf --
        chatbox_title = self.game.FONT_VETERAN_TYPEWRITER_26.render(f"{self.my_name}", True, WHITE)
        self.chat_box_surf.blit(chatbox_title, (10, 10))
        # -- store the chatbox position --
        if self.chatbox_position == (50.0, 50.0): # is at the initial position, so cascade it if necessary
            cascading_offset = index * 50
            self.chatbox_position = (50 + cascading_offset, 50 + cascading_offset) # update the initial position to be slightly offset based on how many are on screen (should then also check at the start pos but like this is fine for now)
        else: # is at a moved position, so dont update it (for now anyways)
            pass
            # print(f"is at moved position => {self.chatbox_position}")
        # -- minimise button --
        minimise_btn_size = 20
        self.opened_chat_minimise_button_surf = pg.Surface((minimise_btn_size, minimise_btn_size))
        self.opened_chat_minimise_button_surf.fill(RED)
        self.opened_chat_minimise_button_rect = pg.Rect(self.opened_chat_width - minimise_btn_size - 10, 10, minimise_btn_size, minimise_btn_size)
        self.chat_box_surf.blit(self.opened_chat_minimise_button_surf, self.opened_chat_minimise_button_rect) # self.minimise_btn_destination_rect = 
        # -- final blit to the given (active) Tab surface --
        self.chatbox_destination_rect = surf.blit(self.chat_box_surf, self.chatbox_position) 
        # -- if its been selected highlight it, do this before the below destination rect move which adjusts for the surf (tab, i.e. computer screen) vs the display (i.e. camera pos) --
        if self.chatbox_move_activated: 
            pg.draw.rect(surf, GREEN, self.chatbox_destination_rect, 5)
        # -- final adjust for true rect -- 
        self.chatbox_destination_rect.move_ip(self.game.pc_screen_surf_x, self.game.pc_screen_surf_y + self.game.tab_bar_height)
    
    def __repr__(self):
        return f"Customer ID.{self.my_id} : {self.my_name}\n - at chatbox destination => {self.chatbox_destination_rect}"

    def update(self):
        # could add
        # - select the chatbox by clicking a small top bar rect (that will encapsulate the minimise btn) instead of anywhere (since there are other buttons to press too)        
        mouse = pg.mouse.get_pos()

        # if self.chatbox_destination_rect:
        #     if self.chatbox_destination_rect.collidepoint(pg.mouse.get_pos()):
        #         print(f"Hovered {self} - at mouse pos : {mouse}")
        #         self.chatbox_move_activated = True
        
        # ok this is improved but still not technically correct
        # - you basically just want
        # - if you have just put down a chatbox this frame, dont let the player pick up another one until next frame

        if self.game.mouse_click_up:       
            if self.chatbox_move_activated: # if you're already "holding" a chatbox window 
                self.chatbox_move_activated = False # put it down where you clicked
                self.game.is_player_moving_chatbox = False 
            else:   
                if self.chatbox_destination_rect:
                    if not self.game.is_player_moving_chatbox:
                        if self.chatbox_destination_rect.collidepoint(pg.mouse.get_pos()):
                            print(f"Clicked {self} - at mouse pos : {mouse}")
                            self.chatbox_move_activated = True  
                            self.game.is_player_moving_chatbox = True
                            return self    
        
        # if not self.chatbox_move_activated:
        #     self.game.is_player_moving_chatbox = False
            
        # so this will be the state dummy - and it should be updating each frame
        if self.chatbox_move_activated:
            self.chatbox_position = mouse[0] - self.game.pc_screen_surf_x, mouse[1] - self.game.pc_screen_surf_y - self.game.tab_bar_height
        return False
    




# minimise for like 10 mins
#   - considering that i think the problem was an order of operations thing
#   - try to resolve super quickly
#   - but no long ting, if it doesnt work off the bat pretty much
#   - then scrap it for now and continue 
# gamified elements - i.e. make an order and send to a customer (to appear on their chat window)
# could quickly do click to select and move via top bar as per update() note
# shelved and unshelved working flawlessly

# then cont omddddd
# - as in to *actual* gamification stuff D:


