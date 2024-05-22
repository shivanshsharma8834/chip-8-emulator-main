class Keyboard:

    def __init__(self) -> None:
        
        self.keymap = {
            49: 0x1,
            50: 0x2, 
            51: 0x3,
            52: 0xc,
            81: 0x4, 
            87: 0x5, 
            69: 0x6, 
            82: 0xD, 
            65: 0x7, 
            83: 0x8, 
            68: 0x9, 
            70: 0xE, 
            90: 0xA, 
            88: 0x0, 
            67: 0xB,
            86: 0xF  
        }

        self.keys_pressed = []

        self.on_next_key_press = None 


    def is_key_pressed(self,keycode):

        return self.keys_pressed[keycode]

    def on_key_down(self,event):

        key =  self.keymap[event.which]

        