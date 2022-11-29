# -- imports --
import pygame as pg
from random import choice, randint
from settings import *
vec = pg.math.Vector2


# ---- Browser Tab Parent Class ---- 

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

    def update(self):
        self.wipe_surface()

    def draw_tab_to_pc(self):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        # [ possibly-temp ]
        # - actually not doing this for the Preparing_Orders_Tab now, and tbf might refactor to do it the new way for all of the Tab subclasses via the parent
        if not isinstance(self, Preparing_Orders_Tab):
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{self.my_tab_name}", True, DARKGREY) 
            self.image.blit(title, (50,30))  
        # -- end temp --
        # [new!] - note - test 15 (from 0) for tab bar adjustment
        self.game.pc_screen_surf.blit(self.image, (0, self.game.tab_bar_height + 15)) # 50 is the top tabs area, need to hard code this once added it in 

    def draw_text_to_surf(self, text:str, pos:tuple[int|float, int|float], surf:pg.Surface, colour=DARKGREY, font_size=16, want_return=False, font="bohemian"):
        """ the actual blit for this instance's .image surface is executed in draw_tab_to_pc """
        # -- obvs will add functionality for font and font size at some point, just is unnecessary rn --
        if font == "bohemian":
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
        # -- lato --
        elif font == "lato":
            if font_size == 12:
                text_surf = self.game.FONT_LATO_12.render(f"{text}", True, colour) 
            if font_size == 16:
                text_surf = self.game.FONT_LATO_16.render(f"{text}", True, colour) 
            elif font_size == 20:
                text_surf = self.game.FONT_LATO_20.render(f"{text}", True, colour)
            elif font_size == 26:
                text_surf = self.game.FONT_LATO_26.render(f"{text}", True, colour)
            elif font_size == 32:
                text_surf = self.game.FONT_LATO_32.render(f"{text}", True, colour)
        # -- --
        resulting_rect = surf.blit(text_surf, pos) 
        # -- return the resulting rect (pos & size) if you ask... nicely -- 
        if want_return:
            return resulting_rect

    def get_tab_name(self):
        if isinstance(self, New_Orders_Tab):
            return "New Orders"
        elif isinstance(self, Preparing_Orders_Tab):
            return "Preparing Orders"
                
    def wipe_surface(self):
        self.set_bg_colour()              
    
    def set_bg_colour(self):
        if isinstance(self, New_Orders_Tab):
            self.image.fill(TABBLUE)
        elif isinstance(self, Preparing_Orders_Tab):
            self.image.fill(GOOGLEMAPSBLUE)


# ---- Browser Tab Child Classes ----

class New_Orders_Tab(Browser_Tab):
    def __init__(self, game): 
        super().__init__(game)
        # -- new - current order sidebar --
        # -- declare vars to store lists of orders --
        self.sidebar_order_1 = {1:"Grilled Charmander", 2:"Nuka Cola", 3:"Mario's Mushroom Soup", 4:"Squirtle Sashimi", 5:"Exeggcute Fried Rice"} # 6:"Mario's Mushroom Soup", 7:"Squirtle Sashimi", 8:"Large Exeggcute Fried Rice", 9:"Squirtle Sashimi", 10:"Large Exeggcute Fried Rice"
        self.sidebar_order_2 = {1:"Mario's Mushroom Soup", 2:"Squirtle Sashimi", 3:"Exeggcute Fried Rice"}
        self.sidebar_order_3 = {}
        # -- new - sidebar order details --
        # -- again obvs will refactor this into one dictionary but since just adding this functionality in from scratch using this temp dict instead of updating the og dict variables --
        # quantity only will do for now lol
        self.sidebar_order_1_details = {"Grilled Charmander":{"quantity":1}, "Nuka Cola":{"quantity":1}, "Mario's Mushroom Soup":{"quantity":1}, "Squirtle Sashimi":{"quantity":1}, "Exeggcute Fried Rice":{"quantity":1}} 
        self.sidebar_order_2_details = {"Mario's Mushroom Soup":{"quantity":2}, "Squirtle Sashimi":{"quantity":2}, "Exeggcute Fried Rice":{"quantity":3}}
        self.sidebar_order_3_details = {}
        # -- create the surface for the orders sidebar -- 
        self.width_offset = 90 # if this is set to zero then the sidebar will take exactly half the screen size, if set to 100 it will be -100px from the width and +100px in x axis 
        self.orders_sidebar_surf = pg.Surface(((self.rect.width / 2) - self.width_offset, self.rect.height))
        self.orders_sidebar_surf_colour = WHITE
        self.orders_sidebar_surf.fill(self.orders_sidebar_surf_colour)
        # -- for tracking the active order --
        self.active_order_number = 1
        # -- first test implementation of menu items --
        # -- should put this into settings btw --
        self.menu_items_dict = {1:{"name":"Grilled Charmander", "price":7.99, "my_id":1, "course":"main", "image":self.game.meal_icon_1, "has_toggles":True, "toggles":[("medium",0), ("spicy",0)]},
                                2:{"name":"Squirtle Sashimi", "price":9.49, "my_id":2, "course":"main", "image":self.game.meal_icon_2, "has_toggles":False},
                                3:{"name":"Exeggcute Fried Rice", "price":9.49, "my_id":3, "course":"noodles_rice", "image":self.game.meal_icon_3, "has_toggles":True, "toggles":[("large",2.50), ("regular",0)]},
                                4:{"name":"Nuka Cola", "price":3.15, "my_id":4, "course":"drinks", "image":self.game.meal_icon_4, "has_toggles":True, "toggles":[("large", 1.75),("regular", 0),("quantum", 3), ("classic", 0)]},
                                5:{"name":"Mario's Mushroom Soup", "price":4.29, "my_id":5, "course":"starter", "image":self.game.meal_icon_5, "has_toggles":False}}
        # -- ik, should be one dict, will refactor the dicts in future to encompass this, course, etc, just adding in it like this for now - also mays well bang it in settings tbf --
        self.menu_items_price_dict = {"Grilled Charmander":self.menu_items_dict[1]["price"],
                                        "Squirtle Sashimi":self.menu_items_dict[2]["price"],
                                        "Exeggcute Fried Rice":self.menu_items_dict[3]["price"],
                                        "Nuka Cola":self.menu_items_dict[4]["price"],
                                        "Mario's Mushroom Soup":self.menu_items_dict[5]["price"]}
        self.menu_items_course_dict = {"Grilled Charmander":self.menu_items_dict[1]["course"],
                                        "Squirtle Sashimi":self.menu_items_dict[2]["course"],
                                        "Exeggcute Fried Rice":self.menu_items_dict[3]["course"],
                                        "Nuka Cola":self.menu_items_dict[4]["course"],
                                        "Mario's Mushroom Soup":self.menu_items_dict[5]["course"]}
        self.menu_items_img_dict = {"Grilled Charmander":self.menu_items_dict[1]["image"],
                                        "Squirtle Sashimi":self.menu_items_dict[2]["image"],
                                        "Exeggcute Fried Rice":self.menu_items_dict[3]["image"],
                                        "Nuka Cola":self.menu_items_dict[4]["image"],
                                        "Mario's Mushroom Soup":self.menu_items_dict[5]["image"]}                                    
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
        # -- [new!] - default width for drawing the dynamic highlight menu item to active order on crud action --
        self.crud_highlight_width = 250

    def draw_basket_total_cost_bar(self):
        """ draws the order total sticky surf on the orders sidebar, positioned on top of the sticky bottom surf """
        # -- dimensions setup --
        self.sidebar_sticky_bottom_basket_cost_height = 80
        self.sidebar_sticky_bottom_basket_cost_width = self.orders_sidebar_surf.get_width()
        # -- 
        y_pos = self.rect.height - self.sidebar_sticky_bottom_surf_height - self.sidebar_sticky_bottom_basket_cost_height
        # -- create our new surf --
        self.sidebar_sticky_bottom_basket_cost_surf = pg.Surface((self.sidebar_sticky_bottom_basket_cost_width, self.sidebar_sticky_bottom_basket_cost_height))
        self.sidebar_sticky_bottom_basket_cost_surf.fill(self.orders_sidebar_surf_colour) 
        # -- draw orange bg --
        bg_rect = pg.Rect(0, 0, self.sidebar_sticky_bottom_basket_cost_width, self.sidebar_sticky_bottom_basket_cost_height)
        pg.draw.rect(self.sidebar_sticky_bottom_basket_cost_surf, ORANGE, bg_rect)
        # -- create subtotal subtitle surf --
        basket_total_subtitle_surf = self.game.FONT_LATO_16.render(f"subtotal", True, GREYGREY) 
        # -- create subtotal text surf -- 
        basket_total_text_surf = self.game.FONT_LATO_20.render(f"${self.current_basket_total:.2f}", True, WHITE) 
        # -- draw the text and subtitle surfaces to the sticky bottom basket surf -- 
        self.sidebar_sticky_bottom_basket_cost_surf.blit(basket_total_subtitle_surf, (20,19))
        self.sidebar_sticky_bottom_basket_cost_surf.blit(basket_total_text_surf, (20,37))
        # -- then blit the sidebar sticky bottom surf to the sidebar surf above the other bottom order x basket selector / send to customer sticky bar, and save the resulting rect -- 
        self.sidebar_sticky_bottom_surf_outline_rect = self.orders_sidebar_surf.blit(self.sidebar_sticky_bottom_basket_cost_surf, (0, y_pos))
        # -- [new!] --
        bg_rect = self.sidebar_sticky_bottom_surf_outline_rect.copy()
        bg_rect.height += 10
        bg_rect.y -= 10
        x_padding = 10
        self.sidebar_sticky_bottom_surf_outline_rect.width -= 45 # 25 for edge, extra 20 (10 per side) is for padding, and to centralise the border rect
        self.sidebar_sticky_bottom_surf_outline_rect.height -= 20 
        self.sidebar_sticky_bottom_surf_outline_rect.x += x_padding
        self.sidebar_sticky_bottom_surf_outline_rect.y += 10

        # -- [new!] - then blit an outline rect (since im updating the ui so this bar is now the same colour as the bg tho its still sticky - so it could do with some improved visual clarity -- 
        pg.draw.rect(self.orders_sidebar_surf, WHITE, self.sidebar_sticky_bottom_surf_outline_rect, 3, 10)

    def update_basket_total(self):
        # - note - once this functionality is more finalised dont run it all the timem i.e. set once, then reset on CRUD item only
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
            item_quantity = int(order_details_dict[an_order_item]["quantity"])
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


    # [ todo! ] - move these below their 'parent' pls and tidy up that parent (draw_orders_sidebar) more too
    def setup_orders_sidebar(self):
        """ for drawing active order buttons - but just as indicators for now, no on click functionality yet """
        # -- set sidebar sticky bottom surf dimensions and create surface -- 
        self.sidebar_sticky_bottom_surf_height = 140
        self.sidebar_sticky_bottom_surf = pg.Surface((self.orders_sidebar_surf.get_width(), self.sidebar_sticky_bottom_surf_height))
        self.sidebar_sticky_bottom_surf.fill(ORANGE) # CLEANORANGE
        # -- set btn and btn padding dimensions  --
        self.order_number_indicator_btn_size = 40
        self.order_number_indicator_btn_padding = 50

    def draw_active_order_indicators(self):
        """ handle the order number indicator buttons and handle the hover state and colour changes, and the on click functionality too """
        # -- split the sections into 3 quadrants, for each of the 3 buttons (25 is just edge adjustment), then minus the button size from those quadrants so you have the padding on either side added together remaining, then div 2 to get the width of both sides seperately and place the button at the end pos of the first padding rect in the quadrant --    
        btn_increment_pos = (((self.orders_sidebar_surf.get_width() / 3) - 25) - self.order_number_indicator_btn_size) / 2
        # -- then increment over the amount of buttons to move along by a quadrant and draw the button rect centralised within it -- 
        for i in range(1,4):
            # -- setup everything to blit in a loop using just the index pos from the above for loop to do both the image at its current state, plus its dynamic position --
            order_btn_img_1 = self.game.order_btn_1_active_img.copy()
            order_btn_img_2 = self.game.order_btn_2_active_img.copy()
            order_btn_img_3 = self.game.order_btn_3_active_img.copy()
            order_btn_img_1_dull = self.game.order_btn_1_dull_img.copy()
            order_btn_img_2_dull = self.game.order_btn_2_dull_img.copy()
            order_btn_img_3_dull = self.game.order_btn_3_dull_img.copy()
            active_btns_list = [order_btn_img_1, order_btn_img_2, order_btn_img_3] 
            dull_btns_list = [order_btn_img_1_dull, order_btn_img_2_dull, order_btn_img_3_dull] 
            # -- use the index pos of each active and dull image (above) and blit them at incrementing positions based on that index (1,2,3) --
            if self.active_order_number == i:
                order_number_indicator_btn_true_rect = self.sidebar_sticky_bottom_surf.blit(active_btns_list[i-1], (btn_increment_pos + ((i-1) * (self.orders_sidebar_surf.get_width() / 3)), 7))
            else:
                order_number_indicator_btn_true_rect = self.sidebar_sticky_bottom_surf.blit(dull_btns_list[i-1], (btn_increment_pos + ((i-1) * (self.orders_sidebar_surf.get_width() / 3)), 7))
            # -- use the resulting rect we saved and set it to the true pos for mouse collision --
            order_number_indicator_btn_true_rect = self.game.get_true_rect(order_number_indicator_btn_true_rect)
            order_number_indicator_btn_true_rect.move_ip(self.orders_sidebar_surf.get_width() + 180 - 5, self.rect.height - self.sidebar_sticky_bottom_surf_height)
            # -- check for mouse collision on this specific order number indicator --
            if order_number_indicator_btn_true_rect.collidepoint(pg.mouse.get_pos()):
                # [ todo! ] - ideally blit a different image here please, and just dont allow hover (and therefore also click) for the current active order number using the index --
                order_number_indicator_btn_true_rect = self.sidebar_sticky_bottom_surf.blit(active_btns_list[i-1], (btn_increment_pos + ((i-1) * (self.orders_sidebar_surf.get_width() / 3)), 7))
                # -- if clicked a order number indicator, set the selection to be the active order --
                if self.game.mouse_click_up:
                    self.active_order_number = i
                
    def draw_orders_sidebar(self):
        """ """
        # -- setup dimensions and surface for sticky bottom surf and active order indicator buttons --
        self.setup_orders_sidebar()
        self.draw_active_order_indicators()
        # -- handle the add to customer order button -- 
        add_to_customer_btn_width = 300
        add_to_customer_btn_center_pos = int(((self.orders_sidebar_surf.get_width() - 25) - add_to_customer_btn_width) / 2) # now confirmed - the extra 25 **is** the screen edge lol
        # [new!]
        send_to_customer_btn = self.game.send_to_cust_btn_img
        add_to_customer_btn_true_rect = pg.Rect(add_to_customer_btn_center_pos, self.order_number_indicator_btn_size + 25, add_to_customer_btn_width, self.order_number_indicator_btn_size)
        # [new!]
        self.sidebar_sticky_bottom_surf.blit(send_to_customer_btn, (add_to_customer_btn_center_pos, self.order_number_indicator_btn_size + 25))
        # -- add hover and on click functionality -- 
        add_to_customer_btn_true_rect = self.game.get_true_rect(add_to_customer_btn_true_rect)
        add_to_customer_btn_true_rect.move_ip(self.orders_sidebar_surf.get_width() + 180, self.rect.height - self.sidebar_sticky_bottom_surf_height)
        # -- on hover (mouse collide with button true rect) - blit hovered image to clarify change to button state --
        if add_to_customer_btn_true_rect.collidepoint(pg.mouse.get_pos()):
            self.sidebar_sticky_bottom_surf.blit(self.game.send_to_cust_btn_hover_img.copy(), (add_to_customer_btn_center_pos, self.order_number_indicator_btn_size + 25))
            # -- on hover - update state to show popup --
            if self.game.mouse_click_up: 
                self.want_customer_select_popup = True
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
            self.orders_sidebar_surf_colour = VLIGHTGREY 
        else:
            self.orders_sidebar_surf_colour = WHITE
        self.orders_sidebar_surf.fill(self.orders_sidebar_surf_colour)
            
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
                # -- new test addition --
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
            # --
            self.customer_selector_popup_window_surf.blit(self.customer_selector_confirm_btn_surf, (self.customer_selector_popup_window_width - 200 - self.close_btn_padding, self.customer_selector_popup_window_height - 50 - self.close_btn_padding))
            # -------- under construction - mind your head --------
    	    # [ todo-stuff! ]
            if self.customer_select_popup_selected_customer:
                if self.game.mouse_click_up: 
                    
                    # [ new! ] 
                    # -- calculate the true amount of basket items from the quantities --
                    # should probably make this an update type funct btw and actually execute it in update or sumnt maybe, either way make it its own function
                    active_order_details_dict = self.get_active_order_details_dict()
                    basket_total_items = 0 
                    # todo - so actually do this quantity stuff when you do the price stuff too (since assume am looping for that too) - pretty sure actually am already doing it there so just use that self var lol
                    for basket_item_details in active_order_details_dict.values():
                        basket_total_items += basket_item_details["quantity"]
                  
                    # [ new! ] 
                    # temp implementation for sending the finalised customer order details dict to the customer window
                    # - potentially could do the confirm (if the order sent matches the order the given customer wanted) logic implementation there too tbf
                    temp_details_dict_to_send = {"basket_price":self.current_basket_total, "basket_total_items":basket_total_items}

                    # -- now sending with current basket total if we are sending the payment_window msg to the customers message log --
                    self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].add_new_chatlog_msg("api", "payment_window", temp_details_dict_to_send) # think parameters here are - author, msg, details dict (if is payment_window msg)
                    # -- also quickly do the reset for the customers state timer here, tho this particular part of that functionality might get removed or altered in some way --
                    self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].my_customer.reset_ordering_state_timer()
                    
                    # [ newer-new-update! ] 
                    # - so sliding in here quickly to add in the functionality for on click chat, so removing that from here
                    # - and setting this up so it just does what it actually should do and just send the payment window
                    # - will still need to tidy up and deal with all the notes tho

                    # [ note! ] 
                    # - i think actually at the payment point, it should pause, while its doing the payment and check stuff, then its either going to a new state timer, or this state timer is starting again

                    # -- debug - print the chatlog --
                    print(self.game.chatbox_layer_list[self.customer_select_popup_selected_customer.my_id - 1].my_chatlog)

        # -- then blit the actual popup --
        self.customer_selector_popup_window_true_rect = self.image.blit(self.customer_selector_popup_window_surf, (int((self.rect.width - self.customer_selector_popup_window_width) / 2), int((self.rect.height - self.customer_selector_popup_window_height) / 2) - 25)) # minus 25 for (half of) the toptab bar which isnt done yet, but is hardcoded so replace the 50 here lol 
        self.customer_selector_popup_window_true_rect = self.game.get_true_rect(self.customer_selector_popup_window_true_rect)
            
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
            # -- get the quantity from the new active order details dict --
            order_details_dict = self.get_active_order_details_dict()
            item_quantity = order_details_dict[an_item]["quantity"]
            # -- now also grabbing other info too, reeeally glad i preset this up as a dict now lol --
            item_course = self.menu_items_course_dict[an_item]   
            # -- also image too --         
            item_img = self.menu_items_img_dict[an_item]            
            # -- setup the bg fading alpha rect on crud a new item to the active order --
            crud_highlight_height = 30
            crud_highlight_bg_rect = pg.Rect(60 - 5, 90 + (index * 50) + self.orders_sidebar_scroll_y_offset - 7, self.crud_highlight_width, crud_highlight_height) # have done -5 in x and y as this is just the text pos (ok nudging a bit more in the y tho)
            crud_hightlight_bg_surf = pg.Surface((self.crud_highlight_width, crud_highlight_height)).convert_alpha() # doing a now too surf as want the transparency
            crud_hightlight_bg_surf.fill(ORANGE)
            # -- [new!] - yum text img test --
            self.yum_text = self.game.yum_test_img.copy()
            self.yum_text = pg.transform.rotate(self.yum_text, 15)
            # --
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
                    # -- [new!] - yum alpha --
                    crud_hightlight_bg_surf.set_alpha(self.fading_alpha) 
                    yum_alpha = (self.fading_alpha * 3) 
                    self.yum_text.set_alpha(yum_alpha)
                    # -- the fading bg blit --
                    self.crud_highlight_bg_true_rect = crud_highlight_bg_rect.copy()
                    self.crud_highlight_bg_true_rect.x += 10
                    self.orders_sidebar_surf.blit(crud_hightlight_bg_surf, crud_highlight_bg_rect)
                    # -- blit yum test --
                    crud_highlight_bg_rect.x += crud_hightlight_bg_surf.get_width() - 20
                    crud_highlight_bg_rect.y -= 30
                    # -- yum resizing --
                    dynamic_width = self.yum_text.get_width()
                    dynamic_height = self.yum_text.get_height()
                    offset = (self.fading_alpha - 80) * -1 # flip our decrement var to increment instead 
                    true_offset = float(f"1.{offset + 10}") # use our new increment var to increase the yum text size by a fixed amount (x1.10 to x1.80)
                    dynamic_width *= true_offset
                    dynamic_height *= true_offset
                    self.yum_text = pg.transform.scale(self.yum_text, (dynamic_width, dynamic_height))
                    if true_offset < 1.6: # drags a bit so cut the animation early
                        self.orders_sidebar_surf.blit(self.yum_text, crud_highlight_bg_rect)

            # [ new! ]
            # -- drawing info and icons for each menu item --
            order_sidebar_items_start_pos_y = 100
            order_sidebar_items_y_offset = 65
            order_sidebar_items_start_pos_x = 72

            # -- draw course tag --
            # def draw_course_tag(self):
            formatted_course = item_course.replace("_", " & ")
            item_course_tag_text = self.game.FONT_LATO_REGULAR_12.render(f"{formatted_course}", True, BLACK) 
            item_course_tag_container_width = item_course_tag_text.get_width()
            item_course_tag_container_height = item_course_tag_text.get_height()
            item_course_tag_rect = pg.Rect(order_sidebar_items_start_pos_x, order_sidebar_items_start_pos_y + (index * order_sidebar_items_y_offset) + self.orders_sidebar_scroll_y_offset - 20, item_course_tag_container_width + 8, item_course_tag_container_height + 3) # 8 and 3 just nudge padding to centralise
            resulting_rect = pg.draw.rect(self.orders_sidebar_surf, YELLOW, item_course_tag_rect, 0, 3)
            resulting_rect.x, resulting_rect.y = resulting_rect.x + 4, resulting_rect.y + 2 
            self.orders_sidebar_surf.blit(item_course_tag_text, resulting_rect)

            # -- draw meal icon --
            # def draw_meal_icon(self):
            self.orders_sidebar_surf.blit(item_img, (15, order_sidebar_items_start_pos_y + (index * order_sidebar_items_y_offset) + self.orders_sidebar_scroll_y_offset - 25)) # extra minus 5 to centralise img
            

            # -- finally, end each item in the active order in the for loop by drawing its name and quantity to the orders sidebar surf --
            self.draw_text_to_surf(f"{item_quantity}x {an_item}", (order_sidebar_items_start_pos_x, order_sidebar_items_start_pos_y + (index * order_sidebar_items_y_offset) + self.orders_sidebar_scroll_y_offset), self.orders_sidebar_surf, colour=ORANGE, font_size=16, font="lato")
       

        # [ todo-? ] 
        # -- make this a draw title function now, and fix the below double blit --
        # - note actually also just fix the rect to be a standard rect like the bottom bar instead of just just the small rect behind the text
        # - note, do this title draw after drawing the scrolling text since it has a bg rect now as we want it to be on the bottom 
        order_basket_title_true_rect = self.draw_text_to_surf(f"order {self.active_order_number} basket", (20, 20), self.orders_sidebar_surf, want_return=True, font_size=32, font="lato") 
        pg.draw.rect(self.orders_sidebar_surf, self.orders_sidebar_surf_colour, order_basket_title_true_rect)

        # [ new! ]
        # -- adding little underline rect to the 'order X basket' title --
        # - again the kind of thing that would be a good function
        # - draw underline, and just use the actual text rect and size to dynamically dictate the pos and size of the underline bar, and then just pass a colour or sumnt like that (and ig adjustments to size or pos, e.g. bigger, smaller, closer, further)
        # - may actually refactor this whole thing for a week in 2 weeks time tbf, just to see how clean i can get it
        title_underline_rect = pg.Rect(order_basket_title_true_rect.x, order_basket_title_true_rect.y + order_basket_title_true_rect.height, order_basket_title_true_rect.width, 3)
        pg.draw.rect(self.orders_sidebar_surf, ORANGE, title_underline_rect) # CLEANGREY

        # -- yes legit have to fix this to not do this blit twice - do it twice to get the size, can actually just alter that function to not blit and just return, bosh -- 
        self.draw_text_to_surf(f"order {self.active_order_number} basket", (20, 20), self.orders_sidebar_surf, colour=ORANGE, font_size=32, font="lato") 
        # -- check for mouse actions like click and hover --
        self.check_hover_menu_item()        
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
            self.draw_text_to_surf(f"{an_item_dict['name']} ${item_price}", (10, 15), menu_item_surf, font_colour, font="lato") # now includes price
            # -- new consideration - draw buttons for the toggles if it has buttons else just draw one button to add to order -- 
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

                    # [ todo-quickly! ]
                    # -- 100% MAKE THIS A FUNCTION ONCE DONE TESTING! --
                    if self.active_order_number == 1:                    
                        to_add_to_list = self.sidebar_order_1
                    elif self.active_order_number == 2:                    
                        to_add_to_list = self.sidebar_order_2
                    elif self.active_order_number == 3:                    
                        to_add_to_list = self.sidebar_order_3
        
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
                    # -- for triggering bg on crud a menu item to the active orders menu, with fade effect (much wow!) --
                    # so its defo guna have "name" by now since we're doing it after the above dict update stuff
                    self.trigger_active_order_crud_fade = an_item_dict["name"]                    
                    # -- reset the fading alpha --
                    self.fading_alpha = 80         
                    # -- [new!] - make a text surf object from the clicked menu item string, grab its width, and set the crud width so the fading alpha crud surface is dynamic --
                    menu_item_string = an_item_dict["name"]
                    text_surf = self.game.FONT_LATO_16.render(f"8x {menu_item_string} ", True, BLACK)                     
                    self.crud_highlight_width = text_surf.get_width() + 10
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

class Preparing_Orders_Tab(Browser_Tab):
    def __init__(self, game): # < add any specific parameters that you want to pass to the child class here, and then underneath super().__init__()
        super().__init__(game)
        # -- setup scrollable screen dimensions, and then create a filled surface --
        self.scrollable_screen_width = self.rect.width - 50
        self.scrollable_screen_height = 900
        self.scrollable_screen_surf = pg.Surface((self.scrollable_screen_width, self.scrollable_screen_height))
        self.scrollable_screen_surf.fill(WHITE)
        # -- top prep bars container dimensions --
        self.top_prep_bars_bg_container_width = self.scrollable_screen_width 
        self.top_prep_bars_bg_container_height = 400
        # -- prep queue height --
        self.top_prep_prep_queue_height = 150
        # -- inner store prep bars dimensions --
        self.store_prep_bar_width = self.scrollable_screen_width - (20 * 2) # 20 = side padding
        self.store_prep_bar_height = 140
        # -- tab scroll -- 
        self.tab_scroll_offset = 0
        
        # [ new-test! ]
        # - for toggling map popup on and off
        self.map_popup_activated = False


    # ---- Draw, Update ----

    def draw(self):
        if self.is_active_tab:
            # -- setup the sections
            self.create_top_preparing_customers_queue_bar()
            self.create_mid_preparation_flow_bar()
            # -- draw stuff to those sections
            self.draw_new_customer_to_prep_queue()
            # -- blit the actual sections
            self.draw_cust_prep_queue_surf()
            self.draw_stores_container_surf()
            # -- do map stuff
            self.draw_show_map_button() 
            # -- [new!] -- 
            if self.map_popup_activated:
                self.draw_map_popup()          
            # -- finally, blit the main/default scrollable screen surface to this tab image, if it is the active tab --
            self.image.blit(self.scrollable_screen_surf, (25, 0 + self.tab_scroll_offset))
                
    def update(self):
        ...


    # ---- General x Misc ----

    def draw_title(self, surf:pg.Surface, text, pos=(10, 10)):
        """ new implementation to replace the way we are currently doing it in the parent class """
        title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{text}", True, DARKGREY) 
        surf.blit(title, pos)  


    # ---- Create Section Containers To Scrollable Screen Surf ----

    def draw_stores_container_surf(self):
        # -- [new!] - also quickly draw the title here since we're doing this new full screen scrollable surf thing here --
        self.draw_title(self.stores_container_surf, "Stores Prep Queue")
        # - note - need to update the positioning here as have removed the title from this section -
        self.scrollable_screen_surf.blit(self.stores_container_surf, (0, self.top_prep_prep_queue_height))

    def draw_cust_prep_queue_surf(self):
        # -- [new!] - also quickly draw the title here since we're doing this new full screen scrollable surf thing here --
        self.draw_title(self.cust_prep_queue_surf, "Customer Prep Queue")
        # -- blit their container to the scrollable screen surface --
        self.scrollable_screen_surf.blit(self.cust_prep_queue_surf, (0, 0))
        

    # ---- Preparing Customers Queue Top Bar ----  

    def create_top_preparing_customers_queue_bar(self): # considering sticky but probably not now tbf
        # -- create a bg container for the current stores (design with expanding to add more stores in mind) --
        self.cust_prep_queue_surf = pg.Surface((self.top_prep_bars_bg_container_width, self.top_prep_prep_queue_height))
        self.cust_prep_queue_surf.fill(TABBLUE)

    def draw_new_customer_to_prep_queue(self):
        # -- define card dimensions -- 
        self.customer_prep_card_width = 150 # note - should probably move these to init btw
        self.customer_prep_card_height = 110
        # -- setup bottom pos --
        self.bottom_pos = self.top_prep_prep_queue_height - self.customer_prep_card_height
        # -- loop and draw prep queue cards -- 
        for index, (_, a_customer) in enumerate(self.game.all_preparing_customers.items()): # a_customer_id, a_customer
            if a_customer.preparing_substate == "queued":
                # - note - was considering animating these in and sure totally can do but its such a polish thing that dw about it for now at all -
                customer_surf = pg.Surface((self.customer_prep_card_width, self.customer_prep_card_height))
                customer_surf.fill(YELLOW)
                # -- blit their name quickly too just so we know who it is - will improve this in due course obvs --
                text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_12.render(f"{a_customer.my_name}", True, DARKGREY) 
                customer_surf.blit(text_surf, (5, 5))
                # -- do the blit, based on your position/index in the dictionary -- 
                self.cust_prep_queue_surf.blit(customer_surf, (10 + (index * self.customer_prep_card_width) + (10 * index), self.bottom_pos))


    # ---- Stores Preparing Orders Mid Bar (Changed From Top) ----  

    def create_mid_preparation_flow_bar(self): 
        # -- create a bg container for the current stores (design with expanding to add more stores in mind) --
        self.stores_container_surf = pg.Surface((self.top_prep_bars_bg_container_width, self.top_prep_bars_bg_container_height))
        self.stores_container_surf.fill(GOOGLEMAPSBLUE)
        # -- create the inner store preparing orders bar surfaces --
        store_1_prep_bar_surf = pg.Surface((self.store_prep_bar_width, self.store_prep_bar_height)) 
        store_2_prep_bar_surf = pg.Surface((self.store_prep_bar_width, self.store_prep_bar_height)) 
        store_1_prep_bar_surf.fill(TAN)
        store_2_prep_bar_surf.fill(TAN)
        # -- blit those stores to their background container --
        self.stores_container_surf.blit(store_1_prep_bar_surf, (20, 80))
        self.stores_container_surf.blit(store_2_prep_bar_surf, (20, 80 + self.store_prep_bar_height + 20))


    # ---- New Initial Maps Test Stuff ----

    def draw_show_map_button(self):
        # -- setup the btn dimensions and the surface --
        self.show_map_btn_width = 150
        self.show_map_btn_height = 110
        self.show_map_btn = pg.Surface((self.show_map_btn_width, self.show_map_btn_height))
        self.show_map_btn.fill(BLUEMIDNIGHT)
        # -- blit the button and get the true rect for checking mouse collisions -- 
        # - note - this is just blit on top and not to the specific section surfaces, it still scrolls tho its not sticky, and note the minus 20 below here is for padding btw (screen edge has been taken into consideration in the rest of the calculation already)
        self.map_btn_true_rect = self.scrollable_screen_surf.blit(self.show_map_btn, (self.top_prep_bars_bg_container_width - self.show_map_btn_width - 20, 20)) # guna be like the above container height (make that stuff self btw) (dont think i need scroll but i might)
        # -- move the blitted rect to its true position on the screen based on the surface it was itself blit on to --
        self.map_btn_true_rect = self.game.get_true_rect(self.map_btn_true_rect) 
        self.map_btn_true_rect.move_ip(25, 0) # nudge in the x for the border edge which i forgot to include in initial calculations -- 
        # -- not *entirely* ideal to do hover checks in draw, but is completely fine tbf so dw about it --
        if self.map_btn_true_rect.collidepoint(pg.mouse.get_pos()): 
            if self.game.mouse_click_up:
                print(f"Button Click Registed => Show Map")
                self.map_popup_activated = True
                

    # [ here! ] 
    # make it bigger
    # add close btn
    # start doing the actual map stuff oooooo

    # [ todo! ] 
    # should real quick lay down the orders moving to pos 1 (or maybe just there, skip animating for now)
    # and with a given state (requires order_info, timer, etc)

    def draw_map_popup(self): 
        # -- configure the popup bg --
        self.popup_bg_width = self.image.get_width()
        self.popup_bg_height = self.image.get_height()
        self.popup_bg_surf = pg.Surface((self.popup_bg_width, self.popup_bg_height)).convert_alpha()
        self.popup_bg_surf.fill(DARKGREY)
        self.popup_bg_surf.set_alpha(120)
        self.scrollable_screen_surf.blit(self.popup_bg_surf, (0,0))
        # -- configure the main surface --
        x_padding, y_padding = 200, 100
        self.map_popup_width = self.popup_bg_width - x_padding  
        self.map_popup_height = self.popup_bg_height - y_padding
        self.map_popup = self.game.map_test_img_1.copy()
        # -- just a coloured surface version --
        # self.map_popup = pg.Surface((self.map_popup_width, self.map_popup_height))
        # self.map_popup.fill(CUSTOMERTAN)
        # -- draw title text to the popup surf -- 

        title_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"Select A Store To Start Preparing This Order", True, BLACK) 
        title_bg_surf = pg.Surface((title_text_surf.get_width(), title_text_surf.get_height()))
        title_bg_surf.fill(WHITE)
        self.map_popup.blit(title_bg_surf, (10, 10)) 
        self.map_popup.blit(title_text_surf, (10, 10)) 
        
        # # -- new test for close button --
        self.close_btn_size = 30
        self.close_btn_padding = 20
        self.close_btn_surf = pg.Surface((self.close_btn_size, self.close_btn_size))
        self.close_btn_surf.fill(RED)
        self.close_btn_true_rect = self.map_popup.blit(self.close_btn_surf, (self.map_popup_width - self.close_btn_size - self.close_btn_padding, self.close_btn_padding)) 
        # -- close button true rect for mouse collision --
        self.close_btn_true_rect = self.game.get_true_rect(self.close_btn_true_rect)
        self.close_btn_true_rect.move_ip(x_padding / 2, (y_padding / 2) - self.close_btn_size)
        # -- if click close btn --
        if self.close_btn_true_rect.collidepoint(pg.mouse.get_pos()):
            # -- close this popup -- 
            if self.game.mouse_click_up: 
                self.map_popup_activated = False

        # [new!]
        # - super duper temp implementation for now, just click one store btn to validate -
        self.store_btn_size = 30 
        self.store_btn_surf = pg.Surface((self.store_btn_size, self.store_btn_size))
        self.store_btn_surf.fill(BLUEGREEN)
        self.store_btn_true_rect = self.map_popup.blit(self.store_btn_surf, (120, 220)) 
        self.store_btn_true_rect = self.game.get_true_rect(self.store_btn_true_rect)
        self.store_btn_true_rect.move_ip(x_padding / 2, (y_padding / 2) - self.store_btn_size)
         # -- if click this temp store btn --
        if self.store_btn_true_rect.collidepoint(pg.mouse.get_pos()):
            # -- close this popup and activate... (ig will be substate stuff tbf) -- 
            if self.game.mouse_click_up: 
                self.map_popup_activated = False
                # -- obvs will pass the selected customer, this is just temp as i wanna test out the functionality, simply set the pos 0 cust in the preparing dict to active on click (instead of actually selecting one)
                next_preparing_customer = list(self.game.all_preparing_customers.values())[0]
                next_preparing_customer.preparing_substate = "at_store_1"

        # self.close_btn_true_rect.move_ip(int((self.rect.width - self.customer_selector_popup_window_width) / 2), int((self.rect.height - self.customer_selector_popup_window_height) / 2) - 25)
        # if self.close_btn_true_rect.collidepoint(pg.mouse.get_pos()): 
        #     # -- on hover change colour for visual clarity, ux is good mkay -- 
        #     self.close_btn_surf.fill(DARKRED)
        #     self.customer_selector_popup_window_surf.blit(self.close_btn_surf, (self.customer_selector_popup_window_width - self.close_btn_size - self.close_btn_padding, self.close_btn_padding)) 
        #     # -- on click, set the state to close the popup window --
        #     if self.game.mouse_click_up: 
        #         self.want_customer_select_popup = False
        #         # -- new test addition --
        #         self.customer_select_popup_selected_customer = False # and reset this var
        
        # -- final blit -- 
        self.scrollable_screen_surf.blit(self.map_popup, ((x_padding / 2) - 25, (y_padding / 2) - 25)) # minus 25 for screen edge/border btw # - old centralised position just incase decide to update the gui for this idea - # self.scrollable_screen_surf.blit(self.map_popup, ((self.image.get_width() - self.map_popup_width - 50) / 2, (self.image.get_height() - self.map_popup_height - 25)))         

        # # -- then blit the actual popup --
        # self.customer_selector_popup_window_true_rect = self.image.blit(self.customer_selector_popup_window_surf, (int((self.rect.width - self.customer_selector_popup_window_width) / 2), int((self.rect.height - self.customer_selector_popup_window_height) / 2) - 25)) # minus 25 for (half of) the toptab bar which isnt done yet, but is hardcoded so replace the 50 here lol 
        # self.customer_selector_popup_window_true_rect = self.game.get_true_rect(self.customer_selector_popup_window_true_rect)
            

    # new update notes
    # ----------------
    # so thinking...
    # - we will handle preparing here in some way
    # - this will show some basic stats about current orders also ?
    # - when preparing state is finished, we'll move the customer to the next delivering stage from here too (thats what im guna mock up now)
    # - yeahhhh duhhhhh
    # - so you've completed the order, now the actual first thing to do is choose the store for it to start preparing
    # - the first thing on this tab should be a vertical list of orders moving thru as they start preparing and their time 
    #   - maybe have 2 bars 1 for each store, and stuff at the end is done, kinda like those pizza ovens, it moves thru and then its ready to go out
    # - and then when stuff is done you can move it to the delivered page and handle it there (or it does it itself whatever)
    

    # [rn]
    # - replace chats with order x customer x etc
    # - just do one button 
    # - to open this map functionality stuff
    # - and ig just start setting that up
    # - and then also doing sumnt for 



# ---- End of File ----
