import binascii
import math
import random

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

        self.pc = int(hex(0x200), base=16)

        self.stack = list()

        self.paused = False 

        self.speed = 1

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

            self.memory[i] = int(sprites[i].hex(), base=16)


    
    def load_rom(self, rom_name):
         
        with open(rom_name,'rb') as rom_dump:
             
            rom_data = rom_dump.read()

            program = []

            for i in range(0, len(rom_data)):
                 
                program.append(int(rom_data[i: i + 1].hex(), base=16))
                           
        for location in range(0, len(program)):

            self.memory[int(hex(0x200), base=16) + location] = program[location]
            
    
    def cycle(self): 

        for i in range(self.speed):

            if not(self.paused):

                print(f'Program counter {self.pc}')
                print(f'Current memory = {self.memory[self.pc]}')

                
                opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1] # Opcode is made by attaching two instructions together.
                

                self.execute_instruction(opcode)
                

                

        self.renderer.render()


    def execute_instruction(self,opcode): 

        self.pc += 2
        
        F = (opcode & 0xf000) >> 12
        X = (opcode & 0x0f00) >> 8
        Y = (opcode & 0x00f0) >> 4
        N = (opcode & 0x000f) 
        NN = (opcode & 0x00ff)
        NNN = (opcode & 0x0fff)

        print(f'Opcode is {opcode}')
        print(f'Hex opcode is {hex(opcode)}')
        print(f'X: {hex(X)}, Y: {hex(Y)}, N: {hex(N)}, NN: {hex(NN)}, NNN: {hex(NNN)}')

        if (F == 0x0): # Clear screen
             
            if (NN == 0xe0):
                print('Clear screen 00E0')
                self.renderer.clear()
                return
            if (NN == 0xee):
                print('Return from subroutine')
                self.pc = self.stack.pop()
                return

        if (F == 0x1): # Jump to address NNN 
            print(f'Jump to address {NNN} 1NNN')
            self.pc = NNN 
            return
        
        if (F == 0x2): 
            print(f'Call subroutine at {NNN}')
            self.stack.append(self.pc)
            self.pc = NNN
            return 
    
        if (F == 0x3):
            print(f'Skip instruction if VX == NN')
            if (self.v[X] == NN):
                self.pc += 2
            return

        if (F == 0x4):
            print(f'Skip instruction if VX != NN')
            if (self.v[X] != NN):
                self.pc += 2 
            return 
    
        if (F == 0x5):
            print(f'Skip instruction if VX == VY')
            if (self.v[X] == self.v[Y]):
                self.pc += 2 
            return 
    
        if (F == 0x9):
            print(f'Skip instruction if VX != VY')
            if (self.v[X] != self.v[Y]):
                self.pc += 2
            return 

        if (F == 0x6) : 
            print(f'Set register V{X} to {NN} 6XNN')
            self.v[X] = NN
            return
        
        if (F == 0x7) :
            print(f'Add register V{X} the value {NN} 7XNN')
            self.v[X] += NN
            return
        
        if (F == 0x8):
            if (N == 0x0):
                self.v[X] = self.v[Y]
                return 

            if (N == 0x1):
                self.v[X] = self.v[X] | self.v[Y]
                return 
            
            if (N == 0x2):
                self.v[X] = self.v[X] & self.v[Y]
                return 
        
            if (N == 0x3):
                self.v[X] = self.v[X] ^ self.v[Y]
                return 
        
            if (N == 0x4):
                
                self.v[X] += self.v[Y]

                self.v[0xf] = 0
                
                if self.v[X] > 0xff:
                    self.v[0xf] = 1

                self.v[X] = self.v[X] & 0xff

                return 
            
            if (N == 0x5):

                self.v[0xf] = 0

                if self.v[X] > self.v[Y]:

                    self.v[0xf] = 1

                self.v[X] -= self.v[Y]

                return  
            
            if N == 0x6:

                self.v[0xf] = self.v[X] & 0x1

                self.v[X] >>= 1

                return 
            
            if N == 0x7:

                self.v[0xf] = 0

                if self.v[X] > self.v[Y]:

                    self.v[0xf] = 1

                self.v[X] = self.v[Y] - self.v[X]

                return  

            if N == 0xe:

                self.v[0xf] = self.v[X] & 0x80

                self.v[X] <<= 1

                return 

            



            
            



        if (F == 0xa) :
            print(f'Set index register to {NNN} ANNN')
            self.i = NNN
            return

        if F == 0xb:

            self.pc = NNN + self.v[0]

            return 
        
        if F == 0xc:

            randnum = random.randint(0, 255)
            self.v[X] = randnum & 0xff

            return 


        if (F == 0xd) :
            print(f'Drawn instruction handled')
            width = 8 
            height = (opcode & 0xf)

            self.v[0xf] = 0

            for row in range(0, height):
                sprite = self.memory[self.i + row]

                for col in range(0,width):

                    if ((sprite & 0x80) > 0):

                        if ((self.renderer.setPixel(self.v[X] + col, self.v[Y] + row))):
                            self.v[0xf] = 1

                    sprite <<= 1
            return
        

        else:
            print(f'Instruction not handled yet')
            return




            



        
            


           
                 




            


            
         



        