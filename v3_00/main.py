# by Courtney 'Ceefar' Farquharson
# CRUD Cafe Demo App

# Overview
# - - - - - - - 
# - minimise window etc - todo 
# - usage x description x overview - todo
# - current can add new customers and add items to baskets, etc - todo

# Usage
# - - - - - - - 
# Start Game
# - Key: Any

# Add New Customer
# - Key: 1

# Change Tab
# - Key: Q/q

# Cycle Active Basket/Order
# - Key: O/o

# Scroll Window or Order
# - Key: Key_UP, Key_DOWN
# - Notes: 
#   - hover either the chatbox window or the active order in the orders sidebar to scroll the page using the up and down keys
#   - on hover effects :
#       - chatbox window
#           - border highlights green
#       - active order
#           - background colour darkens

# Minimise Window, etc
# - to add here


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# -- imports --
import pygame as pg
import sys
from os import path
from settings import *
from chatbox_and_customer import Chatbox, Customer
from browser_tabs import Browser_Tab, New_Orders_Tab, Preparing_Orders_Tab

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        # -- load folders -- 
        game_folder = path.dirname(__file__)
        imgs_folder = path.join(game_folder, 'imgs')
        fonts_folder = path.join(game_folder, 'fonts')
        audio_folder = path.join(game_folder, 'audio')
        # -- load images -- 
        # - background scene -
        self.scene_img = pg.image.load(path.join(imgs_folder, SCENE_IMG)).convert_alpha() # self.an_img = pg.transform.scale(self.an_img, (140, 140)) # (56, 56))
        # -- scene elements --  
        self.scene_pinboard_image = pg.image.load(path.join(imgs_folder, SCENE_INFO_PINBOARD_IMG)).copy().convert_alpha()  
        self.scene_pinboard_paper_image = pg.image.load(path.join(imgs_folder, SCENE_PINBOARD_PAPER_IMG)).copy().convert_alpha() 
        self.emoji_1_img = pg.image.load(path.join(imgs_folder, SCENE_PINBOARD_ICON_1_IMG)).copy().convert_alpha() 
        self.emoji_2_img = pg.image.load(path.join(imgs_folder, SCENE_PINBOARD_ICON_2_IMG)).copy().convert_alpha() 
        self.emoji_3_img = pg.image.load(path.join(imgs_folder, SCENE_PINBOARD_ICON_3_IMG)).copy().convert_alpha() 
        self.emoji_4_img = pg.image.load(path.join(imgs_folder, SCENE_PINBOARD_ICON_4_IMG)).copy().convert_alpha() 
        self.emoji_5_img = pg.image.load(path.join(imgs_folder, SCENE_PINBOARD_ICON_5_IMG)).copy().convert_alpha() 
        # -- windows --      
        self.window_img = pg.image.load(path.join(imgs_folder, WINDOW_IMG)).convert_alpha()  
        self.window_border_img = pg.image.load(path.join(imgs_folder, WINDOW_BORDER_1_IMG)).convert_alpha()  
        self.window_border_hl_1_img = pg.image.load(path.join(imgs_folder, WINDOW_BORDER_HL_1_IMG)).convert_alpha()  
        self.window_border_hl_2_img = pg.image.load(path.join(imgs_folder, WINDOW_BORDER_HL_2_IMG)).convert_alpha()  
        self.window_hl_1_img = pg.image.load(path.join(imgs_folder, WINDOW_HL_1_IMG)).convert_alpha()  
        self.window_hl_2_img = pg.image.load(path.join(imgs_folder, WINDOW_HL_2_IMG)).convert_alpha()  
        self.window_shelved_1_img = pg.image.load(path.join(imgs_folder, WINDOW_SHELVED_1_IMG)).convert_alpha()  
        self.window_shelved_hl_1_img = pg.image.load(path.join(imgs_folder, WINDOW_SHELVED_HL_1_IMG)).convert_alpha()  
        # -- tab bar elements --
        self.tab_bar_prep_img = pg.image.load(path.join(imgs_folder, TAB_BAR_PREPARING_IMG)).convert_alpha()  
        self.tab_bar_order_img = pg.image.load(path.join(imgs_folder, TAB_BAR_ORDERING_IMG)).convert_alpha()  
        # -- chat elements --
        self.payment_pending_1_img = pg.image.load(path.join(imgs_folder, PAYMENT_PENDING_IMG_1)).convert_alpha()  
        self.payment_success_1_img = pg.image.load(path.join(imgs_folder, PAYMENT_SUCCESS_IMG_1)).convert_alpha()  
        # -- sidebar elements --
        self.send_to_cust_btn_img = pg.image.load(path.join(imgs_folder, SEND_TO_CUST_BTN_IMG)).convert_alpha()  
        # -- map popup --
        self.map_test_img_1 = pg.image.load(path.join(imgs_folder, MAP_TEST_IMG_1)).convert_alpha()  
        # -- load fonts -- 
        self.FONT_TWINMARKER_26 = pg.font.Font((path.join(fonts_folder, "TwinMarker.ttf")), 26) 
        self.FONT_VETERAN_TYPEWRITER_20 = pg.font.Font((path.join(fonts_folder, "veteran typewriter.ttf")), 20) 
        self.FONT_VETERAN_TYPEWRITER_26 = pg.font.Font((path.join(fonts_folder, "veteran typewriter.ttf")), 26) 
        self.FONT_BOHEMIAN_TYPEWRITER_10 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 10)
        self.FONT_BOHEMIAN_TYPEWRITER_12 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 12)
        self.FONT_BOHEMIAN_TYPEWRITER_14 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 14)
        self.FONT_BOHEMIAN_TYPEWRITER_16 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 16)
        self.FONT_BOHEMIAN_TYPEWRITER_18 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 18)
        self.FONT_BOHEMIAN_TYPEWRITER_20 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 20)
        self.FONT_BOHEMIAN_TYPEWRITER_26 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 26)
        self.FONT_BOHEMIAN_TYPEWRITER_32 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 32)
        self.FONT_BOHEMIAN_TYPEWRITER_46 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 46)
        # -- load lato fonts -- 
        self.FONT_LATO_16 = pg.font.Font((path.join(fonts_folder, "Lato-Black.ttf")), 16) 
        self.FONT_LATO_20 = pg.font.Font((path.join(fonts_folder, "Lato-Black.ttf")), 20) 
        self.FONT_LATO_26 = pg.font.Font((path.join(fonts_folder, "Lato-Black.ttf")), 26) 
        self.FONT_LATO_32 = pg.font.Font((path.join(fonts_folder, "Lato-Black.ttf")), 32) 
        # -- define main gui surface dimensions --
        self.pc_screen_surf_width, self.pc_screen_surf_height = 1000, 620
        self.pc_screen_surf_x, self.pc_screen_surf_y = (WIDTH / 2) - (self.pc_screen_surf_width / 2), 100 # testing +15 for tab bar adjustment
        self.tab_bar_height = 50 # the top bar on the pc_screen_surf the emulate browser tabs
        self.pc_screen_surf_true_y = self.pc_screen_surf_y + self.tab_bar_height # else y val doesnt take the tab_bar_height into consideration
        # -- [new!] - preloading core scene gui vars for start screen --
        self.waiting_start = True
        self.waiting_boot = True
        self.pinboard_image_surf = self.scene_pinboard_image.copy()
        self.login_1_img = pg.image.load(path.join(imgs_folder, START_LOGIN_IMG_1)).convert_alpha()  
        self.login_2_img = pg.image.load(path.join(imgs_folder, START_LOGIN_IMG_2)).convert_alpha()  
        self.boot_ticker = 100 # 500 but shorted during development
        # -- [new!] - sound loading and volume tweaking --
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            sound = pg.mixer.Sound(path.join(audio_folder, EFFECTS_SOUNDS[type]))
            sound.set_volume(0.3)
            self.effects_sounds[type] = sound

    def new_level(self):
        """ initialize all variables and do all the setup for a new game """
        # -- customer setup vals --
        self.total_customers_for_level = 4
        self.id_customer_dict = {}
        self.chatbox_layer_list = []
        self.all_active_customers = {} # by layer?! - hmmm, but i think not as layer is a chatbox thing remember!
        # -- groups --
        self.all_sprites = pg.sprite.Group()    
        self.browser_tabs = pg.sprite.Group()
        self.customers = pg.sprite.Group()
        self.chatboxes = pg.sprite.Group()
        # -- initialising sprite object instances -- 
        self.new_orders_tab = New_Orders_Tab(self)
        self.preparing_orders_tab = Preparing_Orders_Tab(self)
        # -- loop customers needed for this level --
        for _ in range(0, self.total_customers_for_level):
            a_customer = Customer(self)
            self.id_customer_dict[a_customer.my_id] = a_customer # store all the customer instances in a list for significantly easier access to them as key value pairs (id:instance)
            a_chatbox = Chatbox(self, a_customer)
            self.chatbox_layer_list.append(a_chatbox) # store all the customer instances in a list for accessing them by layer
        # -- initialise the layers group once the object instances are all added to their respective groups --
        self.chatbox_layers = pg.sprite.LayeredUpdates(self.chatboxes)
        # -- misc game x level setup vars --
        self.is_player_moving_chatbox = False 
        # -- new x misc --
        self.all_cancelled_customers = {} # should move this above
        self.all_ordering_customers = {} # should move this above too
        self.all_preparing_customers = {} # should move this above also
        self.pinboard_pos = (0, 20)   
        self.customer_sidebar_queue = {}  
        self.pinboard_image_surf = self.scene_pinboard_image.copy() 

    def run(self):
        # runs the game loop... thank you for coming to my TEDtalk
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # for Python v2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    
    def render_start_screen(self):
        """ render the start screen... thank you for coming to my TEDtalk """
        self.draw_start()
        want_start = self.wait_for_continue()
        if want_start:
            return True

    def game_over_man_game_over(self):
        """ render the game over screen """
        ...


    # ---- Events, Update, Draw - Executes In That Order ----

    def draw(self):
        pg.display.set_caption(f"Crud Cafe v3.11 - {self.clock.get_fps():.2f}")
        # -- draw the background -- 
        self.screen.blit(self.scene_img, (0, 0)) 
        # -- [new!] - draw to the pinboard image, just basic setup stuff dw too much about the vars n states yet --
        self.write_info_counters_to_pinboard(font_size=46, post_it="ordering")
        self.write_info_counters_to_pinboard(font_size=46, post_it="cancelled")
        self.write_info_counters_to_pinboard(font_size=46, post_it="preparing")
        # -- [new!] - test to for drawing customer info to the pinboard --
        for a_customer in self.all_active_customers.values():
            if isinstance(a_customer, Customer):
                # -- [new!] - adding customers to new all_preparing_customers dictionary --
                if a_customer.my_active_sub_state == "preparing":
                    if a_customer.my_id not in self.all_preparing_customers.keys():
                        self.all_preparing_customers[a_customer.my_id] = a_customer
                # -- [new!] - creating a new ordering version of the above instead of using all_customers for ordering as i was previous --
                if a_customer.my_active_sub_state == "ordering":
                    if a_customer.my_id not in self.all_ordering_customers.keys():
                        self.all_ordering_customers[a_customer.my_id] = a_customer                        
                # -- [new!] - only draw the customers sidebar ordering timer stuff if they have paid, means making an update to the dictionary timers idea since probs dont need that anymore -- 
                if not a_customer.has_customer_paid:
                    a_customer.wipe_customer_timer_img()
                    a_customer.draw_customer_timer_info_to_pinboard()
        # -- [new!] - draw the new info pinboard concept image --
        self.scene_img.blit(self.pinboard_image_surf, self.pinboard_pos)
        # -- wipe the computer screen surface at the start of each frame, we then draw to this surface and then blit it to the screen (without the fill) -- 
        self.wipe_computer_screen_surface()
        # -- [new!] - draw tab bar img --
        self.draw_tab_bar()
        # -- loop tabs --
        for sprite in self.browser_tabs:
            if isinstance(sprite, Browser_Tab): # really for type hinting
                if sprite.is_active_tab:  
                    # -- [new!] - loop all the chatboxes and draw the window border if valid --
                    for a_chatbox_window in self.chatboxes:
                        if isinstance(a_chatbox_window, Chatbox): # purely for type hints
                            # -- [new!] - maybe temp? - if the customer is in the cancelled sub-state (or soon to be `completed` too), then dont blit the chatbox to the screen, by moving its rect off screen --                            
                            if a_chatbox_window.my_customer.customer_state == "inactive":
                                a_chatbox_window.rect = pg.Rect(-500, -500, 0, 0)
                            # -- draw the border for the window, but only if its in the opened state --
                            if a_chatbox_window.my_customer.chatbox_state == "opened": 
                                a_chatbox_window.draw_window_border_and_name()
                                a_chatbox_window.draw_customer_interaction_button()
                    # -- draw the chatbox layers in the correct order on top of one another using ._layer, .image which are self explanitory, & .rect which is for the position -- 
                    self.chatbox_layers.draw(sprite.image)
                    # -- for customer selector popup - has to happen after drawing chatbox layers in order of operations as its a popup, it should be on top of everything else --
                    if isinstance(sprite, New_Orders_Tab):
                        if sprite.want_customer_select_popup:
                            sprite.draw_active_customers_selector_popup()
                    # -- finally, run this for all child instances, if they are they active tab you draw their surface to the scene screen image --                     
                    sprite.draw_tab_to_pc()       
        # -- new first implementation of preparing orders tab & its functionality --
        self.preparing_orders_tab.draw()          
        # -- redraw the screen once we've blit to it, with a rect as a temp faux monitor outline/edge --
        screen_outline_rect = self.screen.blit(self.pc_screen_surf, (self.pc_screen_surf_x, self.pc_screen_surf_y))
        screen_outline_rect.height += 15
        pg.draw.rect(self.screen, DARKGREY, screen_outline_rect, 25) # draws the faux monitor edge around the screen surf               
        # -- finally, flip the display --
        pg.display.flip()

    def update(self):
        """ keep update and draw seperate for best practice, runs before draw() but after events() """
        self.pinboard_image_surf = self.scene_pinboard_image.copy() 
        # -- notable vars to reset every frame --
        self.opened_chatbox_offset_counter = 0
        self.shelved_chatbox_offset_counter = 0
        # -- update the browser tabs first since they are on the bottom -- 
        self.browser_tabs.update()         
        # -- store customers by states --
        for this_customer in self.customers: 
            if isinstance(this_customer, Customer): # purely for type hints
                if this_customer.customer_state == "active":
                    self.all_active_customers[this_customer.my_id] = this_customer
        # -- loop chatboxes to handle states seperately as we may need to break this loop, there won't be enough windows on screen for this ever to be even slightly problematic -- 
        self.hovered_chatbox = False
        for a_chatbox in reversed(self.chatbox_layer_list):
            if isinstance(a_chatbox, Chatbox): # purely for type hints
                if a_chatbox.handle_hover_or_click():
                    self.hovered_chatbox = a_chatbox # save this instance as we will unset the hover for every other instance that isnt this one
                    break
        # -- loop chatboxes to run each instances update - importantly is done this way as increments a counter for offset positions, else would do self.chatboxes.update() --
        for this_chatbox in self.chatboxes:
            if isinstance(this_chatbox, Chatbox): # purely for type hints
                # -- reset the hovered var on all chatbox instances that weren't the hovered one that we saved when we broke out of the loop above earlier -- 
                if this_chatbox != self.hovered_chatbox:
                    this_chatbox.is_hovered = False                    
                this_chatbox.update() 
        # -- then at the end of update reset the chatbox layers to be in the correct order --
        self.reorder_all_window_layers()
        # -- temp new test --
        self.customers.update()

    def events(self):
        """ handle all events here, executes before update() and draw() """
        # -- preset mouse states - these will reset each run through -- 
        self.mouse_click_up = False
        # -- quit event first --
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # -- mouse events - mouse up --
            if event.type == pg.MOUSEBUTTONUP: 
                self.mouse_click_up = True
            # -- keyboard events - key up --
            if event.type == pg.KEYUP:
                # -- temp toggle between our 2 tabs --
                if event.key == pg.K_q:
                    self.new_orders_tab.is_active_tab = not self.new_orders_tab.is_active_tab
                    self.preparing_orders_tab.is_active_tab = not self.preparing_orders_tab.is_active_tab
                    if self.preparing_orders_tab.is_active_tab:
                        self.preparing_orders_tab.tab_scroll_offset = 0
                # -- temporary way to incrememntally make customers active, this will be handled by a game timer in future but this is waaay better for testing --  
                created_customers = len(self.all_active_customers) # the amount of customers you've manually added in already
                # -- handle the exception if we accidentally try to add too many customers than we have available by just skipping over it, in the real game this will basically be the end level state - once the last customer has been completed or cancelled anyways --
                try:
                    if event.key == pg.K_1:
                        # -- activate a new customer by pressing 1 --
                        new_customer = self.id_customer_dict[(created_customers + 1) + len(self.all_cancelled_customers)]
                        new_customer.customer_state = "active"
                        # -- [new!] --
                        new_customer.update_activate_customer_substate()
                except KeyError:
                    pass
                # -- toggle the orders in the orders sidebar --
                if event.key == pg.K_o: # mostly for dev mode / debugging during new order functionality implementation + testing
                    self.new_orders_tab.active_order_number += 1
                    self.new_orders_tab.orders_sidebar_scroll_y_offset = 0 # reset the scroll offset to 0 when we change to another order too
                # -- for tap up/down on keyboard to scroll, depending on the hovered window / surface --
                if event.key == pg.K_UP:
                    self.handle_scroll_up()
                if event.key == pg.K_DOWN:
                    self.handle_scroll_down()
            # -- keyboard events - key down --
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


    # ---- For Main Scene GUI ----

    def wipe_computer_screen_surface(self):
        """ we use this as a base to draw everything on to, it is basically our game surface """
        self.pc_screen_surf = pg.Surface((self.pc_screen_surf_width, self.pc_screen_surf_height))
        self.pc_screen_surf.fill(SKYBLUE) # once setup the actual tab bar, make this black - then will make boot up / boot down animation hella easy

    def draw_tab_bar(self):
        if self.new_orders_tab.is_active_tab:
            self.pc_screen_surf.blit(self.tab_bar_order_img.copy(), (25, 25))
        else:
            self.pc_screen_surf.blit(self.tab_bar_prep_img.copy(), (25, 25))


    # ---- For Pinboard Scene GUI ----

    def write_info_counters_to_pinboard(self, font_size=26, post_it="ordering"):
        """ runs in main draw loop, draw to our background image then draw out background image to the screen every frame """
        # -- preset positions for each post-it area --
        # due to the nail and string at top of the png, the actual part of the image that you want to draw on (the pinboard) starts at y >= 85
        pinboard_y_offset = 85
        ordering_post_it_offset = (50, 7)
        cancelled_post_it_offset = (75, 117)
        preparing_post_it_offset = (135, 12)
        # -- switch to handle each post it value and position seperately --
        if post_it == "ordering":
            # -- handle blit position --
            pos = (self.pinboard_pos[0] + ordering_post_it_offset[0], self.pinboard_pos[1] + pinboard_y_offset + ordering_post_it_offset[1])
            # -- handle font size, will do this properly (i.e. in its own function) shortly --
            if font_size == 26:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_26.render(f"{len(self.all_ordering_customers)}", True, ORDERPOSTITBLUE) 
            elif font_size == 32:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_32.render(f"{len(self.all_ordering_customers)}", True, ORDERPOSTITBLUE) 
            elif font_size == 46:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_46.render(f"{len(self.all_ordering_customers)}", True, ORDERPOSTITBLUE) 
        # -- preparing --
        elif post_it == "preparing":
            pos = (self.pinboard_pos[0] + preparing_post_it_offset[0], self.pinboard_pos[1] + pinboard_y_offset + preparing_post_it_offset[1])
            # -- handle font size, will do this properly shortly --
            if font_size == 26:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_26.render(f"{len(self.all_preparing_customers)}", True, PURPLE) 
            elif font_size == 32:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_32.render(f"{len(self.all_preparing_customers)}", True, PURPLE) 
            elif font_size == 46:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_46.render(f"{len(self.all_preparing_customers)}", True, PURPLE) 
        # -- cancelled --
        elif post_it == "cancelled":
            # -- handle blit position --
            pos = (self.pinboard_pos[0] + cancelled_post_it_offset[0], self.pinboard_pos[1] + pinboard_y_offset + cancelled_post_it_offset[1])
            # -- handle font size, will do this properly shortly --
            if font_size == 26:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_26.render(f"{len(self.all_cancelled_customers)}", True, RED) 
            elif font_size == 32:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_32.render(f"{len(self.all_cancelled_customers)}", True, RED) 
            elif font_size == 46:
                text_surf = self.FONT_BOHEMIAN_TYPEWRITER_46.render(f"{len(self.all_cancelled_customers)}", True, RED) 
        # -- finally do the actually blit -- 
        self.pinboard_image_surf.blit(text_surf, pos)


    # ---- For Reordering Layers ----

    def reorder_all_window_layers(self):
        """ after all windows have been updated, run this to reorder them into a consistent, incrementing integers """
        reorder_counter = 1
        for a_chatbox in self.chatbox_layers:
            if isinstance(a_chatbox, Chatbox):
                if a_chatbox.my_customer.customer_state == "active":
                    pg.sprite.LayeredUpdates.change_layer(self.chatbox_layers, a_chatbox, reorder_counter) 
                    reorder_counter += 1 
        # -- reorder this too since we want the order to be correct here also as we need this list style array for reversed looping + breaking for handling click & hover --         
        self.chatbox_layer_list = list(sorted(self.chatbox_layer_list, key=lambda item: item._layer))

    # -- Use By Most Sprites To Orient Their Hitbox Rect To Their True Position On The Screen vs The PC Screen Tab Surface They Will Have Been Blit To -- 
    def get_true_rect(self, a_rect:pg.Rect, move_in_negative=False):
        """ update a given rect position by offsetting it from the pc_screen x and y pos """
        # should probably make this a .game function when adding new classes as they will likely use it too
        moved_rect = a_rect.copy()
        if move_in_negative:
            moved_rect.move_ip(-self.pc_screen_surf_x, -self.pc_screen_surf_true_y)
        else:
            moved_rect.move_ip(self.pc_screen_surf_x, self.pc_screen_surf_true_y)
        return moved_rect

       
    # -- Start Screen + Boot Screen Functionality --
    
    def run_start(self):
        while self.waiting_start:
            self.dt = self.clock.tick(FPS) / 1000.0
            want_start = self.render_start_screen()
            if want_start:
                self.effects_sounds['boot_sound'].play()
                self.waiting_start = False

    def draw_start(self):
        """ """
        pg.display.set_caption(f"Crud Cafe v3.11 - {self.clock.get_fps():.2f}")
        # -- draw the background and screen surf -- 
        self.scene_img.blit(self.pinboard_image_surf, (0,20))
        self.screen.blit(self.scene_img, (0, 0)) 
        self.wipe_computer_screen_surface()
        self.pc_screen_surf.blit(self.login_1_img, (0, 0)) # 50 is the top tabs area, need to hard code this once added it in 
        # -- redraw the screen once we've blit to it, with a rect as a temp faux monitor outline/edge --
        screen_outline_rect = self.screen.blit(self.pc_screen_surf, (self.pc_screen_surf_x, self.pc_screen_surf_y))
        screen_outline_rect.height += 15
        pg.draw.rect(self.screen, DARKGREY, screen_outline_rect, 25) # draws the faux monitor edge around the screen surf     
        # --
        pg.display.flip()

    def run_boot(self):
        while self.waiting_boot:
            want_start = self.draw_boot()
            if want_start:
                self.waiting_boot = False

    def draw_boot(self):
        """ """
        self.scene_img.blit(self.pinboard_image_surf, (0,20))
        self.screen.blit(self.scene_img, (0, 0)) 
        self.wipe_computer_screen_surface()
        self.pc_screen_surf.blit(self.login_2_img, (25, 25)) # 50 is the top tabs area, need to hard code this once added it in --
        # -- redraw the screen once we've blit to it, with a rect as a temp faux monitor outline/edge --
        screen_outline_rect = self.screen.blit(self.pc_screen_surf, (self.pc_screen_surf_x, self.pc_screen_surf_y))
        screen_outline_rect.height += 15
        pg.draw.rect(self.screen, DARKGREY, screen_outline_rect, 25) # draws the faux monitor edge around the screen surf     
        # --
        pg.display.flip()
        want_continue = self.pause_for_continue()
        # want_continue = self.wait_for_continue()
        if want_continue:
            return True


    # ---- For Events & Misc ----

    def handle_scroll_down(self):
        """ when hovering a valid chatbox window or tab element, scrolls the window down using the down key """
        # -- for orders sidebar scrolling --
        if self.new_orders_tab.is_active_tab and self.new_orders_tab.is_orders_sidebar_surf_hovered:
            self.new_orders_tab.orders_sidebar_scroll_y_offset -= 10
        # -- for chatbox scrolling --
        for a_chatbox in self.chatboxes:
            if a_chatbox.is_hovered:
                a_chatbox.chatbox_window_scroll_y_offset -= 10
        # -- for preparing tab scrolling --
        if self.preparing_orders_tab.is_active_tab:
            self.preparing_orders_tab.tab_scroll_offset -= 10

    def handle_scroll_up(self):
        """ when hovering a valid chatbox window or tab element, scrolls the window up using the up key """
        # -- for chatbox scrolling --
        for a_chatbox in self.chatboxes:
            if a_chatbox.is_hovered:
                a_chatbox.chatbox_window_scroll_y_offset += 10
        # -- for orders sidebar scrolling --
        if self.new_orders_tab.is_active_tab and self.new_orders_tab.is_orders_sidebar_surf_hovered:
            self.new_orders_tab.orders_sidebar_scroll_y_offset += 10
        # -- for preparing tab scrolling --
        if self.preparing_orders_tab.is_active_tab:
            self.preparing_orders_tab.tab_scroll_offset += 10
            if self.preparing_orders_tab.tab_scroll_offset > 0:
                self.preparing_orders_tab.tab_scroll_offset = 0 # coube achieved with min() too tbf

    def pause_for_continue(self):
        self.boot_ticker -= 1
        if self.boot_ticker < 0:
            return "start"

    # -- [ new! ] - for game start / game over --
    def wait_for_continue(self):
        pg.event.wait()
        wait_input = True
        while wait_input:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    # -- press any key to start for now, will do this properly for button press on user and quit button too (maybe with small anim or atleast changed state image (i.e. hover effect)) --
                    return "start"
                if event.type == pg.QUIT:
                    wait_input = False
                    self.quit()

# ---- End Game Class ----


# -- instantiate a new game object and run the game --
g = Game()
g.run_start()
g.run_boot()   
while True:
    g.new_level()
    g.run()
    g.game_over_man_game_over()
