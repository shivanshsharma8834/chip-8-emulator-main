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
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
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

           
                 




            


            
         



        