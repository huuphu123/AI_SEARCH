import pygame


from Color import Color
from Cups_UI import *


class UI:
    def __init__(self, Cups: Cups):
        self.Cups = Cups
        self.count = 0
        self.path = Cups.path
        self.active_solve = False
        self.active_reset = False
        self.button = pygame.image.load('./button/button.png')
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
        self.surface.fill(Color[0])
        pygame.display.set_caption('Water sort')
        self.Cups.surface = self.surface
    
    def init_display(self):
        self.surface.fill(Color[0])
        font_surface = pygame.font.Font(None, 50).render('PRESS SPACE TO START!    STEP: ' + str(self.count), None, Color[1])
        self.surface.blit(font_surface, (20, 20))
        self.Cups.draw()

    def run(self):
        self.init_display()
        pygame.display.update()
        pygame.time.delay(50)
        while True:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        clone_path = self.path
                        while len(clone_path) != 0:
                            self.Cups.move(clone_path[0])
                            self.count += 1
                            clone_path = clone_path[1:]
                            self.init_display()
                            pygame.display.update()
                            self.active_solve = True
                        self.path = []
                    

                    

