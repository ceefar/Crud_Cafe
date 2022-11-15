# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 10
# Player and Mob Health
# Video link: https://youtu.be/-9bXcSjuN28
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
        self.FONT_BOHEMIAN_TYPEWRITER_20 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 20)
        self.FONT_BOHEMIAN_TYPEWRITER_26 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 26)
        # -- define gui surface dimensions --
        self.pc_screen_surf_width, self.pc_screen_surf_height = 1000, 600

    def new_level(self):
        """ initialize all variables and do all the setup for a new game """
        # -- level setup values --
        self.total_customers_for_level = 4
        self.all_shelved_chat_customers = [] 
        self.all_open_chat_customers = []
        # self.all_active_customers = [] # -> # dont forget new idea of moving them from active into open or shelved at the start (using the same function that will do it progressively throughout the level on a variable timer)
        # -- groups --
        self.all_sprites = pg.sprite.Group()    
        self.browser_tabs = pg.sprite.Group()
        self.customers = pg.sprite.Group()
        # -- sprite object instances -- 
        self.new_orders_tab = New_Orders_Tab(self)
        self.chats_tab = Chats_Tab(self)
        for _ in range(0, self.total_customers_for_level):
            a_new_customer = Customer(self)
            self.all_open_chat_customers.append(a_new_customer) 
            print(f"Created New Customer {a_new_customer}")

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
        self.pc_screen_surf_x, self.pc_screen_surf_y = (WIDTH / 2) - (self.pc_screen_surf_width / 2), 100
        self.pc_screen_surf = pg.Surface((self.pc_screen_surf_width, self.pc_screen_surf_height))
        self.pc_screen_surf.fill(SKYBLUE)

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # keeps update and draw seperate
        self.browser_tabs.update() 
        self.hovered_customers = []
        for index, a_customer in enumerate(self.customers):
            if isinstance(a_customer, Customer):
                # clicked_open_customer = a_customer.check_click_opened_chatbox()
                # if clicked_open_customer:
                #     print(f"{clicked_open_customer.my_name = }") 
                if a_customer.chatbox_opened_destination_rect:
                    if a_customer.chatbox_opened_destination_rect.collidepoint(pg.mouse.get_pos()):
                        # print(f"Hover {a_customer}")                                
                        self.hovered_customers.append(a_customer) 
        if self.hovered_customers:
            top_hovered_customer = self.hovered_customers[-1]
            clicked_open_customer = top_hovered_customer.check_click_opened_chatbox()
            if clicked_open_customer:
                print(f"{clicked_open_customer.my_name = }") 
    
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
                    # -- loop all the open chat customers (not in all sprites) and draw their chatboxes to the open tabs image -- 
                    print(f"THE ORDER =>> {self.all_open_chat_customers = }")
                    for index, a_customer in enumerate(self.all_open_chat_customers):
                        if isinstance(a_customer, Customer): 
                            self.new_orders_tab.image = a_customer.draw_open_chatbox(index, self.new_orders_tab.image) 
                            print(f"{a_customer}")
                            if self.hovered_customers:
                                if a_customer is self.hovered_customers[-1]:                   
                                    self.new_orders_tab.image = a_customer.draw_open_chatbox(index, self.new_orders_tab.image, True)   
                    sprite.draw_to_pc()
      
        # -- redraw the screen once we've blit to it, with a rect as a temp faux monitor outline/edge --
        screen_outline_rect = self.screen.blit(self.pc_screen_surf, (self.pc_screen_surf_x, self.pc_screen_surf_y))
        pg.draw.rect(self.screen, DARKGREY, screen_outline_rect, 25) # draws the faux monitor edge around the screen surf 
              


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
