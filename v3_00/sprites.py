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
        self.sidebar_order_1 = {1:"Grilled Charmander (Spicy)", 2:"Large Nuka Cola", 3:"Mario's Mushroom Soup", 4:"Squirtle Sashimi", 5:"Large Exeggcute Fried Rice", 6:"Mario's Mushroom Soup", 7:"Squirtle Sashimi"} # 8:"Large Exeggcute Fried Rice", 9:"Squirtle Sashimi", 10:"Large Exeggcute Fried Rice"
        self.sidebar_order_2 = {1:"Mario's Mushroom Soup", 2:"Squirtle Sashimi", 3:"Large Exeggcute Fried Rice"}
        self.sidebar_order_3 = {}
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
                                2:{"name":"Squirtle Sashimi", "price":9.49, "my_id":2, "course":"main", "has_toggles":False},
                                3:{"name":"Exeggcute Fried Rice", "price":9.49, "my_id":3, "course":"noodles_rice", "has_toggles":True, "toggles":[("large",2.50), ("regular",0)]},
                                4:{"name":"Nuka Cola", "price":3.15, "my_id":4, "course":"drinks", "has_toggles":True, "toggles":[("large", 1.75),("regular", 0),("quantum", 3), ("classic", 0)]},
                                5:{"name":"Mario's Mushroom Soup", "price":4.29, "my_id":5, "course":"starter", "has_toggles":False}}
        # -- menu items dimensions --
        self.menu_items_hovered_width = 500
        self.menu_items_normal_width = 300
        # -- menu item hover states & rects --
        self.menu_items_hover_states = {}
        for index in self.menu_items_dict.keys():
            self.menu_items_hover_states[index] = False
        self.menu_item_hover_rects = {}
        self.is_one_menu_item_hovered = False # if any of them is hovered, update the dimensions of one but use this to offset the y position of the others (remember -> only needs to be those below the hovered item, not above it!)
        # -- for menu items hover, y pos offset --
        self.hover_height_increment = 50 # for all to scoot by this amount in the y when there is a hover
        # -- item and add to cart button dimensions --
        self.toggle_btn_padding = 20 # preset padding var for item toggle and add to order buttons
        self.add_to_order_btn_max_width = (500 - (6 * self.toggle_btn_padding)) / 5 # the size used when there are no toggles, 4 is the max toggles, then + 1 for 5, so then we also need 6 * the padding 
        # -- for scrolling functionality --
        self.orders_sidebar_scroll_y_offset = 0 
        self.is_orders_sidebar_surf_hovered = False
        # -- new test - for customer selector popup window --
        self.want_customer_select_popup = False
        self.customer_select_popup_selected_customer = False


    def draw_orders_sidebar(self):
        # -- for drawing active order buttons - but just as indicators for now, no on click functionality yet --
        self.sidebar_sticky_bottom_surf_height = 140
        self.sidebar_sticky_bottom_surf = pg.Surface((self.orders_sidebar_surf.get_width(), self.sidebar_sticky_bottom_surf_height))
        self.sidebar_sticky_bottom_surf.fill(YELLOW)
        # -- btn and btn padding dimensions  --
        self.order_number_indicator_btn_size = 40
        self.order_number_indicator_btn_padding = 50
        
        # -- handle the order number indicator buttons and handle the hover state and colour changes --
        # -- logic here - spit the sections into 3 quadrants, for each of the 3 buttons (30 is just a small adjustment as the width overruns due to the screen edge, i believe) -- 
        # -- then minuse the button size from those quadrants so you have the padding on either side added together remaining, then simple div 2 to get the width of both sides seperately and place the button at the end pos of the first padding rect in the quadrant --       
        btn_increment_pos = (((self.orders_sidebar_surf.get_width() / 3) - 25) - self.order_number_indicator_btn_size) / 2
        # -- logic continued -- then increment over the amount of buttons to move along by a quadrant and draw the button rect centralised within it -- 
        # -- new test continued - loop and draw order indicator buttons --
        for i in range(1,4):
            self.order_number_indicator_btn = pg.Rect(btn_increment_pos + ((i-1) * (self.orders_sidebar_surf.get_width() / 3)), 10, self.order_number_indicator_btn_size, self.order_number_indicator_btn_size)
            # -- if this indicator buttons index is the same as the order number then draw a green button else draw a red one --
            indicator_colour = GREEN if self.active_order_number == i else RED
            # -- draw the rect, get the true rect for hover, and add the basics of the hover functionality tho not adding on click stuff right now --
            order_number_indicator_btn_true_rect = pg.draw.rect(self.sidebar_sticky_bottom_surf, indicator_colour, self.order_number_indicator_btn)
            order_number_indicator_btn_true_rect = self.game.get_true_rect(order_number_indicator_btn_true_rect)
            order_number_indicator_btn_true_rect.move_ip(self.orders_sidebar_surf.get_width() + 180, self.rect.height - self.sidebar_sticky_bottom_surf_height)
            if order_number_indicator_btn_true_rect.collidepoint(pg.mouse.get_pos()):
                pg.draw.rect(self.sidebar_sticky_bottom_surf, ORANGE, self.order_number_indicator_btn)

        # -- handle the add to customer order button -- 
        add_to_customer_btn_width = 300
        add_to_customer_btn_center_pos = int(((self.orders_sidebar_surf.get_width() - 25) - add_to_customer_btn_width) / 2) # now confirmed - the extra 25 **is** the screen edge lol
        add_to_customer_btn = pg.Rect(add_to_customer_btn_center_pos, self.order_number_indicator_btn_size + 25, add_to_customer_btn_width, self.order_number_indicator_btn_size)
        add_to_customer_btn_true_rect = pg.draw.rect(self.sidebar_sticky_bottom_surf, BLUE, add_to_customer_btn)
        # -- add hover and on click functionality -- 
        add_to_customer_btn_true_rect = self.game.get_true_rect(add_to_customer_btn_true_rect)
        add_to_customer_btn_true_rect.move_ip(self.orders_sidebar_surf.get_width() + 180, self.rect.height - self.sidebar_sticky_bottom_surf_height)
        # -- on hover - change rect colour --
        if add_to_customer_btn_true_rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(self.sidebar_sticky_bottom_surf, SKYBLUE, add_to_customer_btn)
            # -- on hover - update state to show popup --
            if self.game.mouse_click_up: 
                self.want_customer_select_popup = True
            

            # still fair few things to do here obvs 
            # - start by adding the text for the button


        # -- finally blit the new sticky bottom surface -- 
        self.orders_sidebar_surf.blit(self.sidebar_sticky_bottom_surf, (0, self.rect.height - self.sidebar_sticky_bottom_surf_height)) 

        # -- draw the sidebar --
        orders_sidebar_surf_true_rect = self.image.blit(self.orders_sidebar_surf, ((self.rect.width / 2) + self.width_offset, 0)) 

        # -- adds hover state to orders sidebar to improve scrolling ux by only allowing scroll when hovered over the surface you want to scroll i.e. this orders sidebar surf --        
        orders_sidebar_surf_true_rect = self.game.get_true_rect(orders_sidebar_surf_true_rect)
        if orders_sidebar_surf_true_rect.collidepoint(pg.mouse.get_pos()):  
            self.is_orders_sidebar_surf_hovered = True
        else:
            self.is_orders_sidebar_surf_hovered = False

        # -- wipes the surface, drawing the analogous bg colour if the orders sidebar surface is hovered --
        if self.is_orders_sidebar_surf_hovered:
            bg_colour = TAN_ANALOGOUS_1 # TAN_ANALOGOUS_1 TAN_DARKER_1
        else:
            bg_colour = self.orders_sidebar_surf_colour
        self.orders_sidebar_surf.fill(bg_colour) # bg colour = TAN

    
    def draw_active_customers_selector_popup(self):
        # -- first blit a background surf for the popup --
        popup_bg = pg.Surface((self.rect.width, self.rect.height)).convert_alpha()
        popup_bg.fill(DARKGREY)
        popup_bg.set_alpha(120)
        self.image.blit(popup_bg, (0,0))
        # -- configure the actual popup --
        self.customer_selector_popup_window_width = 600
        self.customer_selector_popup_window_height = 400
        self.customer_selector_popup_window_surf = pg.Surface((self.customer_selector_popup_window_width, self.customer_selector_popup_window_height))
        self.customer_selector_popup_window_surf.fill(WHITE)

        # -- draw title text to the popup surf -- 
        text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"Select Customer", True, BLACK) 
        self.customer_selector_popup_window_surf.blit(text_surf, (20, 20)) 

        # -- draw customer names buttons - semi temp, kinda buttons but not really but whatever --
        for i, a_customer in enumerate(self.game.all_active_customers.values()):
            text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{a_customer.my_name}", True, WHITE) 
            customer_selector_bg_rect = pg.Rect(20, 25 + (50 * (i+1)), 250, 40)
            # -- then draw and get true rect -- 
            customer_selector_btn_true_rect = pg.draw.rect(self.customer_selector_popup_window_surf, SKYBLUE, customer_selector_bg_rect)
            # -- update the true rect for mouse collision -- 
            customer_selector_btn_true_rect = self.game.get_true_rect(customer_selector_btn_true_rect)
            customer_selector_btn_true_rect.move_ip(int((self.rect.width - self.customer_selector_popup_window_width) / 2), int((self.rect.height - self.customer_selector_popup_window_height) / 2) - 25)
            if customer_selector_btn_true_rect.collidepoint(pg.mouse.get_pos()):
                pg.draw.rect(self.customer_selector_popup_window_surf, BLUEMIDNIGHT, customer_selector_bg_rect)
                if self.game.mouse_click_up: 

                    # [ CRITICAL! ]
                    self.customer_select_popup_selected_customer = a_customer
                    # REMEMBER WHEN YOU CLICK CLOSE OR SELECT TO WIPE THIS VAR!

            # -- if this is the selected customer then set the colour to green to visually confirm the click, ux baybayyy -- 
            if self.customer_select_popup_selected_customer is a_customer:
                pg.draw.rect(self.customer_selector_popup_window_surf, FORESTGREEN, customer_selector_bg_rect)

            # -- then at the end draw the text on top --
            self.customer_selector_popup_window_surf.blit(text_surf, (30, 32 + (50 * (i+1)))) 

        # -- new test for close button --
        self.close_btn_size = 30
        self.close_btn_padding = 20
        self.close_btn_surf = pg.Surface((30, 30))
        self.close_btn_surf.fill(RED)
        self.close_btn_true_rect = self.customer_selector_popup_window_surf.blit(self.close_btn_surf, (self.customer_selector_popup_window_width - self.close_btn_size - self.close_btn_padding, self.close_btn_padding)) 
        self.close_btn_true_rect = self.game.get_true_rect(self.close_btn_true_rect)
        self.close_btn_true_rect.move_ip(int((self.rect.width - self.customer_selector_popup_window_width) / 2), int((self.rect.height - self.customer_selector_popup_window_height) / 2) - 25)
        if self.close_btn_true_rect.collidepoint(pg.mouse.get_pos()): 
            # -- on hover change colour for visual clarity, ux is good mkay -- 
            self.close_btn_surf.fill(DARKRED)
            self.customer_selector_popup_window_surf.blit(self.close_btn_surf, (self.customer_selector_popup_window_width - self.close_btn_size - self.close_btn_padding, self.close_btn_padding)) 
            # -- on click, set the state to close the popup window --
            if self.game.mouse_click_up: 
                self.want_customer_select_popup = False

        # -- new test for confirm button --
        # - want this to be on select dynamic text 
        self.customer_selector_confirm_btn_surf = pg.Surface((200, 50))
        if self.customer_select_popup_selected_customer:
            self.customer_selector_confirm_btn_surf.fill(FORESTGREEN)
        else:
            self.customer_selector_confirm_btn_surf.fill(PALEGREEN)

        # -- if we have confirm text then draw it --
        if self.customer_select_popup_selected_customer:
            confirm_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.customer_select_popup_selected_customer.my_name}", True, WHITE)
            self.customer_selector_confirm_btn_surf.blit(confirm_text_surf, (20, 20)) 

        self.customer_selector_confirm_btn_true_rect = self.customer_selector_popup_window_surf.blit(self.customer_selector_confirm_btn_surf, (self.customer_selector_popup_window_width - 200 - self.close_btn_padding, self.customer_selector_popup_window_height - 50 - self.close_btn_padding)) # 200 and 50 here is the width and height of the surf, obvs hard code this duh
        # exact same calculation as above so whack this in a function to return a copy of the rect given as a parameter and reuse the function 
        self.customer_selector_confirm_btn_true_rect = self.game.get_true_rect(self.customer_selector_confirm_btn_true_rect)
        self.customer_selector_confirm_btn_true_rect.move_ip(int((self.rect.width - self.customer_selector_popup_window_width) / 2), int((self.rect.height - self.customer_selector_popup_window_height) / 2) - 25)
       
        # -- obvs will have on hover like this but also a different condition to update the colour and text when a customer has been selected --
        if self.customer_selector_confirm_btn_true_rect.collidepoint(pg.mouse.get_pos()): 
            if self.customer_select_popup_selected_customer:
                # if we can click this button, then on hover show green colour
                self.customer_selector_confirm_btn_surf.fill(GREEN)
            else:
                # else if we cant click this button, on hover show red colour
                self.customer_selector_confirm_btn_surf.fill(RED)
            
            # -- again, if we have confirm text then draw it --
            if self.customer_select_popup_selected_customer:
                confirm_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.customer_select_popup_selected_customer.my_name}", True, WHITE)
                self.customer_selector_confirm_btn_surf.blit(confirm_text_surf, (20, 20)) 
                
            self.customer_selector_popup_window_surf.blit(self.customer_selector_confirm_btn_surf, (self.customer_selector_popup_window_width - 200 - self.close_btn_padding, self.customer_selector_popup_window_height - 50 - self.close_btn_padding))
            

    	    # [ here! ]
            if self.customer_select_popup_selected_customer:
                if self.game.mouse_click_up: 
                    for i, item in enumerate(self.active_order_list):
                        print(f"Blit {item} to {self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1]} for {self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].my_customer}")
                        # blit to the chatbox associated with this customers id, temporary while testing until doing in chatbox function
                        self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].my_chatlog.append({"author":"api", "msg":f"{item}"})

                # k so just guna draw to the image from here to test but
                # actually create a function in the chatbox to handle this, since it needs the order of chats for the position n ting


        # - then sending just any text to that customers window surface and wiping/resetting the surface vars and tings
        #   - can probably just access that directly using the dict key value pairs in .game that are by id
        #   - obvs need to do the pre-blit list thing first so thats next! 
        #       - eeeee so awesome :D

        # - smashed it
        # - see below and see notes obvs but mostly i think first just start of this new version with...

        # - scroll for the windows
        # - oh and also wiping the current one <3


        # - then a button that says not selected bottom right, and then when u click a name it shows it as selected and sets the button text to "add to {selected_name}"
        # - then legit get that to actually do the blit to their window and wipe the order and omg <3 new version
        #   - note => just as basic for now is fine (will make it be total or sumnt - for now just len of the basket)
        #   - ensure this actually works by only adding in 2 or 3 to test
        #   - then adding more after with new baskets created and blit to the window (in a new, next chat position each time) 

        
        # -- then blit the actual popup --
        self.customer_selector_popup_window_true_rect = self.image.blit(self.customer_selector_popup_window_surf, (int((self.rect.width - self.customer_selector_popup_window_width) / 2), int((self.rect.height - self.customer_selector_popup_window_height) / 2) - 25)) # minus 25 for (half of) the toptab bar which isnt done yet, but is hardcoded so replace the 50 here lol 
        self.customer_selector_popup_window_true_rect = self.game.get_true_rect(self.customer_selector_popup_window_true_rect)
        # -- temp --
        if self.customer_selector_popup_window_true_rect.collidepoint(pg.mouse.get_pos()): 
            # hovered the popup rect - can remove was temp for closing the popup before adding an actual close button
            pass
            

    def update(self):
        """ overrides the Browser_Tab parent update() function to include functionality for the orders sidebar """
        self.wipe_surface()
        self.draw_menu_items_selector()
        self.draw_orders_sidebar()
        # -- todo - make this a draw title instead --
        self.draw_text_to_surf(f"Order {self.active_order_number} Basket", (20, 30), self.orders_sidebar_surf) 
        # -- set the order list we will draw to the surface based on the currently active order number - could make this switch case ternary but probs way too long for a single line --
        if self.active_order_number == 1: 
            self.active_order_list = list(self.sidebar_order_1.values())
        elif self.active_order_number == 2:
            self.active_order_list = list(self.sidebar_order_2.values())
        elif self.active_order_number == 3:
            self.active_order_list = list(self.sidebar_order_3.values())
        else:
            # -- loop back to the start, temporary while using keyboard to change order number - note: might keep the keyboard press now tho tbf lol --
            self.active_order_number = 1 
            self.active_order_list = list(self.sidebar_order_1.values())
        # -- loop all the items in the order numbers list and draw them to the order sidebar surface using the scroll offset --
        for index, an_item in enumerate(self.active_order_list):

            # Note! => quantity stuff, maybe here
            self.draw_text_to_surf(f"1x {an_item}", (20, 80 + (index * 40) + self.orders_sidebar_scroll_y_offset), self.orders_sidebar_surf)

        # -- check for mouse actions like click and hover --
        self.check_hover_menu_item()
            
    def draw_menu_items_selector(self):
        for index, an_item_dict in enumerate(self.menu_items_dict.values()):
            menu_item_surf = pg.Surface((self.menu_items_normal_width, 50))
            # -- if is hovered --
            if self.menu_items_hover_states[index + 1]:
                menu_item_surf = pg.Surface((self.menu_items_hovered_width, 100))
                if an_item_dict["has_toggles"]:
                    menu_item_surf.fill(RED)
                else:
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
            item_price = an_item_dict["price"]
            self.draw_text_to_surf(f"{an_item_dict['name']} ${item_price}", (10, 15), menu_item_surf, font_colour) # now includes price

            # -- new test - draw buttons for the toggles if it has buttons else just draw one button to add to order -- 
            if an_item_dict["has_toggles"]:
                pass 
                # -- in progress - for toggle btns --
                # for index, a_toggle in enumerate(an_item_dict["toggles"]):
                #     toggle_name = a_toggle[0] 
                #     toggle_extra_cost = a_toggle[1]
            else:
                pass
            # -- finally draw the add to order button at the end regardless of if there are toggles or not --
            end_btn_x_pos = (self.add_to_order_btn_max_width * 4) + (self.toggle_btn_padding * 5)
            add_to_order_btn = pg.Rect(end_btn_x_pos, 30, self.add_to_order_btn_max_width, 40)
            item_add_to_order_btn_true_rect = pg.draw.rect(menu_item_surf, SKYBLUE, add_to_order_btn)
            item_add_to_order_btn_true_rect = self.game.get_true_rect(item_add_to_order_btn_true_rect)
            item_add_to_order_btn_true_rect.move_ip(test_item_pos)
            if item_add_to_order_btn_true_rect.collidepoint(pg.mouse.get_pos()):   
                pg.draw.rect(menu_item_surf, GREEN, add_to_order_btn)  

                # -- if the player clicks the add to order button then add this item to the currently active order number --
                if self.game.mouse_click_up: 

                    # -- 100% MAKE THIS A FUNCTION ONCE DONE TESTING! --
                    if self.game.new_orders_tab.active_order_number == 1:                    
                        to_add_to_list = self.game.new_orders_tab.sidebar_order_1
                    elif self.game.new_orders_tab.active_order_number == 2:                    
                        to_add_to_list = self.game.new_orders_tab.sidebar_order_2
                    elif self.game.new_orders_tab.active_order_number == 3:                    
                        to_add_to_list = self.game.new_orders_tab.sidebar_order_3
                    to_add_to_list[len(to_add_to_list) + 1] = f"{an_item_dict['name']}"
                        
            # -- do the blit and store the resulting rect to check hover via mouse collide -- 
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
    

# - scroll bars todo
#   - current basket text needs to be on a bg rect so it looks sticky
#   - scroll bar to incdicate when scroll is possible
#       - and only allowing scroll when it is actually possible 

# - add to customer order button and working
#   - ensure sticky bottom of orders sidebar works
#   - ensure have adding to new position in customer window functionality surf sorted
#   - and do on hover scroll for these windows too

# - possible hover outline rect moving idea but also maybe not just respace a bit more is fine
# - remove from cart
# - quants
# - pricing up the actual cart duhhh lol

# - see phone
# - but basically first up to do
#   - orders x customers page
#   - improved gui stuff
#   - toggles stuff that i skipped
#   - talking
#   - moving

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

        # -- new test for chatlog blit stuff --
        self.my_chatlog = [] # [{"author":"api", "msg":"your order"},{"author":"api", "msg":"number is 23041309"}] # am thinking as a list of dicts, i.e. json

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
                    self.test_draw_my_chatlog()
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


    # -- initial first test implementatino for chatlog drawing --
    def test_draw_my_chatlog(self):
        if self.my_chatlog:
            for i, a_chatlog_item in enumerate(self.my_chatlog):
                a_msg = a_chatlog_item["msg"]
                a_msg_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_16.render(f"{a_msg}", True, BLACK)
                # blit to the chatbox associated with this customers id, temporary while testing until doing in chatbox function
                self.image.blit(a_msg_surf, (30, 50 + (40 * i)))


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
        
    