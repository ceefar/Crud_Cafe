# -- imports --
import pygame as pg
from random import choice
from settings import *
vec = pg.math.Vector2


class Customer(pg.sprite.Sprite): # note: consider making this an Object not a Sprite
    def __init__(self, game):
        self.groups = game.customers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- general stuff -
        self.my_id = len(game.customers) # will start at 1
        self.customer_state = "inactive" # active or completed or cancelled
        self.chatbox_state = choice(["shelved","opened"]) # opened or shelved, have them start shelved - only relevant when customer is active (for now anyways) 
        self.my_name = choice(["James","Jim","John","Jack","Josh","Tim","Tom","Jonathon","Abu","Steve","Carl","Mike","Brian"])
        self.my_name += " " + choice(["A","B","C","D","E","F","G","H","I","J","K","L"]) # add a display id - e.g KX139 or sumnt (have it be zones or sumnt but its slightly obscure so you dont twig it for a while, maybe like EWSN for cardinal directions)
        self.my_pinboard_timer_img = self.game.scene_pinboard_paper_image.copy()
        # -- note - only just started implementing this properly, the plan is to port a lot of vars from other classes over here once i figure out how the bulk of the functionality and objects all fit together --

    def __repr__(self):
        return f"Customer ID.{self.my_id} : {self.my_name}"


    def wipe_customer_timer_img(self):
        ...
        # self.my_pinboard_timer_img = 


    def draw_customer_timer_info_to_pinboard(self):
        """ for drawing the customer timer bg surface, plus the info drawn on that surface, to the pinboard scene surface """
        # -- positions and dimensions setup --
        first_pinboard_y_pos = 260
        pinboard_border_width = 12 # put this stuff in settings once configured 
        customer_timer_container_rect = pg.Rect(pinboard_border_width + 10, first_pinboard_y_pos + (20 * self.my_id - 1) + (70 * self.my_id - 1), self.my_pinboard_timer_img.get_width(), self.my_pinboard_timer_img.get_height()) # trying 260/270/280 as width is 280 proper, but with 12 12 border outside is 304 total
        self.draw_text_to_customer_timer_img(f"{self.my_name}")
        # -- the actual blit for this customers timer image container on to the pinboard scene surface - note only drawing 3 max for now me thinks (not implemented tho btw) --
        self.game.pinboard_image_surf.blit(self.my_pinboard_timer_img, customer_timer_container_rect)
 

    def draw_text_to_customer_timer_img(self, text, font_size=16, pos:tuple[int|float, int|float]|vec = (0, 0)):
        """ draw any text to a given position on this customers pinboard timer container/surface/image """
        # -- create the text surface --
        if font_size == 16:
            title = self.game.FONT_BOHEMIAN_TYPEWRITER_16.render(f"{text}", True, BLACK) 
        # -- blit the text surface to this customers pinboard timer img
        self.my_pinboard_timer_img.blit(title, pos) # nudging abit for screen width vs minimise btn pos & width to get visually appealing center pos for the title text
        




        # so remember this needs stuff like new timer and existing state to be on point
        # - obvs add the new self timer var
        #   - then tomo consider a refactor for getter/setter or sumnt idk yet but have a better think lol

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

    def draw_window_border_and_name(self):
        # -- simple switch to set the border img vs its hover state --
        if self.image_state == "normal":
            self.window_border_img = self.game.window_border_img.copy()
        elif self.image_state == "hl1":
            self.window_border_img = self.game.window_border_hl_1_img.copy()
        elif self.image_state == "hl2":
            self.window_border_img = self.game.window_border_hl_2_img.copy()
        # -- blit the border, bilt the name --
        self.image.blit(self.window_border_img, (0,0)) 
        self.draw_name_to_chatbox()


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
            self.image_state = "hl2"
        elif self.is_hovered:
            self.image = self.game.window_hl_1_img.copy() 
            self.image_state = "hl1"
        else: 
            self.image = self.game.window_img.copy()
            self.image_state = "normal"


    # -- New Chat Message Initial Test Stuff --

    def draw_payment_element(self, pos, order_details:dict): # {"price": 18.99}
        payment_pending_img = self.game.payment_pending_1_img.copy()
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
        self.image.blit(payment_pending_img, pos)
        # note - will want a handler function that will sort all the different payment plus associated sprite animation states

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
            for i, a_chatlog_item in enumerate(self.my_chatlog):
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
# -- End Chatbox Class --


