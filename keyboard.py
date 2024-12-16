import pygame as pg
import sys

class Keyboard:

    def __init__(self) -> None:
        
        self.key_map = {
            pg.K_1: 0x1,    #1
            pg.K_2: 0x2,    #2
            pg.K_3: 0x3,    #3
            pg.K_4: 0xc,    #4
            pg.K_q: 0x4,    #Q
            pg.K_w: 0x5,    #W
            pg.K_e: 0x6,    #E
            pg.K_r: 0xD,    #R
            pg.K_a: 0x7,    #A
            pg.K_s: 0x8,    #S
            pg.K_d: 0x9,    #D
            pg.K_f: 0xE,    #F
            pg.K_z: 0xA,    #Z
            pg.K_x: 0x0,    #X
            pg.K_c: 0xB,    #C
            pg.K_v: 0xF     #V
        }

        self.keys_pressed = [False for i in range(16)]

        self.on_next_key_press = None 


    def is_key_pressed(self,keycode):

        return self.keys_pressed[keycode]

    def on_key_down(self,event):

        try:
            key = self.key_map[event]
            self.keys_pressed[key] = True
        except:
            pass

    
    def on_key_up(self, event):

        try:
            key = self.key_map[event]
            self.keys_pressed[key] = False
        except:
            pass


    def event_handler(self):

        for event in pg.event.get():

            match event.type:   

                case pg.QUIT:
                    sys.exit()

                case pg.KEYDOWN:

                    self.on_key_down(event.key)
                    print("Event key: ", event.key)
                
                case pg.KEYUP:

                    self.on_key_up(event.key)


        