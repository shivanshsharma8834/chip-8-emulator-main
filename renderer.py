import math

import pygame as pg 

class Renderer:

    def __init__(self, game, scale) -> None:
        
        self.cols = 64 
        self.rows = 32

        self.scale = scale 

        self.game = game 

        self.display_buffer = [0] * (self.cols * self.rows)
    

    def setPixel(self,x,y):

        if (x >= self.cols):

            x -= self.cols

        elif (x <= 0):

            x += self.cols

        if (y >= self.rows):

            x -= self.rows
        
        elif (y <= 0):

            y += self.rows


        pixel_loc = x + (y * self.cols)

        print("Pixel loc: ", pixel_loc)

        if pixel_loc < 2048:
            self.display_buffer[pixel_loc] ^= 1 

            return not(self.display_buffer[pixel_loc])

    def clear(self):

        self.display_buffer = [0] * (self.cols * self.rows)


    def render(self):


        for i in range(len(self.display_buffer)):

            x = ( i % self.cols ) * self.scale
            y = math.floor(i / self.cols) * self.scale

            if (self.display_buffer[i]):

                pg.draw.rect(self.game.display, "black", (x,y, self.scale, self.scale))
            





