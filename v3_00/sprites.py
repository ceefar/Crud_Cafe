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

    def draw_text_to_surf(self, text:str, pos:tuple[int|float, int|float], surf:pg.Surface, colour=DARKGREY, font_size=16):
        """ the actual blit for this instance's .image surface is executed in draw_tab_to_pc """
        # -- obvs will add functionality for font and font size at some point, just is unnecessary rn --
        if font_size == 10:
            text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_10.render(f"{text}", True, colour) 
        elif font_size == 12:
            text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_12.render(f"{text}", True, colour) 
        elif font_size == 14:
            text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_14.render(f"{text}", True, colour) 
        elif font_size == 16:
            text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_16.render(f"{text}", True, colour) 
        elif font_size == 18:
            text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_18.render(f"{text}", True, colour) 
        elif font_size == 20:
            text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{text}", True, colour) 
        # -- --
        surf.blit(text_surf, pos) 

# -- Browser Tab Children --
class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add any specific parameters for the child class here, and then underneath super().__init__()
        super().__init__(game)
        # -- [NEW] v3.06 additions for new orders - current order sidebar --
        # -- declare vars to store lists of orders --
        self.sidebar_order_1 = {1:"Grilled Charmander", 2:"Nuka Cola", 3:"Mario's Mushroom Soup", 4:"Squirtle Sashimi", 5:"Exeggcute Fried Rice"} # 6:"Mario's Mushroom Soup", 7:"Squirtle Sashimi", 8:"Large Exeggcute Fried Rice", 9:"Squirtle Sashimi", 10:"Large Exeggcute Fried Rice"
        self.sidebar_order_2 = {1:"Mario's Mushroom Soup", 2:"Squirtle Sashimi", 3:"Exeggcute Fried Rice"}
        self.sidebar_order_3 = {}

        # [ new! ]
        # -- again obvs will refactor this into one dictionary but since just adding this functionality in from scratch using this temp dict instead of updating the og dict variables --
        # quantity only will do for now lol
        self.sidebar_order_1_details = {"Grilled Charmander":{"quantity":1}, "Nuka Cola":{"quantity":1}, "Mario's Mushroom Soup":{"quantity":1}, "Squirtle Sashimi":{"quantity":1}, "Exeggcute Fried Rice":{"quantity":1}} 
        self.sidebar_order_2_details = {"Mario's Mushroom Soup":{"quantity":2}, "Squirtle Sashimi":{"quantity":2}, "Exeggcute Fried Rice":{"quantity":3}}
        self.sidebar_order_3_details = {}
        
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
        # -- will refactor the dicts in future to encompass this, just adding in it like this for now - also mays well bang it in settings tbf --
        self.menu_items_price_dict = {"Grilled Charmander":self.menu_items_dict[1]["price"],
                                        "Squirtle Sashimi":self.menu_items_dict[2]["price"],
                                        "Exeggcute Fried Rice":self.menu_items_dict[3]["price"],
                                        "Nuka Cola":self.menu_items_dict[4]["price"],
                                        "Mario's Mushroom Soup":self.menu_items_dict[5]["price"]}
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
        # -- new test - for current basket total --
        self.current_basket_total = 0.0
        # temp test for trigger crud fade rect idea
        self.trigger_active_order_crud_fade = False
        self.fading_alpha = 0


    # [ current! ]
    # - new stuff - 
    # -- order total sticky surf on the orders sidebar, positioned on top of the sticky bottom surf -- 
    def draw_basket_total_cost_bar(self):
        # -- dimensions and surf --
        self.sidebar_sticky_bottom_basket_cost_height = 40
        self.sidebar_sticky_bottom_basket_cost_width = self.orders_sidebar_surf.get_width()
        self.sidebar_sticky_bottom_basket_cost_surf = pg.Surface((self.sidebar_sticky_bottom_basket_cost_width, self.sidebar_sticky_bottom_basket_cost_height))
        self.sidebar_sticky_bottom_basket_cost_surf.fill(SKYBLUE)
        # -- text surf -- 
        basket_total_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_18.render(f"${self.current_basket_total:.2f}", True, BLACK) 
        # -- draw the text surf to the sticky bottom basket surf -- 
        self.sidebar_sticky_bottom_basket_cost_surf.blit(basket_total_text_surf, (20,10))
        # -- finally blit the sidebar sticky bottom surf to the sidebar surf above the other bottom order x basket selector / send to customer sticky bar -- 
        self.orders_sidebar_surf.blit(self.sidebar_sticky_bottom_basket_cost_surf, (0, self.rect.height - self.sidebar_sticky_bottom_surf_height - self.sidebar_sticky_bottom_basket_cost_height)) 
        
        
    # - note - ideally dont run this all the time, will be easy enough to do once the functionality is more finalised, i.e. set once, then reset on CRUD item only
    def update_basket_total(self):
        # -- store the running total --
        basket_running_total = 0.0

        # [ new-test! ] 
        # updating this to zip the sidebar_order_x_details now too 
        order_details_dict = self.get_active_order_details_dict()

        # [ new! ] 
        # [ running-total-here ] - want to do save the quantity to self here too and use that instead when passing it! << DO THIS! 
        # -- loop the active items and grab their prices from the menu items dict --
        for an_order_item in self.active_order_list: 
            order_item_price = self.menu_items_price_dict[an_order_item]
            item_quantity = order_details_dict[an_order_item]["quantity"]
            basket_running_total += (order_item_price * item_quantity)
        # -- set the current basket total to the result -- 
        self.current_basket_total = basket_running_total


    def get_active_order_details_dict(self):
        if self.active_order_number == 1:
            return self.sidebar_order_1_details
        elif self.active_order_number == 2:
            return self.sidebar_order_2_details
        elif self.active_order_number == 3:
            return self.sidebar_order_3_details

    
    # so after taking a well deserved break to get other stuff done 
    # - to finish up its just the rect bg alpha on update thing
    
    # then more generally
    # -------------------
    # - increase decrease (and delete?) buttons and functionality
    # - sending price to customer and resetting
    #   - HUGE N0TE
    #       - should be sending or saving the entire order (say save to customer) as a json file, also want to save the entire chatlog as a json file
    #       - like start doing this now and preparing to output it to sql too
    #       - and then maaaaybe in future ill actually do a load via sql too 
    #       - which is pretty much cloud saving functionality if you add simple user account functionality too o: 


    # -- end new stuff -- 


    # [ todo! ] - really need to chunk this up 
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

        # [ new! ]
        # -- blit the basket total cost sticky bottom surfaces --  
        self.draw_basket_total_cost_bar() # - note - have moved self.update_basket_total() to after the active_order switch in update()

        # -- then blit the new sticky bottom surface -- 
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
        # -- note - i think should probably be resetting this var at the start, but obvs it needs to be set too (not perma off), guna confirm more finalised functionality first before deciding --
        # self.customer_select_popup_selected_customer = False
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

                    # - update this to a .game var to be able to reset it here easily 
                    self.customer_select_popup_selected_customer = a_customer

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
                
                # -- New test --
                self.customer_select_popup_selected_customer = False # and reset this var

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
            

    	    # [ todo-stuff! ]
            if self.customer_select_popup_selected_customer:
                if self.game.mouse_click_up: 
                    
                    # [ new! ] 
                    # -- calculate the true amount of basket items from the quantities --
                    # should probably make this an update type funct btw and actually execute it in update or sumnt maybe, either way make it its own function
                    active_order_details_dict = self.get_active_order_details_dict()
                    basket_total_items = 0 
                    for basket_item_details in active_order_details_dict.values():
                        basket_total_items += basket_item_details["quantity"]

                    # [ todo-quickly! ] - so actually do the above stuff when you do the price stuff too (since assume am looping for that too)
                    # [ todo-quickly! ] - then set it to a self var and use it here bosh

                    # [ note! ] - wont actually be doing this loop here, will just be sending the price stuff, this is just temp for testing
                    for i, item in enumerate(self.active_order_list):
                       
                        # [ new! ]
                        # temp implementation for sending the finalised customer order details dict to the customer window
                        # - potentially could do the confirm (if the order sent matches the order the given customer wanted) logic implementation there too tbf

                        temp_details_dict_to_send = {"basket_price":self.current_basket_total, "basket_total_items":basket_total_items}

                        # - obvs only want to send payment here but its just easier to do it this way while testing
                        author_msg_pairs = [("api", "payment_window", temp_details_dict_to_send), ("customer", f"{item}")]
                        rng = choice(author_msg_pairs)
                        if rng[1] == "payment_window":
                            # -- now sending with current basket total if we are sending the payment_window msg to the customers message log --
                            self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].add_new_chatlog_msg(rng[0], rng[1], rng[2])
                        else:
                            # -- else it just adds the item as a new random message purely to test the functionality -- 
                            self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].add_new_chatlog_msg(rng[0], rng[1])

                        # -- debug - print the chatlog --
                        print(self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].my_chatlog)

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

            # [ new! ]
            # -- get the quantity from the new active order details dict --
            order_details_dict = self.get_active_order_details_dict()
            item_quantity = order_details_dict[an_item]["quantity"]
            

            # - doing the bg rect on crud a new item to the active order, so ig have it obvs drawn here, or thereabouts, and have it activated elsewhere, aite 
            # [ current! ] 
            # [ here! ] 
            # [ rnrn! ] 
            # the setup 
            crud_highlight_width = 250
            crud_highlight_height = 30
            crud_highlight_bg_rect = pg.Rect(20 - 5, 80 + (index * 40) + self.orders_sidebar_scroll_y_offset - 7, crud_highlight_width, crud_highlight_height) # have done -5 in x and y as this is just the text pos (ok nudging a bit more in the y tho)
            crud_hightlight_bg_surf = pg.Surface((crud_highlight_width, crud_highlight_height)).convert_alpha() # doing a now too surf as want the transparency
            crud_hightlight_bg_surf.fill(ORANGE)


            if self.trigger_active_order_crud_fade == an_item:
                # print(f"FIGHT! > {an_item = } vs {self.trigger_active_order_crud_fade = }")
                if self.fading_alpha > 0:
                    self.fading_alpha -= 1
                elif self.fading_alpha == 0:                
                    self.fading_alpha = 0
                    self.trigger_active_order_crud_fade = False

                if self.fading_alpha:
                    crud_hightlight_bg_surf.set_alpha(self.fading_alpha) 
                    # the blit
                    self.orders_sidebar_surf.blit(crud_hightlight_bg_surf, crud_highlight_bg_rect)


            # -- draw this item and its quantity for the active order to the orders sidebar surf --
            self.draw_text_to_surf(f"{item_quantity}x {an_item}", (20, 80 + (index * 40) + self.orders_sidebar_scroll_y_offset), self.orders_sidebar_surf, font_size=14)

                    


        # -- check for mouse actions like click and hover --
        self.check_hover_menu_item()

        # new
        # temp test for fading bg rect on crud thing
        # -- considering putting this here, either way defo make it its own function --
    
        
        

        # [ new! ]
        # -- new test addition for updating the active/current basket total - note is running the calculation the frame after the initial blit --
        self.update_basket_total() # - note -  could easily be resolved by creating an active_order_number switch in that function (do actually have that function now btw if u wanna do this lol), but this is perfectly fine, just noting it incase of a major refactor as its not with draw_basket_total_cost_bar()
            

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
            # --  draw the item text to that surface after drawing the surf dynamic bg surface underneath, then grab the hover rect and append it to an instance variable so we can check it for mouse collision later --
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

                    # [ todo-quick! ]
                    # -- 100% MAKE THIS A FUNCTION ONCE DONE TESTING! --
                    if self.active_order_number == 1:                    
                        to_add_to_list = self.sidebar_order_1
                    elif self.active_order_number == 2:                    
                        to_add_to_list = self.sidebar_order_2
                    elif self.active_order_number == 3:                    
                        to_add_to_list = self.sidebar_order_3
                    
                    # [ new! ]
                    # -- adds the actual item to the active order and the new associated order detail dict --
                    # -- first get the details dict for this active order --
                    active_order_details_dict = self.get_active_order_details_dict()
                    # -- if this item **is** already in the active sidebar order list, then add it to this orders details dict as a new item to the dict (not a quantity update) --
                    if an_item_dict["name"] in to_add_to_list.values():                        
                        active_order_details_dict[an_item_dict["name"]]["quantity"] += 1
                     # -- else, if its not in the active sidebar order list, then add it to this orders details dict as a new item to the dict (not as an update to the quantity) --
                    else:
                        active_order_details_dict[an_item_dict["name"]] = {"quantity": 1}
                        to_add_to_list[len(to_add_to_list) + 1] = f"{an_item_dict['name']}"

                    # [ new! ]
                    # -- testing triggering bg on crud a menu item to the active orders menu, with fade effect (much wow!) --
                    # so its defo guna have "name" by now since we're doing it after the above dict update stuff
                    self.trigger_active_order_crud_fade = an_item_dict["name"]                    
                    #
                    # self.trigger_active_order_crud_fade = True
                    self.fading_alpha = 80
                        
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
# -- End New Orders Tab Class --     


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

        # -- new test for scrolling chat window --
        self.chatbox_window_scroll_y_offset = 0 

        # -- new test for chatlog blit stuff --
        self.chatlog_text_msg_height = 45
        self.chatlog_payment_msg_height = 108 
        # -- more new chatlog stuff --
        self.my_chatlog = [] 
        if self.my_id == 3: # 50 start pos + 110 size + 20 padding -> for testing formatting, then extra 30 is just the move down amount of chococake, likely too much tho but dw
            self.my_chatlog = [{"author":"customer", "msg":f"One Chocolate Cake Plis", "chat_pos":50, "height":45}, {"author":"api", "msg":f"payment_window", "chat_pos":110, "height":208}]  # {"author":f"customer", "msg":f"Chocolate Cake", "chat_pos":225}

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

                    # -- NEW --
                    # - drawing chatlog stuff -
                    # self.test_draw_payment_element()
                    self.draw_my_chatlog()
                
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


    # -- New Chat Message First Test Stuff --

    def draw_payment_element(self, pos, order_details:dict): # {"price": 18.99}
        payment_pending_img = self.game.payment_pending_1_img.copy()
        # [ new! ]
        # -- get the price from the new details dict --
        self.basket_price = float(f"{order_details['basket_price']:.2f}") # set the precision to 2 decimal places
        self.basket_total_items = order_details["basket_total_items"]
        # -- create the text surfaces --
        basket_price_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_26.render(f"${self.basket_price}", True, FORESTGREEN)
        basket_total_items_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_12.render(f"basket items: {self.basket_total_items}", True, BLACK)
        # -- draw the text surfs to this objects copy of the payment window img 
        payment_pending_img.blit(basket_price_text_surf, (78, 27)) 
        payment_pending_img.blit(basket_total_items_text_surf, (78, 57)) 
        # obvs and then can do the delivery charge stuff here too
        # - even would be cute for them to sometimes stop the transaction because of this but **not** anytime soon
        
        # [ rnrn! ] - just last remaining thing to do is the quantities 
        
        self.image.blit(payment_pending_img, pos)
        # will want a handler function that will sort all the different payment plus associated sprite animation states


    def add_new_chatlog_msg(self, author:str, msg:str, order_details=None): # [ new! ] just sending price for now but obvs guna update 
        # -- create the dictionary chatlog item --
        chatlog_dictionary_entry = {}

        # -- set author --
        author_entry = author

        # -- set msg entry and chat height --
        # - payment window - 
        if msg == "payment_window":
            msg_entry = "payment_window"
            chat_height_entry = self.chatlog_payment_msg_height
        # - text message -
        else: # only doing these two (payment window vs any other msg) while testing init functionality
            msg_entry = msg
            chat_height_entry = self.chatlog_text_msg_height
            
        # -- set y position --
        # -- if there is anything in the chatlog, then we use dynamic positions --
        if self.my_chatlog:
            # [ here! ]
            # <- to do this dynamically based on size of the previous entry
            last_chat_entry_pos = self.my_chatlog[-1]["chat_pos"]
            last_chat_entry_height = self.my_chatlog[-1]["height"]
            chat_pos_entry = last_chat_entry_pos + last_chat_entry_height + 10 # 110 
        # -- else, this is the first chat message so we set it to the initial position --
        else:
            chat_pos_entry = 50
            
        # -- create the final dict of the chatlog entry --
        chatlog_dictionary_entry["author"] = author_entry
        chatlog_dictionary_entry["msg"] = msg_entry
        chatlog_dictionary_entry["height"] = chat_height_entry
        chatlog_dictionary_entry["chat_pos"] = chat_pos_entry
        if order_details:
            chatlog_dictionary_entry["order_details"] = order_details

        # -- finally, append the finalised dict to the chatlog list --
        self.my_chatlog.append(chatlog_dictionary_entry)


    def draw_my_chatlog(self):
        if self.my_chatlog:
            for i, a_chatlog_item in enumerate(self.my_chatlog):
                a_msg = a_chatlog_item["msg"]
                an_author = a_chatlog_item["author"]
                a_chat_line_y_pos = a_chatlog_item["chat_pos"]

                # [ new! ]
                if "order_details" in a_chatlog_item:
                    order_details = a_chatlog_item["order_details"]

                x_pos = 20 if an_author == "api" or an_author == "customer" else 60
                chat_bg_colour = CUSTOMERTAN if an_author == "api" or an_author == "customer" else PURPLE # using bg colour in actual image for the imgs (i.e. payment window) tho
                
                # -- if payment window msg, draw the payment element to the window --
                if a_msg == "payment_window":
                    self.draw_payment_element((x_pos, a_chat_line_y_pos + self.chatbox_window_scroll_y_offset), order_details) # 50 + (40 * i)
                # -- else if any other message, draw it as text -- 
                else:
                    # -- if valid author create the author text surface --
                    if an_author == "customer":
                        author_name_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_10.render(f"{self.my_customer.my_name}", True, BLACK)
                    # -- create the message text surface --
                    a_msg_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_14.render(f"{a_msg}", True, BLACK)
                    # -- setup and draw the background rect --
                    text_chat_max_width = 250
                    chat_bg_rect = pg.Rect(x_pos, a_chat_line_y_pos + self.chatbox_window_scroll_y_offset, text_chat_max_width, 45)  
                    pg.draw.rect(self.image, chat_bg_colour, chat_bg_rect, 0, 5)
                    # -- setup the remaining blit positions --
                    x_pos += 10 # for text the x pos is + 10 from the bg rect
                    author_offset = 0
                    y_offset = 5 # general offset since the bg rect is draw at the actual pos, this offsets the text in y so its formatted nicely 
                    # -- if there is a valid author, blit the author text surf to the window, and offset the message pos, else dont
                    if an_author == "customer":
                        self.image.blit(author_name_surf, (x_pos, a_chat_line_y_pos + y_offset + self.chatbox_window_scroll_y_offset)) 
                        author_offset += 10 
                    # -- finally blit the actual msg to the window --
                    self.image.blit(a_msg_surf, (x_pos, a_chat_line_y_pos + author_offset + y_offset + self.chatbox_window_scroll_y_offset)) # (x_pos, 50 + (40 * i))

    # -- End of Test Stuff -- 


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
        
    