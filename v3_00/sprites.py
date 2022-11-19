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
        # -- general tab variables --
        self.my_tab_name = self.get_tab_name()
        # -- tab state --
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
            self.image.fill(GOOGLEMAPSBLUE)

    def update(self):
        self.wipe_surface()

    def wipe_surface(self):
        self.set_bg_colour()    

    def draw_tab_to_pc(self):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.my_tab_name} {len(self.game.all_active_customers)}", True, DARKGREY) 
        self.image.blit(title, (50,30))  
        self.game.pc_screen_surf.blit(self.image, (0, self.game.tab_bar_height)) # 50 is the top tabs area, need to hard code this once added it in 

    def draw_text_to_surf(self, text:str, pos:tuple[int|float, int|float], surf:pg.Surface, colour=DARKGREY):
        """ the actual blit for this instance's .image surface is executed in draw_tab_to_pc """
        # obvs will add functionality for font and font size at some point, just is unnecessary rn
        text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_16.render(f"{text}", True, colour) 
        surf.blit(text_surf, pos) 

# -- Browser Tab Children --
class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add any specific parameters for the child class here, and then underneath super().__init__()
        super().__init__(game)
        # -- [NEW] v3.06 additions for new orders - current order sidebar --
        # -- declare vars to store lists of orders --
        self.sidebar_order_1 = {1:"Free Prawn Crackers", 2:"Grilled Charmander (Spicy)", 3:"Large Nuka Cola"}
        self.sidebar_order_2 = {1:"Free Prawn Crackers", 2:"Mario's Mushroom Soup", 3:"Squirtle Sashimi", 4:"Large Exeggcute Fried Rice"}
        self.sidebar_order_3 = {1:"Free Prawn Crackers"}
        # -- create the surface for the orders sidebar -- 
        self.width_offset = 90 # if this is set to zero then the sidebar will take exactly half the screen size, if set to 100 it will be -100px from the width and +100px in x axis 
        self.orders_sidebar_surf = pg.Surface(((self.rect.width / 2) - self.width_offset, self.rect.height))
        self.orders_sidebar_surf_colour = TAN
        self.orders_sidebar_surf.fill(self.orders_sidebar_surf_colour)
        # -- for tracking the active order --
        self.active_order_number = 1
        # -- first test implementation of menu items --
        # -- should put this into settings btw --
        self.menu_items_dict = {1:{"name":"Grilled Charmander", "price":7.99, "my_id":1, "course":"main", "has_toggles":True, "toggles":[("medium",0), ("spicy",0)]},
                                2:{"name":"Squirtle Sashimi", "price":9.49, "my_id":2, "course":"main"},
                                3:{"name":"Exeggcute Fried Rice", "price":9.49, "my_id":3, "course":"noodles_rice", "has_toggles":True, "toggles":[("large",2.50), ("regular",0)]},
                                4:{"name":"Nuka Cola", "price":3.15, "my_id":4, "course":"drinks", "has_toggles":True, "toggles":[("large", 1.75),("regular", 0),("quantum", 3), ("classic", 0)]},
                                5:{"name":"Mario's Mushroom Soup", "price":4.29, "my_id":5, "course":"starter"}}
        # -- more testing - menu item hover states & rects --
        self.menu_items_hover_states = {}
        for index in self.menu_items_dict.keys():
            self.menu_items_hover_states[index] = False
        self.menu_item_hover_rects = {}
        self.is_one_menu_item_hovered = False # if any of them is hovered, update the dimensions of one but use this to offset the y position of the others (remember -> only needs to be those below the hovered item, not above it!)
        # -- more testing - hover dimensions update --
        self.hover_height_increment = 50 # for all to scoot by this amount in the y when there is a hover


    def draw_orders_sidebar(self):
        self.image.blit(self.orders_sidebar_surf, ((self.rect.width / 2) + self.width_offset, 0)) 
        self.orders_sidebar_surf.fill(self.orders_sidebar_surf_colour) # also wipe this surface too

    def update(self):
        """ overrides the Browser_Tab parent update() function to include functionality for the orders sidebar """
        self.wipe_surface()
        self.draw_menu_items_selector()
        self.draw_orders_sidebar()
        # -- todo - make this a draw title instead --
        self.draw_text_to_surf(f"Order {self.active_order_number} Basket", (20, 30), self.orders_sidebar_surf) 
        # -- set the order list we will draw to the surface based on the currently active order number - could make this switch case ternary but probs way too long for a single line --
        if self.active_order_number == 1: 
            active_order_list = list(self.sidebar_order_1.values())
        elif self.active_order_number == 2:
            active_order_list = list(self.sidebar_order_2.values())
        elif self.active_order_number == 3:
            active_order_list = list(self.sidebar_order_3.values())
        else:
            # -- loop back to the start, temporary while using keyboard to change order number - note: might keep the keyboard press now tho tbf lol --
            self.active_order_number = 1 
            active_order_list = list(self.sidebar_order_1.values())
        # -- loop all the items in the order numbers list and draw them to the order sidebar surface --
        for index, an_item in enumerate(active_order_list):
            self.draw_text_to_surf(f"- {an_item}", (20, 80 + (index * 40)), self.orders_sidebar_surf)
        # -- check for mouse actions like click and hover --
        self.check_hover_menu_item()
            
    def draw_menu_items_selector(self):
        for index, an_item_dict in enumerate(self.menu_items_dict.values()):
            menu_item_surf = pg.Surface((300, 50))
            # -- if is hovered --
            if self.menu_items_hover_states[index + 1]:
                menu_item_surf = pg.Surface((400, 100))
                menu_item_surf.fill(MAGENTA)
                font_colour = WHITE
            # - else is not hovered, so alternate the colours, can be removed / updated, maybe to by course tbf --
            else:
                if index % 2 == 0:
                    menu_item_surf.fill(BLUEMIDNIGHT)
                    font_colour = WHITE
                else:
                    menu_item_surf.fill(SKYBLUE)
                    font_colour = BLUEMIDNIGHT
            # sort offsetting the positions dependant on if any item is hovered, and if it is below or above you, as if it is above you it doesnt need to move
            if self.is_one_menu_item_hovered:
                if index >= self.is_one_menu_item_hovered:
                        offset_y = self.hover_height_increment
                else:
                    offset_y = 0
            else:
                offset_y = 0
            # -- draw the surf dynamic bg surface, draw the item text to that surface, and lastly grab the hover rect and append it to an instance variable so we can check it for mouse collision later --
            test_item_pos = (50, 80 + (index * 40) + (index * 20) + offset_y)
            self.draw_text_to_surf(f"{an_item_dict['name']}", (10, 15), menu_item_surf, font_colour)
            item_hover_rect = self.image.blit(menu_item_surf, test_item_pos)
            self.menu_item_hover_rects[an_item_dict["my_id"]] = item_hover_rect
        
    def check_hover_menu_item(self):
        is_hovered_item = False
        for an_item_id, a_rect in self.menu_item_hover_rects.items():
            true_rect = self.game.get_true_rect(a_rect)
            if true_rect.collidepoint(pg.mouse.get_pos()):                       
                self.menu_items_hover_states[an_item_id] = True
                self.is_one_menu_item_hovered = an_item_id
                is_hovered_item = True
            else:
                self.menu_items_hover_states[an_item_id] = False
        # reset the .self var if there is no item hovered by the mouse
        if not is_hovered_item:
            self.is_one_menu_item_hovered = False
       

            


        


# doing now, make a function to loop the order side bar associated with the dict for the int
# - add new item to active one order list using keyboard button press
# - then make the physical clickable buttons for them
# - then put items in their own little cards too (for delete button, and maybe for quantities here on this side duhhh!)
# - should include types and give certain things toggles, i.e. if can be spicy (or whatever) then maybe u can order a range of spices, or maybe like "no xyz ingredient", kinda like maccas, hella simple

# things to remember todo for new orders functionality
# - quantities duh
# - delete btn duh


class Chats_Tab(Browser_Tab):
    def __init__(self, game): # < add any specific parameters for the child class here, and then underneath super().__init__()
        super().__init__(game)
       

# ---- End Browser Tabs ----


# -- Customer Initial First Test Implementation --
# note: consider making this an Object not a Sprite
class Customer(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.customers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- general stuff - should section better tho --
        self.my_id = len(game.customers) # will start at 1
        self.customer_state = "inactive" # active or completed or cancelled
        self.chatbox_state = choice(["shelved","opened"]) # opened or shelved, have them start shelved - only relevant when customer is active (for now anyways) 
        self.my_name = choice(["James","Jim","John","Jack","Josh","Tim","Tom","Jonathon","Steve","Carl","Mike","Brian"])
        self.my_name += " " + choice(["A","B","C","D","E","F","G","H","I","J","K","L"]) # add a display id - e.g KX139 or sumnt (have it be zones or sumnt but its slightly obscure so you dont twig it for a while, maybe like EWSN for cardinal directions)
 
    def __repr__(self):
        return f"Customer ID.{self.my_id} : {self.my_name}"

 
# -- Chatbox Class --
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
        self.shelved_pos = vec(25, game.pc_screen_surf_height - 110)
        # -- image surf setup --         
        self.image = self.game.window_img.copy()
        # -- set positions -- 
        initial_pos = (-500, -500) # initial position offscreen
        self.rect = self.image.get_rect()
        self.rect.move_ip(initial_pos)
        self.x, self.y = self.rect.x, self.rect.y
        # -- chatbox states and flags --
        self.is_hovered = False
        self.is_at_offscreen_position = True # always starts at the initial position when drawn (in reference to when drawn on screen not off screen at runtime)
        self.chatbox_move_activated = False 
        # -- mouse offset for moving window -- 
        self.mouse_offset_x = False # when chatbox_move_activated is True, set these to the rect x (& y) pos before moving
        self.mouse_offset_y = False # also ensure they are reset when chatbox_move_activated is False
        # -- titlebar setup --
        self.window_titlebar_height = 30 # note => am unsure if will change for open x shelved yet # width is just equal to opened_chat_width or shelved_chat_width
        # -- minimise icon setup - note => is when opened unless stated --
        self.minimise_icon_width, self.minimise_icon_height = 45, 23 # all hardcoded from the positions on the image
        self.pos_of_minimise_icon = 241 # for centering the title text as if you use opened_chat_width it just looks stupid, so just doing some minor adjustments here to make it a visually appealing center        
        self.shelved_pos_of_minimise_icon = 155 # but -10 from this for the rect width so that theres some padding    
    # ---- End Init ----

    # -- Draw, Update, & Repr --
 
    def update(self):
        if self.my_customer.customer_state == "active":
            # -- if opened set its position, draw its image and text to that image - and remember the image wont actually be drawn to the screen until draw -- 
            if self.my_customer.chatbox_state == "opened":
                if self.is_at_offscreen_position:
                    self.set_opened_chatbox_initial_position()
                    self.game.opened_chatbox_offset_counter += 1
                    self.wipe_image()
                    self.draw_name_to_chatbox()
                # -- if this instances has had move mode activated by clicking the top title bar of the window, then move it to the mouse pos, the offset that pos by the -pc_screen_width and height
                if self.chatbox_move_activated:
                    self.rect.x, self.rect.y = pg.mouse.get_pos()
                    self.rect = self.get_true_rect(a_rect=self.rect, move_in_negative=True)
                    # then to picked it up exactly where the mouse picked it up we do one more offset for the clicked pos minus the true position of the window and add that to the x & y
                    self.rect.move_ip(-self.mouse_offset_x, -self.mouse_offset_y)
            # -- handle shelved state -- 
            elif self.my_customer.chatbox_state == "shelved":             
                self.x, self.y = self.get_true_rect(self.rect).x, self.get_true_rect(self.rect).y
                self.wipe_image() # part works but isnt reseting the true rect and ting as per above so do that regardless, if will be diff image then do it seperately again not as same for open - make functs duhhh
                self.draw_name_to_chatbox()
                self.game.shelved_chatbox_offset_counter += 1
                self.set_shelved_chatbox_initial_position() 

    def __repr__(self):
        return f"Chatbox ID: {self.my_id}, layer: {self._layer}"

    # -- Blitting To This Chatbox Image Functs --

    def wipe_image(self):
        """ run this each frame before drawing anything to our image
        - this runs in update but we draw to this image in update then draw this actual image to the screen in draw, by self._layer """
        # -- opened state --
        if self.my_customer.chatbox_state == "opened":
            self.set_opened_state_image_surf()
        # -- shelved state --
        elif self.my_customer.chatbox_state == "shelved":
            self.set_shelved_state_image_surf()

    def set_shelved_state_image_surf(self):
        if self.is_hovered:
            self.image = self.game.window_shelved_hl_1_img.copy()
            self.rect = self.image.get_rect()  
        else:
            self.image = self.game.window_shelved_1_img.copy()
            self.rect = self.image.get_rect()

    def set_opened_state_image_surf(self):
        if self.chatbox_move_activated:
            self.image = self.game.window_hl_2_img.copy()
            self.rect = self.image.get_rect()
        elif self.is_hovered:
            self.image = self.game.window_hl_1_img.copy() 
        else: 
            self.image = self.game.window_img.copy()

    def draw_name_to_chatbox(self): 
        if self.my_customer.chatbox_state == "opened":
            self.draw_name_to_opened_chatbox()
        elif self.my_customer.chatbox_state == "shelved":
            self.draw_name_to_shelved_chatbox()
            
    def draw_name_to_opened_chatbox(self):        
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_16.render(f"{self.my_customer.my_name} (Lyr: {self._layer})", True, BLACK) 
        title_width = title.get_width()
        center_x_pos = (self.pos_of_minimise_icon - title_width) / 2
        self.image.blit(title, (center_x_pos + (self.minimise_icon_width / 4), 5)) # nudging abit for screen width vs minimise btn pos & width to get visually appealing center pos for the title text
            
    def draw_name_to_shelved_chatbox(self):        
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_16.render(f"{self.my_customer.my_name}", True, BLACK) 
        self.image.blit(title, (5, 8)) # nudging abit for screen width vs minimise btn pos & width to get visually appealing center pos for the title text

    # -- Handle Hover and Click States --

    def handle_hover_or_click(self):   
        """ notable -> executes for all instances `before` running all instances update() """           
        # -- og code - for handling click window to move to front      
        if self.my_customer.customer_state == "active":
            # -- get true rect of chatbox to check for collision -- 
            self.true_chatbox_window_rect = self.get_true_rect(self.rect)
            # -- if mouse collided with the chatbox rect --
            if self.true_chatbox_window_rect.collidepoint(pg.mouse.get_pos()):
                # -- update the image to the "highlighted" version --
                self.is_hovered = True
                # -- new code for handling click top bar and move - allowed only if you have collided with only the top highlighted rect only, not ones underneath --
                # -- create a new faux rect for the top bar at this windows position, then move it to the true pos on the screen --
                if self.my_customer.chatbox_state == "opened":
                    self.window_titlebar_rect = pg.Rect(self.x, self.y, self.pos_of_minimise_icon, self.window_titlebar_height)
                    # -- new rect for minimise collision when opened - note the btn is part of the image -- 
                    self.window_minimise_btn_rect = pg.Rect(self.x + self.pos_of_minimise_icon, self.y, 45, 25) # on img is actually 45 x 23
                    self.window_minimise_btn_rect = self.get_true_rect(self.window_minimise_btn_rect)
                elif self.my_customer.chatbox_state == "shelved":
                    self.window_titlebar_rect = pg.Rect(self.x, self.y, self.shelved_pos_of_minimise_icon - 10, self.window_titlebar_height)
                self.window_titlebar_rect = self.get_true_rect(self.window_titlebar_rect)
                # -- check for mouse collision on top hover btn rect if state is opened --                 
                if self.my_customer.chatbox_state == "opened":
                    if self.window_minimise_btn_rect.collidepoint(pg.mouse.get_pos()):
                        if self.game.mouse_click_up:
                            print(f"Clicked Minimise -> {self}")
                            self.my_customer.chatbox_state = "shelved"
                # -- check for mouse collision on top titlebar rect (up to 10 padding before minimise btn) if state is opened --                 
                    if self.window_titlebar_rect.collidepoint(pg.mouse.get_pos()):
                        if self.game.mouse_click_up:
                            self.chatbox_move_activated = True
                            # gives us the offset of the exact pos the mouse has "picked" up the window at
                            self.mouse_offset_x = pg.mouse.get_pos()[0] - self.true_chatbox_window_rect.x 
                            self.mouse_offset_y = pg.mouse.get_pos()[1] - self.true_chatbox_window_rect.y
                # -- new code to handle opening from shelved --
                # -- else if shelved just check the entire image for collision since all we can see if the top bar and clicking it only has open functionality, to open it (well and update its image and rect and position, etc, etc) --
                elif self.my_customer.chatbox_state == "shelved":
                    if self.game.mouse_click_up:
                        self.my_customer.chatbox_state = "opened"
                        self.x, self.y = self.window_titlebar_rect.x, self.window_titlebar_rect.y
                        self.rect = self.game.window_img.copy().get_rect()
                        self.rect.x, self.rect.y = self.x, self.y
                # -- if there waas a click on this rect too then update the layer to be at the front --
                if self.game.mouse_click_up:
                    pg.sprite.LayeredUpdates.change_layer(self.game.chatbox_layers, self, Chatbox.layers_counter) 
                # -- if there is a collision break looping the customers so we only check hover or click for a single chatbox, e.g. not if multiple windows are hovered at once --
                return True

    def unset_hover(self):
        """ unsets the hovered state... thank you for coming to my TEDtalk """
        self.is_hovered = False

    # -- Repositioning Functs --
    def set_shelved_chatbox_initial_position(self):
        shelved_chatboxes_offset = self.shelved_chat_width * (self.game.shelved_chatbox_offset_counter - 1)
        self.x, self.y = self.shelved_pos.x + shelved_chatboxes_offset, self.shelved_pos.y
        self.rect.x, self.rect.y = self.x, self.y # think the additional 25 is the screen edge btw, but should confirm this as am unsure tbf

    def set_opened_chatbox_initial_position(self):
        opened_chatboxes_offset = 50 * self.game.opened_chatbox_offset_counter # do need to check the positions tho remember (maybe do this before and not in loop) - skipping for like 2 mins tho
        self.x, self.y = self.opened_pos.x + opened_chatboxes_offset, self.opened_pos.y + opened_chatboxes_offset
        self.rect.x, self.rect.y = self.x, self.y

    def get_true_rect(self, a_rect:pg.Rect, move_in_negative=False):
        """ update a given rect position by offsetting it from the pc_screen x and y pos """
        # should probably make this a .game function when adding new classes as they will likely use it too
        moved_rect = a_rect.copy()
        if move_in_negative:
            moved_rect.move_ip(-self.game.pc_screen_surf_x, -self.game.pc_screen_surf_true_y)
        else:
            moved_rect.move_ip(self.game.pc_screen_surf_x, self.game.pc_screen_surf_true_y)
        return moved_rect
        
    