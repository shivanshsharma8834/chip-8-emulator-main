import pygame as pg
from renderer import Renderer
from cpu import CPU


class Game:

    def __init__(self) -> None:

        self.display = pg.display.set_mode((640,640))
        self.clock = pg.time.Clock()
        self.running = False 
        self.framerate = 60

    def setup_game(self):

        self.renderer = Renderer(self, 20)
        self.renderer.test_render()

        self.cpu = CPU(self,self.renderer)

        self.cpu.load_rom('roms/BLITZ')
        self.cpu.load_sprites_in_memory()
        print(self.cpu.memory)

    
       

    def run_game(self):

        self.setup_game()

        self.running = True

        while self.running:

            self.display.fill("white")

            self.renderer.render()


            for event in pg.event.get():

                if event.type == pg.QUIT:

                    self.running = False

            pg.display.update()

            self.clock.tick(self.framerate)



        pg.quit()

        

if __name__ == "__main__":

    pg.init()

    game = Game()

    game.run_game()
