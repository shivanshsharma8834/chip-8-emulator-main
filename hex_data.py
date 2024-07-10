a = 0x00 
b = 0xE0

c = a << 8 | b 

d = 0xe0a2

if (d & 0xF000 == 0x0000):

    if d == 0x00E0:

        print('Clear')

