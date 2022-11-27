# -- imports --
import pygame as pg
from random import choice, randint, uniform
from settings import *
vec = pg.math.Vector2


class Customer(pg.sprite.Sprite): # note: consider making this an Object not a Sprite
    # -- note - i've only just started implementing this after laying other foundations (i.e. chatbox, tabs, ui, etc), the plan is to port a lot of vars from other classes over here once i figure out how the bulk of the functionality and objects all fit together --
    def __init__(self, game):
        self.groups = game.customers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- general stuff --
        self.my_id = len(game.customers) # will start at 1
        self.customer_state = "inactive" # active or inactive, the main state - note -> completed and cancelled customers are also inactive
        self.chatbox_state = "shelved" # "shelved" or "opened", have them start shelved - only relevant when customer is active (for now anyways) 
        self.my_name = choice(["James","Jim","John","Jack","Josh","Tim","Tom","Jonathon","Abu","Steve","Carl","Mike","Brian"])
        self.my_name += " " + choice(["A","B","C","D","E","F","G","H","I","J","K","L"]) # add a display id - e.g KX139 or sumnt (have it be zones or sumnt but its slightly obscure so you dont twig it for a while, maybe like EWSN for cardinal directions)
        
        # [ new! ]
        # -- customer timer sidebar initial test stuff -- 
        self.my_pinboard_timer_img = self.game.scene_pinboard_paper_image.copy()
        self.pinboard_timer_width = self.my_pinboard_timer_img.get_width()
        self.pinboard_timer_height = self.my_pinboard_timer_img.get_height()

        # [ new! ]
        # -- customer sub states --
        self.my_active_sub_state = False # ordering, preparing, delivery
        self.my_inactive_sub_state = "inactive" # for when in the inactive state, either inactive, completed or cancelled - with inactive being the default, standard state when you are initially created (with ur homies) at the start of the level

        # [ new! ]
        # -- customer state timers and traits --
        # -- note - each instance gets their own seperate timer, which is created for them once they are activated, and then moved into each state x sub-state --
        self.ordering_sub_state_timer = False 
        # -- note - during the ordering process if the customer is ever left alone for too long they will drop off and cancel --
        # -- give our customer some basic rng personality traits which affect how they interact with the player, will want to expand this at some point --
        self.customer_trait_schedule = choice(["busy","average","lazy"])
        # note - can hardcode these, even at the top of here tbf, or even as class vars, or settings or whatever, also at some point will generally improve this - 
        # also note - using shortened timers for testing, and havent tested balance for ideal/wanted timers yet either but first test cases are commented out below
        state_timer_cancel_times = {"ordering":{"busy":10, "average":20 ,"lazy":30}, "preparing":{}, "delivering":{}}  # 20 30 60?
        # state_timer_cancel_times = {"ordering":{"busy":2, "average":5 ,"lazy":10}, "preparing":{}, "delivering":{}} 
        # -- set the ordering times now just as its easier, tho once get all this stuff added in will put these in handler functions --
        self.customer_order_cancel_time = state_timer_cancel_times["ordering"][self.customer_trait_schedule]

        # [ new! ]
        # -- additional substate for preparing --
        self.preparing_substate = False

        # [ new! ]
        # -- new super duper test implementation of customers actual order, the one that they will read out (with ocassional mistakes that the player will have to get correct at the end) --
        if self.my_id % 2 == 0:
            self.my_wanted_order_details = {"Grilled Charmander":{"quantity":1}, "Nuka Cola":{"quantity":1}, "Mario's Mushroom Soup":{"quantity":1}, "Squirtle Sashimi":{"quantity":1}, "Exeggcute Fried Rice":{"quantity":1}} 
        else:
            self.my_wanted_order_details = {"Mario's Mushroom Soup":{"quantity":2}, "Squirtle Sashimi":{"quantity":2}, "Exeggcute Fried Rice":{"quantity":3}}

        # [ new! ]
        # -- kinda temp, but keeping the functionality - for handling payment state after sending the payment window to a customer  --
        self.has_customer_paid = False
        self.customer_payment_timer = 0 # times in ticks
        self.customer_payment_wait_time = 200 # ticks

        # [ new! ]
        # - test for rotation -
        self.rot_ticker = 1

    def __repr__(self):
        return f"{self.my_name} [ ID.{self.my_id} ]"


    # [ new! ]
    # -- Payment Handling --

    # - will be some additional functionality added to this shortly, this is just the basics -
    def handle_customer_payment(self):
        if not self.has_customer_paid:
            if self.customer_payment_timer > self.customer_payment_wait_time:
                self.has_customer_paid = True
                print(f"{self.customer_payment_timer = }")
        if self.has_customer_paid:
            # -- reset vars --
            self.customer_payment_time = False 
            self.ordering_sub_state_timer = False
            # -- update the players state --
            self.update_activate_customer_substate()


    def activate_payment_timer(self): 
        """ times up in ticks - so really is a counter not a timer, but you get it anyway """
        self.customer_payment_timer += 1


    # -- State & Timer Handling --

    def update_activate_customer_substate(self):
        """ run this when we set the state to active from inactive
        and then (shortly) when updating the state from ordering to preparing, preparing to delivering, and maybe delivering to inactive + inactive_substate completed
        ------
        - ordering
        - preparing
        - delivering
        """
        # -- first if is for when we move from the inactive state, to being activated in the level, currently set to button press 1 --
        if self.my_active_sub_state == False:
            self.my_active_sub_state = "ordering"
            # -- [new!] - also add us to this new customer info pinboard sidebar timer blit tracker --
            self.game.customer_sidebar_queue[self.my_id] = self
            # -- start this customers ordering timer --
            self.activate_ordering_state_timer()
        elif self.my_active_sub_state == "ordering":
            self.my_active_sub_state = "preparing"
            # [new!]
            # -- remove from the all_ordering_customers dict here --
            del self.game.all_ordering_customers[self.my_id] 
            # [new!]
            # -- update the preparing substate --
            self.preparing_substate = "queued"
        elif self.my_active_sub_state == "preparing":
            self.my_active_sub_state = "delivering"
        elif self.my_active_sub_state == "delivering":
            # -- once moving from delivered to a new state, unless interjected with cancelled or similar, it will be finished and move to inactive with a completed inactive sub state --
            self.customer_state = "inactive"
            self.my_inactive_sub_state = "completed"

    def activate_ordering_state_timer(self): 
        """ stores the time at which this customer activated this state, if this time minus """
        self.ordering_sub_state_timer = pg.time.get_ticks()

    def reset_ordering_state_timer(self):
        """ each time we interact with the customer we reset this timer, if we dont move them from ordering to preparing before their timer expires fully they becomes cancelled and inactive """
        self.ordering_sub_state_timer = False
        self.ordering_sub_state_timer = pg.time.get_ticks()
        # print(f"\n{self} {self.ordering_sub_state_timer = }\n{self.customer_trait_schedule = }, {self.customer_order_cancel_time = }\n")

    def update(self):
        # -- get the current time this frame --
        state_check_timer = pg.time.get_ticks()
        # if the timer is active, because the customer is in the active state (not inactive)
        if self.customer_state == "active":
            if self.ordering_sub_state_timer:
                # [new!]    
                # if this customers order cancel time has been reached as they havent had a customer interaction in a certain amount of time dictated by their schedule trait
                if state_check_timer - self.ordering_sub_state_timer > (self.customer_order_cancel_time * 1000):
                    self.update_customer_to_cancelled()
            # [ new! ]
            # - this will trigger to paid in the function based on the ticks timer/counter, then invalidate running itself all the time after resetting everything 
            if not self.has_customer_paid:
                self.handle_customer_payment()

    def update_customer_to_cancelled(self):
        """ when a customer cancels an order run this function to break them out of their default flow, make them inactive, and add them to the .game all_cancelled_customers dictionary"""
        self.customer_state = "inactive"
        self.my_inactive_sub_state = "cancelled"
        self.game.all_cancelled_customers[self.my_id] = self
        # -- also reset this timer so we dont keep rerunning this function from update --
        self.ordering_sub_state_timer = False
        # -- and remove them from this dictionary as they arent active anymore --
        del self.game.all_active_customers[self.my_id]
        # -- [new!] - and now also take them out of the new customer sidebar timer blit queue tracker var --
        del self.game.customer_sidebar_queue[self.my_id]
        print(f"UH OH! - customer {self} has cancelled")

    # -- Customer Timer & Pinboard --

    def wipe_customer_timer_img(self):
        """ at the start of each frame create a new, blank customer timer image from a copy of the original """
        self.my_pinboard_timer_img = self.game.scene_pinboard_paper_image.copy()

    def draw_customer_timer_info_to_pinboard(self):
        """ for drawing the customer timer bg surface, plus the info drawn on that surface, to the pinboard scene surface """
        # -- positions and dimensions setup --
        first_pinboard_y_pos = 260
        pinboard_border_width = 12 # put this stuff in settings once configured 
        # -- quick note for this, basically using dynamically offset y positions based the order in the active customers list to blit these timers, and only want 3 to be shown btw but havent added that yet, and again just its the y pos --
        # -- ok so, convert the sidebar queue dictionary to a list, go thru it's id keys (ID:customer) and find this customer (by its id), then get the index of the keyvalue pair in the list converted from the original dictionary --
        position_in_the_queue = list(self.game.customer_sidebar_queue.keys()).index(self.my_id) 
        # -- that gives us the position in the sidebar list, and we will then use that to blit the top three in order, le bosh --
        timer_y_pos_1 = first_pinboard_y_pos + (20 * (position_in_the_queue + 1)) + (70 * (position_in_the_queue + 1)) # plus 1 for offsetting the zero indexing 
        # -- create position rect and draw the customers name to the the surface
        customer_timer_container_rect = pg.Rect(pinboard_border_width + 10, timer_y_pos_1, self.pinboard_timer_width, self.pinboard_timer_height) # trying 260/270/280 as width is 280 proper, but with 12 12 border outside is 304 total
        self.draw_text_to_customer_timer_img(f"{self.my_name}", font_size=14, pos=(18,2))
        # -- [new!] - for drawing the percentage chargebar of time remaining until this customer cancels --
        self.draw_percent_bar_for_state_timer()
        
        # [ new! ]
        # -- image rotation handler test --
        self.timer_rot_handler()
        # [ new! ]
        # -- draw customer emoji/icon --
        self.draw_customer_emoji()
        # -- rotate the image around it center based on how far along the charge/percent bar the customer is -- 
        rotated_img = self.rotate_at_center(self.my_pinboard_timer_img, self.rot)
        # -- the actual blit for this customers timer image container on to the pinboard scene surface - note only drawing 3 max for now me thinks (not implemented tho btw) --
        self.game.pinboard_image_surf.blit(rotated_img, customer_timer_container_rect)
        # self.game.pinboard_image_surf.blit(self.my_pinboard_timer_img, customer_timer_container_rect)
       
    def timer_rot_handler(self):
        # -- loop our rot ticker 1 to 6 --
        if self.rot_ticker >= 6:
            self.rot_ticker = 1
        # -- set rot and img based on this customers wait time chargebar percent --
        if self.rot_ticker == 1:
            if self.bar_percent < 30:
                self.rot = 1
                self.emoji_img = self.game.emoji_1_img.copy()
            elif self.bar_percent < 45:
                self.rot = uniform(-1.0, 1.0)
                self.emoji_img = self.game.emoji_2_img.copy()
            elif self.bar_percent < 60:
                self.rot = uniform(-2.0, 2.0)
                self.emoji_img = self.game.emoji_3_img.copy()
            elif self.bar_percent < 75:
                self.rot = uniform(-3.0, 3.0)
                self.emoji_img = self.game.emoji_4_img.copy()
            else:
                self.rot = uniform(-4.0, 4.0)
                self.emoji_img = self.game.emoji_5_img.copy()
        # -- do this at the end not the start, since we want it to start on 1, not 2 --
        self.rot_ticker += 1

    def draw_text_to_customer_timer_img(self, text, font_size=16, pos:tuple[int|float, int|float]|vec = (0, 0)):
        """ draw any text to a given position on this customers pinboard timer container/surface/image """
        # -- create the text surface --
        # - note - should put this switch in its own function for each font i want, then group those functions in another function, and call that to get the font object you want, can do this in main too 
        if font_size == 12:
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_12.render(f"{text}", True, BLACK) 
        elif font_size == 14:
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_14.render(f"{text}", True, BLACK) 
        elif font_size == 16:
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_16.render(f"{text}", True, BLACK) 
        elif font_size == 18:
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_18.render(f"{text}", True, BLACK) 
        elif font_size == 20:
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_20.render(f"{text}", True, BLACK) 
        elif font_size == 26:
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_26.render(f"{text}", True, BLACK) 
        # -- blit the text surface to this customers pinboard timer img --
        self.my_pinboard_timer_img.blit(title, pos) # nudging abit for screen width vs minimise btn pos & width to get visually appealing center pos for the title text
                
    def draw_percent_bar_for_state_timer(self):
        # -- new addition to update charge spacing for new icon, hard coding it in this way incase want to update or revert or restyle --
        icon_spacing = 60 # try icon size of 50 with 5 padding or 40 with 10
        # -- dimensions --
        timer_bar_max_width = 210 - icon_spacing
        timer_bar_height = 35
        # -- create the timer vars to get the accurate percent of time passed vs time until cancelling --
        state_check_timer = pg.time.get_ticks()
        current_time = state_check_timer - self.ordering_sub_state_timer
        # -- setup percentage chargebar rect --
        self.bar_percent = current_time * (100 / (self.customer_order_cancel_time * 1000)) 
        self.timer_bar_rect = pg.Rect(20 + icon_spacing, 22, self.bar_percent * (timer_bar_max_width / 100), timer_bar_height)
        # [ new! ] 
        # -- dynamic chargebar colouring --
        self.handle_chargebar_rgb()
        # -- draw the chargebar to this customers timer img --
        pg.draw.rect(self.my_pinboard_timer_img, (self.r, self.g, self.b), self.timer_bar_rect)

    def draw_customer_emoji(self):
        """ draw the different emote icons based on the customers wait time chargebar percent, which is set in `self.timer_rot_handler()` """
        self.my_pinboard_timer_img.blit(self.emoji_img, (25, 18))

    def handle_chargebar_rgb(self):
        """ decrement green and increment red based on the current percentage """  
        self.r, self.g, self.b = 1, 255, 1
        self.r = self.r * (self.bar_percent * 2.55)
        self.g = self.g - self.r

    @staticmethod
    def rotate_at_center(image:pg.Surface, angle):
        rotated_image = pg.transform.rotate(image, angle)
        return rotated_image



    # [ new! ]
    # - now adding in emote next to charge/percent bar for customer timer
    #   - grab the old draw outline function for icons?
    # - improve the colour transition so it isnt so icky half way thru
    # - also haved moved the bar to the right a tad to accomodate for the icon  




# -- End Customer Class --

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
        # -- new - for scrolling chat window --
        self.chatbox_window_scroll_y_offset = 0 
        # -- new - chatlog blit stuff --
        self.chatlog_text_msg_height = 45
        self.chatlog_payment_msg_height = 108 
        # -- new - chatlog stuff --
        self.my_chatlog = [] 
        # -- new - for window border img --
        self.window_border_img = self.game.window_border_img.copy()
        # -- new - state addition - note should consider upgrading these (states) shortly --
        self.image_state = "normal"

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
                    # -- drawing chatlog stuff --
                    if self.my_chatlog:
                        self.draw_my_chatlog()
                # -- if this instances has had move mode activated by clicking the top title bar of the window, then move it to the mouse pos, then offset that pos by the (negative btw >) -pc_screen_width and height --
                if self.chatbox_move_activated:
                    self.rect.x, self.rect.y = pg.mouse.get_pos()
                    self.rect = self.get_true_rect(a_rect=self.rect, move_in_negative=True)
                    # -- then to pick it up exactly where the mouse picked it up we do one more offset for the clicked pos minus the true position of the window and add that to the x & y -- 
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


    # -- Functions For Blitting To This Instance's Image --

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
            self.image_state = "hl2"
        elif self.is_hovered:
            self.image = self.game.window_hl_1_img.copy() 
            self.image_state = "hl1"
        else: 
            self.image = self.game.window_img.copy()
            self.image_state = "normal"

    def draw_window_border_and_name(self):
        """ simple switch to set the border img vs the hovered and moving states """
        if self.image_state == "normal":
            self.window_border_img = self.game.window_border_img.copy()
        elif self.image_state == "hl1": # should rename hovered and moving huh XD
            self.window_border_img = self.game.window_border_hl_1_img.copy()
        elif self.image_state == "hl2":
            self.window_border_img = self.game.window_border_hl_2_img.copy()
        # -- blit the outer border img, bilt the name --
        self.image.blit(self.window_border_img, (0,0)) 
        self.draw_name_to_chatbox()


    # [ new! ]
    # -- test stuff for drawing the button to interact with the customer --
    
    def draw_customer_interaction_button(self):
        """ write me plis ceefar """
        if self.my_customer.customer_state == "active":
            if self.my_customer.chatbox_state == "opened":
                # -- setup dimensions and position --
                self.chat_interact_button_width = 120
                self.chat_interact_button_height = 40
                self.chat_interact_button_surf = pg.Surface((120, 40)) 

                # just make this an image now, so doing that just after this quickly...
                self.chat_interact_btn_true_rect = self.image.blit(self.chat_interact_button_surf, (self.opened_chat_width - self.chat_interact_button_width - 15, self.opened_chat_height - self.chat_interact_button_height - 15))

                # ok so get the collide i think you want to just make a rect instead 
                self.chat_interact_btn_true_rect = pg.Rect(self.true_chatbox_window_rect.x, self.true_chatbox_window_rect.y, self.chat_interact_button_width, self.chat_interact_button_height)
                self.chat_interact_btn_true_rect = self.get_true_rect(self.chat_interact_btn_true_rect)

                self.chat_interact_btn_true_rect.move_ip(-self.chat_interact_button_width - 15, 45)

                if self.chat_interact_btn_true_rect.collidepoint(pg.mouse.get_pos()):
                    if self.game.mouse_click_up:
                        
                        # [ new! ]
                        # -- send the customers message when we click their interact button --

                        # temp functionality for now
                        # -- choose a random item from our wanted_order -- 
                        rng = choice(list(self.my_customer.my_wanted_order_details.keys()))
                        # -- add the rng message on clicking the customers interact button
                        self.add_new_chatlog_msg("customer", rng)

                        # [ todo-note! ]
                        # - we wanna be sending a randomised message from us too
                        # - wanna be having that actually blitted on the button (thinking like mass effect, i.e. you actually *say* something different, but the btn says a summarised version)
                        # - and be adding in a slightly randomised response from them each time
                        # - and if not including now ensure you take the whole, making changes to order concept
                        # - also need to do the auto-scrolling to last item thing which will be easy af, could also add a jump to button too but thats just meh extras anyways
                            
                        # -- also reset the ordering state timer now we have interacted with the customer --
                        self.my_customer.reset_ordering_state_timer()
                        # -- note --
                        # - i think actually at the payment point (not here but still), it should pause, while its doing the payment and check stuff, then its either going to a new state timer, or this state timer is starting again


    # -- New Chat Message Initial Test Implementation Stuff --

    def draw_payment_element(self, pos, order_details:dict): # {"price": 18.99}
        # -- [new!] - added in functionality to set the customer to paid after a few seconds 
        if self.my_customer.has_customer_paid:
            payment_pending_img = self.game.payment_success_1_img.copy()
            green_clr = SUCCESSGREEN
        else:
            payment_pending_img = self.game.payment_pending_1_img.copy()
            green_clr = FORESTGREEN
        # -- get the price from the new details dict --
        self.basket_price = float(f"{order_details['basket_price']:.2f}") # set the precision to 2 decimal places
        self.basket_total_items = order_details["basket_total_items"]
        # -- create the text surfaces --
        basket_price_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_26.render(f"${self.basket_price}", True, green_clr)
        basket_total_items_text_surf = self.game.FONT_BOHEMIAN_TYPEWRITER_12.render(f"basket items: {self.basket_total_items}", True, BLACK)
        # -- draw the text surfs to this objects copy of the payment window img 
        payment_pending_img.blit(basket_price_text_surf, (78, 27)) 
        payment_pending_img.blit(basket_total_items_text_surf, (78, 57)) 
        # obvs and then can do the delivery charge stuff here too
        # - even would be cute for them to sometimes stop the transaction because of this but **not** anytime soon
        self.image.blit(payment_pending_img, pos)
        # note - will want a handler function that will sort all the different payment plus associated sprite animation states
        
        # [ new! ]
        # - note, unsure if this will officially be here but just putting it for now while testing anyways
        self.my_customer.activate_payment_timer()

    def add_new_chatlog_msg(self, author:str, msg:str, order_details=None):
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
            # so the last chat entry pos and height are dynamic based on size of the previous entry
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
            for _, a_chatlog_item in enumerate(self.my_chatlog): # note - dont need to enumerate this now?
                a_msg = a_chatlog_item["msg"]
                an_author = a_chatlog_item["author"]
                a_chat_line_y_pos = a_chatlog_item["chat_pos"]
                # -- 
                if "order_details" in a_chatlog_item:
                    order_details = a_chatlog_item["order_details"]
                # --
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

    # -- Functions For Repositioning & Rect Stuff --

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

# -- End Chatbox Class --

