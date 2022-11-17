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
        self.tab_bar_height = 50
        self.pc_screen_surf_true_y = self.pc_screen_surf_y + self.tab_bar_height # else y val doesnt take the tab_bar_height into consideration

    def new_level(self):
        """ initialize all variables and do all the setup for a new game """
        # -- level setup values --
        self.total_customers_for_level = 3
        # test -> store all these chatbox (and customer too ig) instances seperately to loop them in reverse
        # - note, ig this should be open list then duh, as per v1.x
        self.chatbox_list = []
        self.customer_list = [] # might not need this tbf just adding it now incase i do in future, if it remains unused then delete it 
        self.customer_chatbox_pairs = {} # using this you can just use any customer sprite / instance as they key to get back the associated chatbox instance / object
        # -- groups --
        self.all_sprites = pg.sprite.Group()    
        self.browser_tabs = pg.sprite.Group()
        self.chatboxes = pg.sprite.Group()
        self.customers = pg.sprite.Group()
        # -- sprite object instances -- 
        self.new_orders_tab = New_Orders_Tab(self)
        self.chats_tab = Chats_Tab(self)
        # -- new layers testing --
        for _ in range(0, self.total_customers_for_level):
            a_customer = Customer(self)
            a_chatbox = Chatbox(self, a_customer)
            self.customer_list.append(a_customer)
            self.chatbox_list.append(a_chatbox)
            self.customer_chatbox_pairs[a_customer] = a_chatbox
        # -- initialise the layers group once the object instances are all added to their respective groups --
        self.chatbox_layers = pg.sprite.LayeredUpdates(self.chatboxes) 
        # -- player vars --
        self.is_player_moving_chatbox = False      
        self.player_put_down_chatbox_this_frame = False
        # -- misc -- 
        self.faux_screen_edge_width = 25
       
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
        self.pc_screen_surf.fill(SKYBLUE)

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # keeps update and draw seperate
        self.browser_tabs.update() 
        # self.chatbox_layers.update() # self.chatboxes.update() # fyi these two and the for loop all do the same? (unlike draw?)        
        for a_chatbox in reversed(self.chatbox_list):
            if isinstance(a_chatbox, Chatbox): # purely for type hinting
                a_chatbox.update()     
        # reset this each frame after it has run for all the chatbox updates
        self.player_put_down_chatbox_this_frame = False  
                 
    def draw(self): 
        pg.display.set_caption(f"Crud Cafe v1.00 - {self.clock.get_fps():.2f}")
        # -- draw the background -- 
        self.screen.blit(self.scene_img, (0,0)) 
        # -- wipe the computer screen surface at the start of each frame, we then draw to this surface and then blit it to the screen (without the fill) -- 
        self.wipe_computer_screen_surface()
        # -- loop tabs --
        for sprite in self.browser_tabs:
            if isinstance(sprite, Browser_Tab): # purely for type hinting
                if sprite.is_active_tab:  
                    sprite.draw_title_to_tab() # literally just the title for now
                    self.chatbox_layers.draw(sprite.image)
                    sprite.render_tab_page_to_tab_image() # literally just the title for now
        # -- loop all chatboxes purely for xray vision outline (wont be a lot anyways tbf), may scrap it but leaving just incase, reverse and break is necessary for top pos --
        for sprite in reversed(self.chatbox_list):
            if isinstance(sprite, Chatbox): # purely for type hinting
                if sprite.chatbox_is_hovered:
                    sprite.draw_outline() # yanno to fix this, loooool, just use the layers donut D:
                    break
        # -- redraw the screen once we've blit to it, with a rect as a temp faux monitor outline/edge --
        screen_outline_rect = self.screen.blit(self.pc_screen_surf, (self.pc_screen_surf_x, self.pc_screen_surf_y))
        pg.draw.rect(self.screen, DARKGREY, screen_outline_rect, self.faux_screen_edge_width) # draws the faux monitor edge around the screen surf               
        # -- finally, flip the display --
        pg.display.flip()

    def events(self):
        """ handle all events here, executes before update() and draw() """
        # -- preset mouse states - these will reset each run through -- 
        self.mouse_click_up = False
        # --
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # -- mouse events --
            if event.type == pg.MOUSEBUTTONUP: 
                self.mouse_click_up = True
            # -- keyboard events --
            if event.type == pg.KEYUP:
                # -- temp toggle between our 2 tabs --
                if event.key == pg.K_q:
                    self.new_orders_tab.is_active_tab = not self.new_orders_tab.is_active_tab
                    self.chats_tab.is_active_tab = not self.chats_tab.is_active_tab
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new_level()
    g.run()
    g.show_go_screen()

