import pygame as pg

class Keyboard:

    def __init__(self) -> None:
        
        self.keymap = {
            pg.K_1: 0x1,
            pg.K_2: 0x2, 
            pg.K_3: 0x3,
            pg.K_4: 0xc,
            pg.K_q: 0x4, 
            pg.K_w: 0x5, 
            pg.K_e: 0x6, 
            pg.K_r: 0xD, 
            pg.K_a: 0x7, 
            pg.K_s: 0x8, 
            pg.K_d: 0x9, 
            pg.K_f: 0xE, 
            pg.K_z: 0xA, 
            pg.K_x: 0x0, 
            pg.K_c: 0xB,
            pg.K_v: 0xF  
        }

        self.keys_pressed = []

        self.on_next_key_press = None 


    def is_key_pressed(self,keycode):

        return keycode in self.keys_pressed

    def on_key_down(self,event):

        pass
    
    def on_key_up(self, event):

        pass 

        