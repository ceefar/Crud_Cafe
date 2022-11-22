# -- imports --
import pygame as pg
from random import choice
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

    def draw_text_to_surf(self, text:str, pos:tuple[int|float, int|float], surf:pg.Surface, colour=DARKGREY, font_size=16, want_return=False):
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
        resulting_rect = surf.blit(text_surf, pos) 
        # -- return the resulting rect (pos & size) if you ask... nicely -- 
        if want_return:
            return resulting_rect

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


   # should do quick vid update at some point, dont have to speak is fine
   
   # - slick, smart on hover active delete btn idea using the same rect fade rect ? (the whole slide out "<- delete? / click to delete" idea)
   # - the customer talking stuff
   # - HUGE - the customer left side scene timer ui idea
   # - HUGE - the 2x book ideas, see notes
   # - HUGE - replacing the chats tab with orders x customers, see phone notes
   # - fade tweening?
   # - bg traffic?
   # - also port stuff from recent phone note

   # also
   # - should be auto scrolling btw on new msg!
    
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
            self.sidebar_bg_colour = TAN_ANALOGOUS_1 # TAN_ANALOGOUS_1 TAN_DARKER_1
        else:
            self.sidebar_bg_colour = self.orders_sidebar_surf_colour
        self.orders_sidebar_surf.fill(self.sidebar_bg_colour) # bg colour = TAN

    
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
                # -- decrement if the crud fade trigger activates and is this item, then blit the relevant fading bg surface for this item --
                if self.fading_alpha > 0:
                    self.fading_alpha -= 1
                # -- else if it hits 0, reset the trigger --
                elif self.fading_alpha == 0:                
                    self.fading_alpha = 0
                    self.trigger_active_order_crud_fade = False
                # -- if this thing isn't 0 then blit it --
                if self.fading_alpha:
                    crud_hightlight_bg_surf.set_alpha(self.fading_alpha) 
                    # -- the final blit --
                    self.orders_sidebar_surf.blit(crud_hightlight_bg_surf, crud_highlight_bg_rect)

            # -- draw this item and its quantity for the active order to the orders sidebar surf --
            self.draw_text_to_surf(f"{item_quantity}x {an_item}", (20, 80 + (index * 40) + self.orders_sidebar_scroll_y_offset), self.orders_sidebar_surf, font_size=14)

        # -- make this a draw title function now, and fix the below double blit --
        # - note actually also just fix the rect to be a standard rect like the bottom bar instead of just just the small rect behind the text
        # - note, do this title draw after drawing the scrolling text since it has a bg rect now as we want it to be on the bottom 
        order_basket_title_true_rect = self.draw_text_to_surf(f"Order {self.active_order_number} Basket", (20, 30), self.orders_sidebar_surf, want_return=True) 
        pg.draw.rect(self.orders_sidebar_surf, self.sidebar_bg_colour, order_basket_title_true_rect)
        # -- yes legit have to fix this to not do this blit twice - do it twice to get the size, can actually just alter that function to not blit and just return, bosh -- 
        self.draw_text_to_surf(f"Order {self.active_order_number} Basket", (20, 30), self.orders_sidebar_surf, want_return=True) 

        # -- check for mouse actions like click and hover --
        self.check_hover_menu_item()        

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
