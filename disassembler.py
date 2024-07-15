def load_rom(rom_name):
         
        with open(rom_name,'rb') as rom_dump:
             
            rom_data = rom_dump.read()

            program = []

            for i in range(0, len(rom_data), 2):
                 
                program.append(int(rom_data[i: i + 2].hex(), base=16))
                           
        # for location in range(0, len(program)):

        #     self.memory[int(hex(0x200), base=16) + location] = program[location]


            return program 
        

def process_program(program):
     
     for opcode in program:
          

        F = opcode & 0xf000 >> 12 
        X = opcode & 0x0f00 >> 8 
        Y = opcode & 0x00f0 >> 4 
        N = opcode & 0x000f 
        NN = opcode & 0x00ff 
        NNN = opcode & 0x0fff 
        print(hex(opcode))
        print(hex(F))
        
        # if F == 0x0: 
             
        #     print('Case 0')
        #     if (NNN == 0x0e0):
        #         print('Clear instruction.')
        #     elif (NNN == 0x0ee):
        #         print('Return from a subroutine')
            
        #     continue
        
        # elif F == 0x1:
             
        #     print('Case 1')
        #     print(f'Jumping to address {NNN}')

        #     continue



        # elif F == 0x2:
             
        #     print('Case 2')
        #     continue
        
        # elif F == 0x3:
             
        #     print('Case 3')
        #     continue
        
        # elif F == 0x4:
             
        #     print('Case 4')
        #     continue
        
        # elif F == 0x5:
             
        #     print('Case 5')
        #     continue
        
        # elif F == 0x6:
             
        #     print('Case 6')
        #     print(f'Set register V{X} to {NN}')
        #     continue

    
        # elif F == 0x7:
             
        #     print('Case 7')
        #     print(f'Add {NN} to V{X}')
        #     continue
        
        # elif F == 0x8:
             
        #     print('Case 8')
        #     continue
        
        # elif F == 0x9:
             
        #     print('Case 9')
        #     continue
        
        # elif F == 0xa:
             
        #     print('Case A')
        #     print(f'Set index register to {NNN}')
        #     continue

        # elif F == 0xb:
             
        #     print('Case B')
        #     continue

        # elif F == 0xc:
             
        #     print('Case C')
        #     continue

        # elif F == 0xd:
             
        #     print('Case D')
        #     print(f'Draw a sprite at coordinates from V{X} and V{Y}')
        #     continue

        # elif F == 0xe:
             
        #     print('Case E')
        #     continue

        # elif F == 0xf:
             
        #     print('Case F')
        #     continue

        


        
    
if __name__ == "__main__":
     
    program = load_rom('roms/IBM') 
    print(program)
     
    process_program(program)


