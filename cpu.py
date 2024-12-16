import pygame as pg
import random

USE_ORIGINAL_8XY6 = False


class CPU:

    def __init__(self, game) -> None:
        
        self.game = game

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

                opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1] # Opcode is made by ORing two instructions together.
                

                self.execute_instruction(opcode)
                

                

        self.game.renderer.render()


    def execute_instruction(self,opcode): 

        self.pc += 2

        if opcode & 0xffff == 0x00e0: # Clear screen 
             
            self.game.renderer.clear()
            
        elif opcode & 0xffff == 0x00ee: # Return from subroutine

            self.pc = self.stack.pop()

        elif opcode & 0xf000 == 0x1000: # Jump to address

            address = opcode & 0x0fff
            self.pc = address
        
        elif opcode & 0xf000 == 0x2000: # Call subroutine

            address = opcode & 0x0fff
            self.stack.append(self.pc)
            self.pc = address

        elif opcode & 0xf000 == 0x3000: # Skip if v[x] == kk 

            x = (opcode & 0x0f00) >> 8 

            kk = opcode & 0x00ff 

            if self.v[x] == kk:

                self.pc += 2 
         
        elif opcode & 0xf000 == 0x4000: # Skip if v[x] != kk

            x = (opcode & 0x0f00) >> 8 

            kk = opcode & 0x00ff 

            if self.v[x] != kk:

                self.pc += 2 
        
        elif opcode & 0xf00f == 0x5000: # Skip if v[x] == v[y]

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            if self.v[x] == self.v[y]:

                self.pc += 2 

        elif opcode & 0xf000 == 0x6000: # Set v[x] == kk

            x = (opcode & 0x0f00) >> 8 
            kk = opcode & 0x00ff 

            self.v[x] = kk

        elif opcode & 0xf000 == 0x7000: # Add value kk to v[x]

            x = (opcode & 0x0f00) >> 8 
            kk = opcode & 0x00ff

            self.v[x] = (self.v[x] + kk) & 0xff

        elif opcode & 0xf00f == 0x8000: # Set v[x] = v[y]

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4 

            self.v[x] = self.v[y]

        elif opcode & 0xf00f == 0x8001: # Bitwise OR v[x] and v[y]

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            self.v[x] |= self.v[y]

            self.v[0xf] = 0 

        elif opcode & 0xf00f == 0x8002: # Bitwise AND v[x] and v[y]

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            self.v[x] &= self.v[y]

            self.v[0xf] = 0
            
        elif opcode & 0xf00f == 0x8003: # Bitwise XOR v[x] and v[y]

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            self.v[x] ^= self.v[y]

            self.v[0xf] = 0

        elif opcode & 0xf00f == 0x8004: # Add v[y] to v[x] with overflow

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            self.v[x] += self.v[y]

            if self.v[x] > 0xff:

                self.v[0xf] = 1 
                self.v[x] &= 0xff 

            else:

                self.v[0xf] = 0

        elif opcode & 0xf00f == 0x8005: # Sub v[y] from v[x] with underflow

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            vx = self.v[x]
            vy = self.v[y]

            self.v[x] = (vx - vy) & 0xff 

            if vx >= vy:

                self.v[0xf] = 1 

            else:

                self.v[0xf] = 0 
        
        elif opcode & 0xf00f == 0x8006: # Shift right

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            self.v[0xf] = self.v[y] & 0x1 

            self.v[x] = (self.v[y] >> 1) & 0xff

        elif opcode & 0xf00f == 0x8007: # Subtract v[x] from v[y] and store in v[x] 

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            self.v[x] = (self.v[y] - self.v[x]) & 0xff 

            if self.v[y] > self.v[x]:

                self.v[0xf] = 1

            else:
                
                self.v[0xf] = 0

        elif opcode & 0xf00f == 0x800e: # Shift to the left 

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4

            self.v[0xf] = (self.v[y] & 0x80) >> 7 

            self.v[x] = (self.v[y] << 1) & 0xff



        elif opcode & 0xf00f == 0x9000: # Skip if v[x] != v[y]

            x = (opcode & 0x0f00) >> 8 
            y = (opcode & 0x00f0) >> 4 

            if self.v[x] != self.v[y]:

                self.pc += 2
        
        elif opcode & 0xf000 == 0xa000: # Set index register to nnn

            address = opcode & 0x0fff 

            self.i = address

        elif opcode & 0xf000 == 0xb000: # Jump to address with offset v[0]

            address = opcode & 0x0fff 

            self.pc = address + self.v[0]

        elif opcode & 0xf000 == 0xc000: # Set v[x] to random number 

            x = (opcode & 0x0f00) >> 8 
            kk = opcode & 0x00ff 

            random_num = (random.randint(0, 255)) & kk

            self.v[x] = random_num

        elif opcode & 0xf000 == 0xd000: # Draw instruction

            x = self.v[(opcode & 0x0f00) >> 8] 
            y = self.v[(opcode & 0x00f0) >> 4]

            self.v[0xf] = 0

            n = opcode & 0x000f

            # width = 8 
            # height = (opcode & 0xf)

            # for row in range(0, height):
            #     sprite = self.memory[self.i + row]

            #     for col in range(0,width):

            #         if ((sprite & 0x80) > 0):

            #             if ((self.game.renderer.setPixel(self.v[x] + col, self.v[y] + row))):
            #                 self.v[0xf] = 1

            #         sprite <<= 1

            for row in range(n):

                sprite_row = self.memory[self.i + row]

                for bit in range(8):

                    pixel = (sprite_row >> (7 - bit)) & 0x01

                    screen_x = (x + bit) % 64 
                    screen_y = (y + row) % 32 

                    if pixel:

                        self.game.renderer.setPixel(screen_x, screen_y)




        elif opcode & 0xf0ff == 0xe09e: 

            x = (opcode & 0x0f00) >> 8

            key = self.v[x]

            keys = pg.key.get_pressed()

            corresponding_pg_key = None 

            for pg_key, chip8_key in self.game.keyboard.key_map.items():

                if chip8_key == key:

                    corresponding_pg_key = pg_key
                    
                    break
            
            if corresponding_pg_key and keys[corresponding_pg_key]:

                self.pc += 2 

            return 
            
        elif opcode & 0xf0ff == 0xe0a1:

            x = (opcode & 0x0f00) >> 8

            key = self.v[x]

            keys = pg.key.get_pressed()

            corresponding_pg_key = None 

            for pg_key, chip8_key in self.game.keyboard.key_map.items():

                if chip8_key == key:

                    corresponding_pg_key = pg_key
                    
                    break
            
            if not corresponding_pg_key or not keys[corresponding_pg_key]:

                self.pc += 2 

            return 
        
        elif opcode & 0xf0ff == 0xf007:

            x = (opcode & 0x0f00) >> 8

            self.v[x] = self.delayTimer
        
        elif opcode & 0xf0ff == 0xf00a:

            x = (opcode & 0x0f00) >> 8

            keys = pg.key.get_pressed()

            key_pressed = False

            for pg_key, chip8_key in self.game.keyboard.key_map.items():

                if keys[pg_key]:

                    self.v[x] = chip8_key

                    key_pressed = True 

                    break

            if key_pressed:

                waiting_for_release = True

                while waiting_for_release:

                    for event in pg.event.get():

                        if event.type == pg.KEYUP:

                            waiting_for_release = False

            else:

                self.pc -= 2  
            
        elif opcode & 0xf0ff == 0xf015:

            x = (opcode & 0x0f00) >> 8

            self.delayTimer = self.v[x]

        elif opcode & 0xf0ff == 0xf018:

            x = (opcode & 0x0f00) >> 8

            self.soundTimer = v[x]

        elif opcode & 0xf0ff == 0xf01e:

            x = (opcode & 0x0f00) >> 8

            self.i += self.v[x]

        elif opcode & 0xf0ff == 0xf029:

            x = (opcode & 0x0f00) >> 8

            self.i = 0x50 + (self.v[x] * 5)

        elif opcode & 0xf0ff == 0xf033:

            x = (opcode & 0x0f00) >> 8

            val = self.v[x]

            hundreds = val // 100

            tens = (val // 10) % 10 

            ones = val % 10 

            self.memory[self.i] = hundreds
            self.memory[self.i + 1] = tens 
            self.memory[self.i + 2] = ones

        elif opcode & 0xf0ff == 0xf055:

            x = (opcode & 0x0f00) >> 8

            for i in range(x + 1):

                val = self.v[i]

                self.memory[self.i + i] = val 

            self.i = self.i + x + 1 

        elif opcode & 0xf0ff == 0xf065:

            x = (opcode & 0x0f00) >> 8

            for i in range(x + 1):

                val = self.memory[self.i + i]

                self.v[i] = val


            self.i = self.i + x + 1        

        else:
            print(f'Instruction not handled yet, opcode: {hex(opcode)}')
            
        
        if self.delayTimer > 0:

            self.delayTimer -= 1 

        if self.soundTimer > 0:

            self.soundTimer -= 1

            if self.soundTimer == 0:

                print("Play beep")

    
        
        




            



        
            


           
                 




            


            
         



        