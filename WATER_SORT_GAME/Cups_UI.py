import pygame, screeninfo
from Color import Color

SCREEN_SIZE = screeninfo.get_monitors()[0]
MM_TO_PIXEL = SCREEN_SIZE.width / SCREEN_SIZE.width_mm
WIDTH_SCREEN = SCREEN_SIZE.width_mm * MM_TO_PIXEL
HEIGHT_SCREEN = SCREEN_SIZE.height_mm * (MM_TO_PIXEL - 2)
print(WIDTH_SCREEN)
print(HEIGHT_SCREEN)

class Rect_Cup:    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, color, surface, width_border, radius):
        pygame.draw.rect(surface, Color[1], (self.x, self.y, self.width, self.height), width_border, border_bottom_left_radius = radius, border_bottom_right_radius = radius)
        pygame.draw.rect(surface, color, (self.x + width_border, self.y - 0.5 , self.width - 2 * width_border, self.height + 0.5), border_bottom_left_radius = radius - 1, border_bottom_right_radius = radius - 1)
        self.color = color

    def delete(self, color, surface, width_border, radius):
        pygame.draw.rect(surface, Color[1], (self.x, self.y, self.width, self.height), width_border, border_bottom_left_radius = radius, border_bottom_right_radius = radius)
        pygame.draw.rect(surface, color, (self.x + width_border, self.y - width_border , self.width - 2 * width_border, self.height + width_border), border_bottom_left_radius = radius - 1, border_bottom_right_radius = radius - 1)
        self.color = color
        
class Cup:
    def __init__(self, list_Color, surface, capacity, Color):
        self.list_Color = list_Color
        self.length = len(list_Color)
        self.capacity = capacity
        self.list_Rect = []
        self.surface = surface
        self.Color = Color
    
    def draw_cup(self, x, y, width, height, width_border):
        radius = 0
        for i in range(self.capacity + 1):
            if i == 0:
                radius = 30
            else:
                radius = 0
            Rect = Rect_Cup(x, y - height * (i + 1), width, height)
            Rect.draw(Color[0], self.surface, width_border, radius)    
            self.list_Rect.append(Rect)

        for i in range(len(self.list_Color)):
            if i == 0:
                radius = 30
            else:
                radius = 0
            color_array = self.list_Color[i]
            self.list_Rect[i].draw(self.Color[color_array], self.surface, width_border, radius)
        
        for i in range(len(self.list_Color), self.capacity):
            if i != 0:
                self.list_Rect[i].delete(Color[0], self.surface, width_border, 0)
   
    def move_up(self, surface, x, y, w, h):
        self.surface.fill(Color[0])
        self.list_Rect = []
        self.draw_cup(10, 350, w, h, 4)
        surface.blit(self.surface, (x, y))
    
    def move_down(self, surface, x, w, h):
        self.surface.fill(Color[0])
        self.list_Rect = []
        self.draw_cup(10, 350, w, h, 2)
        surface.blit(self.surface, (x, 100))



class Cups:
    def __init__(self, inital_state, num_cups, capacity, surface, path, Color):
        self.initial_state = inital_state
        self.num_cups = num_cups
        self.capacity = capacity
        self.path = path
        self.surface = surface
        self.Color = Color
        self.list_Cups = []
        self.list_surface_cup = []
        self.width_per_surface = int(WIDTH_SCREEN / self.num_cups)
        for i in range(self.width_per_surface):
            surface = pygame.Surface((self.width_per_surface, 500), pygame.SRCALPHA)
            self.list_surface_cup.append(surface)
        self.initListCup(self.list_surface_cup)
    
    def initListCup(self, surface):
        index = 0
        for i in self.initial_state:
            self.list_Cups.append(Cup(i, surface[index], self.capacity, self.Color))
            index += 1
    
    def draw(self):
        for i in range (self.num_cups):
            self.list_Cups[i].draw_cup(10, 350, int(0.8 * self.width_per_surface), 50, 2)
            self.surface.blit(self.list_surface_cup[i], (i * self.width_per_surface, 100))
        pygame.display.update()

    def move(self, action):
        i, j, num = action
        self.list_Cups[i].move_up(self.surface, i * self.width_per_surface , 50, int(0.8 * self.width_per_surface), 50)
        self.list_Cups[j].move_up(self.surface, j * self.width_per_surface , 50, int(0.8 * self.width_per_surface), 50)
        pygame.display.update()
        pygame.time.delay(300)
        while num != 0:
            color = self.list_Cups[i].list_Color[-1]
            self.list_Cups[i].list_Color = self.list_Cups[i].list_Color[0:-1]
            self.list_Cups[j].list_Color = self.list_Cups[j].list_Color + color
            num -= 1
        self.list_Cups[i].move_down(self.surface, i * self.width_per_surface, 0.8 * self.width_per_surface, 50)
        self.list_Cups[j].move_down(self.surface, j * self.width_per_surface, 0.8 * self.width_per_surface, 50)
        pygame.display.update()
        pygame.time.delay(300)


