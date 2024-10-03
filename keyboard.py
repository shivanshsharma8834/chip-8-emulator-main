import pygame as pg
import sys

class Keyboard:

    def __init__(self) -> None:
        
        self.key_map = {
            49: 0x1,    #1
            50: 0x2,    #2
            51: 0x3,    #3
            52: 0xc,    #4
            113: 0x4,    #Q
            119: 0x5,    #W
            101: 0x6,    #E
            114: 0xD,    #R
            97: 0x7,    #A
            115: 0x8,    #S
            100: 0x9,    #D
            102: 0xE,    #F
            122: 0xA,    #Z
            120: 0x0,    #X
            99: 0xB,    #C
            118: 0xF     #V
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
                
                case pg.KEYUP:

                    self.on_key_up(event.key)


        