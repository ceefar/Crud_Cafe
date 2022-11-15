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
       

# -- Customer Class --
# Big Note
# - do wanna do Person Parent and Customer, Manager, etc for Child classes, but just doing this for now to get the base implementation figured out 
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
        self.my_name += " " + choice(["A","B","C","D","E","F","G","H","I","J","K","L"])
        # add a display id - e.g KX139 or sumnt (have it be zones or sumnt but its slightly obscure so you dont twig it for a while, maybe like EWSN for cardinal directions)
        # -- chatbox specific vars --         
        self.shelved_chat_width = 200 
        self.shelved_chat_height = 50
        # -- initialising other empty instance vars --
        self.chatbox_shelved_destination_rect = False
        self.chatbox_opened_destination_rect = False
        # -- customer info --
        # - make this a dict once the basics are sorted 
        self.times_purchased = 0
        self.last_order = False
        self.total_spend = f"{randint(0,250)}:{randint(0,99)}" # is_loyalty_member
        self.display_location = "location"
        self.my_order = [{"item":"nuka cola", "quantity":2},{"item":"egg fried rice", "quantity":1}]
 
    def __repr__(self):
        return f"{self.my_id} : {self.my_name}"

        

    # its an older implementation sir, but it checks out
    def draw_open_chatbox(self, index, surf:pg.Surface, is_hovered=False): 
        # -- main open chatbox bg surf and dimensions --
        self.opened_chat_width = 400
        self.opened_chat_height = 300 # will want this to be dynamic obvs but unsure as per the spec so just doing whatever and will refactor it all tomo
        self.chat_box_surf = pg.Surface((self.opened_chat_width, self.opened_chat_height))
        # -- alternate colours -- 
        if index % 2 == 0:
            self.chat_box_surf.fill(DARKGREY)
        else:
            self.chat_box_surf.fill(GREY)
        # -- draw the chatters name to the shelved chatbox surf --
        chatbox_title = self.game.FONT_VETERAN_TYPEWRITER_26.render(f"{self.my_name}", True, WHITE)
        self.chat_box_surf.blit(chatbox_title, (10, 10))
        # -- some other general info text on the character -- 
        chatbox_customer_info = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"Spent: ${self.total_spend}, Location: {self.display_location}", True, WHITE)
        chatbox_customer_chat_text = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"I would like a {self.my_order[0]['item']}", True, WHITE)
        self.chat_box_surf.blit(chatbox_customer_info, (10, 40))
        self.chat_box_surf.blit(chatbox_customer_chat_text, (10, 70))
        # -- store its pos so we can move it in future -- 
        cascading_offset = 40 # when a new one is open initially its offset is the previous position (tho u need to cap this, then increase the y at a certain point tho dont reeeeally need to do that for a tech demo)
        self.open_position = (100 + (index * cascading_offset), 80 + (index * cascading_offset)) # cascading_offset ensures they arent drawn on top of each other initially
        # -- minimise button --
        minimise_btn_size = 20
        self.opened_chat_minimise_button_surf = pg.Surface((minimise_btn_size, minimise_btn_size))
        self.opened_chat_minimise_button_surf.fill(RED)
        self.opened_chat_minimise_button_rect = pg.Rect(self.opened_chat_width - minimise_btn_size - 5, 5, minimise_btn_size, minimise_btn_size)
        self.chat_box_surf.blit(self.opened_chat_minimise_button_surf, self.opened_chat_minimise_button_rect)
        self.true_minimise_button_rect = self.opened_chat_minimise_button_rect.copy()
        self.true_minimise_button_rect.move_ip(self.open_position)
        self.true_minimise_button_rect.move_ip(WIDTH - surf.get_width(), HEIGHT - surf.get_height())
        # self.true_minimise_button_rect.move_ip(self.game.pc_screen_surf_x - surf.get_width(), self.game.pc_screen_surf_y - surf.get_height())
        # -- final blit to the given (active) Tab surface --
        surf_copy = surf.copy()
        # if self.force_to_mouse_position:
            # self.open_position = pg.mouse.get_pos()
        self.chatbox_opened_destination_rect = surf_copy.blit(self.chat_box_surf, self.open_position) 
        if is_hovered:
            pg.draw.rect(surf_copy, RED, self.chatbox_opened_destination_rect, 5) 
        self.chatbox_opened_destination_rect.move_ip(surf.get_rect().x + self.game.pc_screen_surf_x, surf.get_rect().y + self.game.pc_screen_surf_y + 50) # the extra 50 here is the top tab group, again another reason to get this stuff finalised asap so can hard code these things
        # --
        return surf_copy        

    def check_click_opened_chatbox(self):
        """ if the rect has been clicked we set this customers chatbot state to opened """
        # if self.chatbox_opened_destination_rect:
        #     if self.chatbox_opened_destination_rect.collidepoint(pg.mouse.get_pos()):
        #         print(f"{self.my_name} : {self.chatbox_opened_destination_rect = }")
        if self.game.mouse_click_up:
            if self.chatbox_opened_destination_rect:
                if self.chatbox_opened_destination_rect.collidepoint(pg.mouse.get_pos()):
                    # if self.true_minimise_button_rect.collidepoint(pg.mouse.get_pos()):
                    #     # -- this does shelving --
                    #     self.chatbox_state = "shelved"                    
                    #     self.chatbox_opened_destination_rect = False
                    #     self.game.all_open_chat_customers.remove(self)
                    # else:
                    # -- this handles bringing clicked chatbox to front -- 
                    print(f"{self.game.all_open_chat_customers = }")
                    self.game.all_open_chat_customers.remove(self)
                    self.game.all_open_chat_customers.append(self)
                    print(f"{self.game.all_open_chat_customers = }")
                    print(f"")

                    # swear just need to reset this, or actually its happening in the loop so find out wassup
                    # maybe its just always resetting the order
                    # if so its just a simple dont set if set
                    # self.chatbox_opened_destination_rect = # open_position = (100 + (index * cascading_offset), 80 + (index * cascading_offset))
                    
                    # --
                    return self        