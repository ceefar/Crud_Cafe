import pygame as pg
from settings import *
from random import choice
vec = pg.math.Vector2


# obvs want parent like Person or Character (basically just someone who can have a chatbox, well for now anyways me thinks)
class Customer(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.customers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- general stuff - will section better shortly --
        self.my_id = len(game.customers) # will start at 1
        self.game_state = "active"
        self.chatbox_state = "shelved" # opened or shelved
        self.my_name = choice(["James","Jim","John","Jack","Josh","Tim","Tom","Jonathon","Steve","Carl","Mike","Brian"])
        # add a display id - e.g KX139 or sumnt (have it be zones or sumnt but its slightly obscure so you dont twig it for a while, maybe like EWSN for cardinal directions)
        # -- chatbox specific vars --         
        self.shelved_chat_width = 200 
        self.shelved_chat_height = 50
        # -- initialising other empty instance vars --
        self.chatbox_shelved_destination_rect = False
        self.chatbox_opened_destination_rect = False

    def get_all_shelved_customers(self):
        """ returns the given instance if it is in a shelved state, else returns false """
        return self if self.chatbox_state == "shelved" else False

    def get_all_opened_customers(self):
        """ returns the given instance if it is in an opened state, else returns false """
        return self if self.chatbox_state == "opened" else False

    def draw_shelved_chatbox(self, index): 
        self.chat_box_surf = pg.Surface((self.shelved_chat_width, self.shelved_chat_height))
        if index % 2 == 0:
            self.chat_box_surf.fill(LIGHTGREY) # BLUEMIDNIGHT
        else:
            self.chat_box_surf.fill(DARKGREY) # SKYBLUE
        # -- draw the chatters name to the shelved chatbox surf --
        chatbox_title = self.game.FONT_VETERAN_TYPEWRITER_26.render(f"{self.my_name}", True, WHITE)
        self.chat_box_surf.blit(chatbox_title, (10, 10))
        # -- store its pos so we can move it in future -- 
        self.shelved_pos = (index * self.shelved_chat_width, 10)
        # -- draw this shelved chatbox to the bottom chatbar bg surface -- 
        self.chatbox_shelved_destination_rect = self.game.chat_bar_surf.blit(self.chat_box_surf, self.shelved_pos) # aligns to the bottom
        self.chatbox_shelved_destination_rect.move_ip(0, HEIGHT - self.game.chat_bar_surf.get_height()) # update the saved destination rect to its true position so we can use it for mouse checks
        
    def draw_open_chatbox(self, index, surf:pg.Surface): 
        # -- main open chatbox bg surf and dimensions --
        self.opened_chat_width = self.shelved_chat_width # fine for now, will wanna update when adding buttons and interactions to the open chat window tho
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
        # -- store its pos so we can move it in future -- 
        cascading_offset = 40 # when a new one is open initially its offset is the previous position (tho u need to cap this, then increase the y at a certain point tho dont reeeeally need to do that for a tech demo)
        self.open_position = (150 + (index * cascading_offset), 150 + (index * cascading_offset)) # cascading_offset ensures they arent drawn on top of each other initially
        # -- minimise button --
        minimise_btn_size = 20
        self.opened_chat_minimise_button_surf = pg.Surface((minimise_btn_size, minimise_btn_size))
        self.opened_chat_minimise_button_surf.fill(RED)
        self.opened_chat_minimise_button_rect = pg.Rect(self.opened_chat_width - minimise_btn_size - 5, 5, minimise_btn_size, minimise_btn_size)
        self.chat_box_surf.blit(self.opened_chat_minimise_button_surf, self.opened_chat_minimise_button_rect)
        self.true_minimise_button_rect = self.opened_chat_minimise_button_rect.copy()
        self.true_minimise_button_rect.move_ip(self.open_position)
        self.true_minimise_button_rect.move_ip(WIDTH - surf.get_width(), HEIGHT - surf.get_height())
        # -- final blit to the given (active) Tab surface --
        surf_copy = surf.copy()
        self.chatbox_opened_destination_rect = surf_copy.blit(self.chat_box_surf, self.open_position) 
        self.chatbox_opened_destination_rect.move_ip(WIDTH - surf.get_width(), HEIGHT - surf.get_height()) # is like 20, 20 or sumnt as the surf is the tab but obvs lets still do it and still do it dynamically anyway
        return surf_copy

    def check_click_shelved_chatbox(self):
        """ if the rect has been clicked we set this customers chatbot state to opened """
        if self.game.mouse_click_up:
            if self.chatbox_shelved_destination_rect:
                if self.chatbox_shelved_destination_rect.collidepoint(pg.mouse.get_pos()):
                    self.chatbox_state = "opened"
                    print(f"{self.my_name} => {self.chatbox_state}")
                    self.chatbox_shelved_destination_rect = False
                    self.game.all_shelved_chat_customers.remove(self)
                    return self

    def check_click_opened_chatbox(self):
        """ if the rect has been clicked we set this customers chatbot state to opened """
        if self.game.mouse_click_up:
            if self.chatbox_opened_destination_rect:
                if self.chatbox_opened_destination_rect.collidepoint(pg.mouse.get_pos()):
                    if self.true_minimise_button_rect.collidepoint(pg.mouse.get_pos()):
                        # -- this does shelving --
                        self.chatbox_state = "shelved"
                        print(f"{self.my_name} => {self.chatbox_state}")
                        self.chatbox_opened_destination_rect = False
                        self.game.all_open_chat_customers.remove(self)

                        # -- this does bring to front -- 
                        # self.game.all_open_chat_customers.remove(self)
                        # self.game.all_open_chat_customers.append(self)
                        
                        return self                    



# add button for minimise and add the shelving functionality to it
# - may require enumerating (else its like a customer self var) to get the order and blitting the top on that way (use on hover print with a \n to figure it out)
# then obvs add the bring to front functionality on click
# - try to get this working in some way specific to the layering as its weird rn? 
#   - say when you click if u click on more than one it just always takes the toppest one bosh)

# try get a lil bit of graphics in 🥺, see the inspo 

# then make and save to a public repo, and continue

# make the open chatboxes a better size with some additional light text (text box, image space, name, last reply or whatever, how long a customer for etc etc obvs just do quick now)
# then lets get like 2 or 3 super basic order buttons down and start getting an order together!
# - customer confirms it (just instantly after 2 seconds for now)
# - and then gets set to some new state
# - then obvs ill be doing some seperate order ting
# - for now tho id wanna go to maps tbf so start the mock up of that?
# - yh as imo what say 2 days to have a basic mockup understanding of the mvp basic flow
# - then just 5 days bosh that out 



class Browser_Tab(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.tabs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- positioning -- 
        top_bar_margin = 40 # hard code this to settings once sizes are configured
        self.x, self.y = 0, top_bar_margin
        self.pos = vec(self.x, self.y)
        self.width = WIDTH 
        self.height = HEIGHT
        # -- image and rect --
        self.blank_img_surf = pg.Surface((self.width, self.height - top_bar_margin))
        self.image = pg.Surface((self.width, self.height - top_bar_margin))
        self.image.fill(WHITE)
        self.blank_img_surf.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos # align to top right - for align to center use -> self.rect.centerx = self.rect.x + (self.width / 2) 
        # -- tab class variables --
        self.my_tab_name = self.set_tab_name()
        
    def set_tab_name(self):
        if isinstance(self, New_Orders_Tab):
            return "New Orders"
        else:
            return "Chats"

    def draw(self):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        title = self.game.FONT_VETERAN_TYPEWRITER_26.render(f"{self.my_tab_name}", True, BLUEMIDNIGHT) # FONT_VETERAN_TYPEWRITER_26 # FONT_BOHEMIAN_TYPEWRITER_26
        self.image.blit(title, (30,30))
        self.game.screen.blit(self.image, self.pos)


class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)
       

class Chats_Tab(Browser_Tab):
    def __init__(self, game): # < add anything specific to the child class here, and then underneath super().__init__()
        super().__init__(game)
       




# just make this like chat bar or sumnt idk
class Chatboxes(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites # game.chatboxes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- chatbox specific hardcoded state based values --
        max_shelved_chat_width = 200 # max width regardless of how many chats are shown, will be hard limiting the amount of chats shown here to swerve other issues
        self.shelved_chat_width = max_shelved_chat_width 
        self.shelved_chat_height = 50
        # -- true full chatbar values --
        self.height = 70
        self.width = WIDTH
        # -- positioning -- 
        self.x, self.y = 0, HEIGHT - self.height
        self.pos = vec(self.x, self.y)
        # -- image and rect -- 
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(TAN)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos # align to top right - for align to center use -> self.rect.centerx = self.rect.x + (self.width / 2) 
        
    def draw(self, current_chats:list[str]):
        for i, chatter in enumerate(current_chats):
            # -- create the shelved chatbox surface -- 
            chat_box_surf = pg.Surface((self.shelved_chat_width, self.shelved_chat_height))
            if i % 2 == 0:
                chat_box_surf.fill(BLUEMIDNIGHT)
            else:
                chat_box_surf.fill(SKYBLUE)
            # -- draw the chatters name to the shelved chatbox surf --
            chatbox_title = self.game.FONT_VETERAN_TYPEWRITER_26.render(f"{chatter}", True, WHITE)
            chat_box_surf.blit(chatbox_title, (10, 10))
            # -- draw this shelved chatbox to the screen -- 
            self.image.blit(chat_box_surf, (i * self.shelved_chat_width, self.height - self.shelved_chat_height)) # aligns to the bottom

        self.game.screen.blit(self.image, self.pos)            


# do need stuff like this tho, hmmm
# -- chatbox class variables --
# my_chatbox_name = "Person Name"
# my_chatbox_state = "shelved" # shelved/closed or open