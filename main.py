import pygame as pg
from renderer import Renderer
from keyboard import Keyboard
from speaker import Speaker
from cpu import CPU


class Game:

    def __init__(self) -> None:

        self.display = pg.display.set_mode((640,320))
        self.clock = pg.time.Clock()
        self.running = False 
        self.framerate = 60

    def setup_game(self):

        self.renderer = Renderer(self, scale=10)
        self.keyboard = Keyboard()
        self.speaker = Speaker()
        self.cpu = CPU(self)
        self.cpu.load_rom('roms/BLINKY')
        self.cpu.load_sprites_in_memory()
     

    def run_game(self):

        self.setup_game()

        self.running = True

        while self.running:

            self.display.fill("white")

            self.renderer.render()

            self.cpu.cycle()

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
