import binascii
import math

class CPU:

    def __init__(self, game, renderer, keyboard = None, speaker = None) -> None:
        
        self.game = game 
        self.renderer = renderer
        self.keyboard = keyboard
        self.speaker = speaker 

        self.memory = [0] * 4096

        self.v = [0] * 16

        self.i = 0

        self.delayTimer = 0 
        self.soundTimer = 0 

        self.pc = hex(0x200)

        self.stack = list()

        self.paused = False 

        self.speed = 10 

    def load_sprites_in_memory(self):

        sprites = [
                b'\xF0', b'\x90', b'\x90', b'\x90', b'\xF0',  # 0
                b'\x20', b'\x60', b'\x20', b'\x20', b'\x70',  # 1
                b'\xF0', b'\x10', b'\xF0', b'\x80', b'\xF0',  # 2
                b'\xF0', b'\x10', b'\xF0', b'\x10', b'\xF0',  # 3
                b'\x90', b'\x90', b'\xF0', b'\x10', b'\x10',  # 4
                b'\xF0', b'\x80', b'\xF0', b'\x10', b'\xF0',  # 5
                b'\xF0', b'\x80', b'\xF0', b'\x90', b'\xF0',  # 6
                b'\xF0', b'\x10', b'\x20', b'\x40', b'\x40',  # 7
                b'\xF0', b'\x90', b'\xF0', b'\x90', b'\xF0',  # 8
                b'\xF0', b'\x90', b'\xF0', b'\x10', b'\xF0',  # 9
                b'\xF0', b'\x90', b'\xF0', b'\x90', b'\x90',  # A
                b'\xE0', b'\x90', b'\xE0', b'\x90', b'\xE0',  # B
                b'\xF0', b'\x80', b'\x80', b'\x80', b'\xF0',  # C
                b'\xE0', b'\x90', b'\x90', b'\x90', b'\xE0',  # D
                b'\xF0', b'\x80', b'\xF0', b'\x80', b'\xF0',  # E
                b'\xF0', b'\x80', b'\xF0', b'\x80', b'\x80'   # F
        ]

        for i in range(0, len(sprites)):

            self.memory[i] = sprites[i]


    
    def load_rom(self, rom_name):
         
        with open(rom_name,'rb') as rom_dump:
             
            rom_data = rom_dump.read()

            program = []

            for i in range(0, len(rom_data),4):
                 
                program.append(rom_data[i:i + 4])
                           
        for location in range(0, len(program)):

            self.memory[512 + location] = program[location]
            
    
    def cycle(self):

        for i in range(self.speed):

            if not(self.paused):

                opcode = self.memory[self.pc] + self.memory[self.pc + 1]

                self.execute_instruction(opcode)


        self.renderer.render()


    def execute_instruction(self,opcode):

        self.pc += 2 

        x = (opcode & 0x0f00) 

           
                 




            


            
         



        