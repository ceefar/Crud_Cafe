# -- imports --
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *


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
        # -- load images -- 
        self.scene_img = pg.image.load(path.join(imgs_folder, SCENE_IMG)).convert_alpha() # self.an_img = pg.transform.scale(self.an_img, (140, 140)) # (56, 56))        
        self.window_img = pg.image.load(path.join(imgs_folder, WINDOW_IMG)).convert_alpha()  
        self.window_hl_1_img = pg.image.load(path.join(imgs_folder, WINDOW_HL_1_IMG)).convert_alpha()  
        self.window_hl_2_img = pg.image.load(path.join(imgs_folder, WINDOW_HL_2_IMG)).convert_alpha()  
        self.window_shelved_1_img = pg.image.load(path.join(imgs_folder, WINDOW_SHELVED_1_IMG)).convert_alpha()  
        self.window_shelved_hl_1_img = pg.image.load(path.join(imgs_folder, WINDOW_SHELVED_HL_1_IMG)).convert_alpha()  
        # -- load fonts -- 
        self.FONT_TWINMARKER_26 = pg.font.Font((path.join(fonts_folder, "TwinMarker.ttf")), 26) 
        self.FONT_VETERAN_TYPEWRITER_20 = pg.font.Font((path.join(fonts_folder, "veteran typewriter.ttf")), 20) 
        self.FONT_VETERAN_TYPEWRITER_26 = pg.font.Font((path.join(fonts_folder, "veteran typewriter.ttf")), 26) 
        self.FONT_BOHEMIAN_TYPEWRITER_12 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 12)
        self.FONT_BOHEMIAN_TYPEWRITER_14 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 14)
        self.FONT_BOHEMIAN_TYPEWRITER_16 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 16)
        self.FONT_BOHEMIAN_TYPEWRITER_20 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 20)
        self.FONT_BOHEMIAN_TYPEWRITER_26 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 26)
        # -- define main gui surface dimensions --
        self.pc_screen_surf_width, self.pc_screen_surf_height = 1000, 600
        self.pc_screen_surf_x, self.pc_screen_surf_y = (WIDTH / 2) - (self.pc_screen_surf_width / 2), 100
        self.tab_bar_height = 50 # the top bar on the pc_screen_surf the emulate browser tabs
        self.pc_screen_surf_true_y = self.pc_screen_surf_y + self.tab_bar_height # else y val doesnt take the tab_bar_height into consideration

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
        self.chats_tab = Chats_Tab(self)
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
       
    def run(self):
        # runs the game loop... thank you for coming to my TEDtalk
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # for Python v2.x
            self.events()
            self.update()
            self.draw()

    def wipe_computer_screen_surface(self):
        """ we use this as a base to draw everything on to, it is basically our game surface """
        self.pc_screen_surf = pg.Surface((self.pc_screen_surf_width, self.pc_screen_surf_height))
        self.pc_screen_surf.fill(SKYBLUE) # once setup the actual tab bar, make this black - then will make boot up / boot down animation hella easy

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        """ keep update and draw seperate for best practice, runs before draw() but after events() """
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
        # -- loop all chatboxes to handle states seperately as we may need to break this loop, there won't be enough windows on screen for this ever to be problematic -- 
        self.hovered_chatbox = False
        for a_chatbox in reversed(self.chatbox_layer_list):
            if isinstance(a_chatbox, Chatbox): # purely for type hints
                if a_chatbox.handle_hover_or_click():
                    self.hovered_chatbox = a_chatbox # save this instance as we will unset the hover for every other instance that isnt this one
                    break
        # -- loop all chatboxes to run each instances update - importantly is done this way as increments a counter for offset positions, else would do self.chatboxes.update() --
        for this_chatbox in self.chatboxes:
            if isinstance(this_chatbox, Chatbox): # purely for type hints
                # -- reset the hovered var on all chatbox instances that weren't the hovered one that we saved when we broke out of the loop above earlier -- 
                if this_chatbox != self.hovered_chatbox:
                    this_chatbox.is_hovered = False                    
                this_chatbox.update() 
        # -- then at the end of update reset the chatbox layers to be in the correct order --
        self.reorder_all_window_layers()
 
    def draw(self):
        pg.display.set_caption(f"Crud Cafe v1.00 - {self.clock.get_fps():.2f}")
        # -- draw the background -- 
        self.screen.blit(self.scene_img, (0,0)) 
        # -- wipe the computer screen surface at the start of each frame, we then draw to this surface and then blit it to the screen (without the fill) -- 
        self.wipe_computer_screen_surface()
        # -- loop tabs --
        for sprite in self.browser_tabs:
            if isinstance(sprite, Browser_Tab): # really for type hinting
                if sprite.is_active_tab:  
                    self.chatbox_layers.draw(sprite.image)
                    # -- for customer selector popup - has to happen after drawing chatbox layers in order of operations as its a popup, it should be on top of everything else --
                    if isinstance(sprite, New_Orders_Tab):
                        if sprite.want_customer_select_popup:
                            sprite.draw_active_customers_selector_popup()
                    # -- actually draw the tab surface to the screen -- 
                    sprite.draw_tab_to_pc()

        # -- redraw the screen once we've blit to it, with a rect as a temp faux monitor outline/edge --
        screen_outline_rect = self.screen.blit(self.pc_screen_surf, (self.pc_screen_surf_x, self.pc_screen_surf_y))
        pg.draw.rect(self.screen, DARKGREY, screen_outline_rect, 25) # draws the faux monitor edge around the screen surf               
        # -- finally, flip the display --
        pg.display.flip()

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
                    self.chats_tab.is_active_tab = not self.chats_tab.is_active_tab
                # -- temporary way to incrememntally make customers active, this will be handled by a game timer in future but this is waaay better for testing --  
                created_customers = len(self.all_active_customers) # the amount of customers you've manually added in already
                # -- handle the exception if we accidentally try to add too many customers than we have available by just skipping over it, in the real game this will basically be the end level state - once the last customer has been completed or cancelled anyways --
                try:
                    if event.key == pg.K_1:
                        self.id_customer_dict[created_customers + 1].customer_state = "active"
                except KeyError:
                    pass
                # -- for dev mode / debugging during new order functionality implementation + testing --
                # -- toggle the orders in the orders sidebar --
                if event.key == pg.K_o:
                    self.new_orders_tab.active_order_number += 1
                    self.new_orders_tab.orders_sidebar_scroll_y_offset = 0 # reset the scroll offset to 0 when we change to another order too
                # -- new test for tap up/down on keyboard to scroll, but only if on the new orders tab --
                if event.key == pg.K_UP:
                    if self.new_orders_tab.is_active_tab and self.new_orders_tab.is_orders_sidebar_surf_hovered:
                        self.new_orders_tab.orders_sidebar_scroll_y_offset += 10
                if event.key == pg.K_DOWN:
                    if self.new_orders_tab.is_active_tab and self.new_orders_tab.is_orders_sidebar_surf_hovered:
                        self.new_orders_tab.orders_sidebar_scroll_y_offset -= 10
            # -- key down --
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def render_start_screen(self):
        pass

    def game_over_man_game_over(self):
        pass

    # -- For Reordering Layers --
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

# -- instantiate a game object and run the game --
g = Game()
g.render_start_screen()
while True:
    g.new_level()
    g.run()
    g.game_over_man_game_over()
