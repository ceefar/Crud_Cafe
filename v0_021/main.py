
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        # -- load folders -- 
        game_folder = path.dirname(__file__)
        imgs_folder = path.join(game_folder, 'imgs')
        fonts_folder = path.join(game_folder, 'fonts')
        # -- load fonts -- 
        self.FONT_TWINMARKER_26 = pg.font.Font((path.join(fonts_folder, "TwinMarker.ttf")), 26) 
        self.FONT_VETERAN_TYPEWRITER_26 = pg.font.Font((path.join(fonts_folder, "veteran typewriter.ttf")), 26) 
        self.FONT_BOHEMIAN_TYPEWRITER_26 = pg.font.Font((path.join(fonts_folder, "Bohemian Typewriter.ttf")), 26)

    def new_level(self):
        # -- groups --
        self.all_sprites = pg.sprite.Group()
        self.tabs = pg.sprite.Group()
        self.customers = pg.sprite.Group()
        # -- general game level vars --
        self.customers_this_level = 5
        # -- sprite class initialisations --
        # - customers -
        for _ in range(0, self.customers_this_level):
            Customer(self)
        # - tabs -
        self.new_orders_tab = New_Orders_Tab(self)
        self.chats_tab = Chats_Tab(self)
        # -- player toggles --
        self.display_tabs = ["new_orders", "chats"] # "map", "settings"
        #
        self.all_shelved_chat_customers = []
        self.all_open_chat_customers = []

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        """ update the game loop """
        self.all_sprites.update()
        for a_customer in self.customers:
            if isinstance(a_customer, Customer): # ik, it will be duh, but i just want the type hints while testing                
                clicked_shelved_customer = a_customer.check_click_shelved_chatbox()
                if clicked_shelved_customer:
                    if clicked_shelved_customer not in self.all_open_chat_customers:
                       self.all_open_chat_customers.append(clicked_shelved_customer)
                #
                clicked_open_customer = a_customer.check_click_opened_chatbox()
                if clicked_open_customer:
                    print(f"{clicked_open_customer.my_name = }")
                    if self.display_tabs[0] == "new_orders":   
                        self.new_orders_tab.image = self.new_orders_tab.blank_img_surf
                        # break < adding a break means the bottom one comes off first so would be easy to figure out the inverse
                        # to stop the jittery blit 
                        # you just need to reblit here - or just in refactor tomo figure it out more thoroughly for the order of operations!
                else:
                    a_unknownstate_customer = a_customer.get_all_shelved_customers()
                    if a_unknownstate_customer: # it will return false if the customer isnt shelved so only add it if we got a customer back
                        if a_unknownstate_customer not in self.all_shelved_chat_customers:
                            self.all_shelved_chat_customers.append(a_unknownstate_customer)
                
    def draw(self):
        self.screen.fill(BGCOLOR)
        pg.display.set_caption(f"Crud Cafe Empire : {self.clock.get_fps():.1f}")   
        # -- create a surface for the bottom bar which will hold shelved chats --
        self.chat_bar_surf = pg.Surface((WIDTH, 60))
        self.chat_bar_surf.fill(TAN) 
        # -- loop the all sprites group and do draw stuff -- 
        for sprite in self.all_sprites:
            # -- orders tab --
            if isinstance(sprite, New_Orders_Tab):
                if self.display_tabs[0] == "new_orders":
                    sprite.draw()
            # -- chats tab --
            if isinstance(sprite, Chats_Tab):
                if self.display_tabs[0] == "chats":
                    sprite.draw()            
        # -- end all sprites loop -- 
        # -- loop all the open chat customers (not in all sprites) and draw their chatboxes to the open tabs image -- 
        for index, a_customer in enumerate(self.all_open_chat_customers):
            if self.display_tabs[0] == "new_orders":   
                if isinstance(a_customer, Customer): 
                    self.new_orders_tab.image = a_customer.draw_open_chatbox(index, self.new_orders_tab.image) 
            if self.display_tabs[0] == "chats":
                if isinstance(a_customer, Customer): 
                    self.new_orders_tab.image = a_customer.draw_open_chatbox(index, self.chats_tab.image)
        # -- loop all the shelved chat customers and draw their chatboxes to the bottom chatbar bar --
        for index, a_customer in enumerate(self.all_shelved_chat_customers):
            if isinstance(a_customer, Customer): 
                a_customer.draw_shelved_chatbox(index)
        # -- draw the chatbar surface across the bottom of the screen --
        self.screen.blit(self.chat_bar_surf, (0, HEIGHT - self.chat_bar_surf.get_height())) # hard code height var once display is sorted (is also in the above surface init obvs)     
        # -- finally flip the display -- 
        pg.display.flip()

    def events(self):
        # -- preset mouse states - these will reset each run through -- 
        self.mouse_click_up = False
        # -- handle all events here --
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # -- mouse up 
            if event.type == pg.MOUSEBUTTONUP: # <- own function duh
                self.mouse_click_up = True
            # -- key up -- 
            if event.type == pg.KEYUP:
                # -- Q = toggle the tabs using qwerty --
                if event.key == pg.K_q: 
                    # -- use deque for this duh! --
                    # cycle the tabs by adding the current tab to the end of the list and popping it off the front                    
                    self.display_tabs.append(self.display_tabs[0]) 
                    self.display_tabs.pop(0)
                    print(self.display_tabs)                    
            # -- key down --
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def game_over_man_game_over(self):
        pass

    def draw_grid(self): # [UNUSED]
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))    


# -- driver --
if __name__ == "__main__":         
    # -- create and the game --
    g = Game()
    g.show_start_screen()
    while True:
        g.new_level()
        g.run()
        g.game_over_man_game_over()
