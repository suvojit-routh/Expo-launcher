import pygame

class Branding:
    def __init__(self, surface,sound):
        self.surface = surface
        self.font = pygame.font.Font('font/font.ttf', 80)
        self.opacity = 4
        self.time = 0
        self.sound = sound
        self.end_time = 1000
    def update(self):
        self.rect_x = (self.surface.get_width() - self.end_time)//2
        self.rect_y = self.surface.get_height() - 50
        self.bg_rect = pygame.Rect((self.rect_x,self.rect_y),(self.end_time,30))
        self.main_rect = pygame.Rect((self.rect_x,self.rect_y),(self.time +2,30))
        self.surface.fill('white')
        self.text = self.font.render('EXPOVERSE', True, 'black')
        self.text.set_alpha(self.opacity)
        self.text_x = (self.surface.get_width() - self.text.get_width()) // 2
        self.text_y = (self.surface.get_height() - self.text.get_height()) // 2
        self.surface.blit(self.text, (self.text_x, self.text_y))
        pygame.draw.rect(self.surface,'pink',self.bg_rect,0,20)
        pygame.draw.rect(self.surface,'cyan',self.main_rect,0,20)
        pygame.draw.rect(self.surface,'black',self.main_rect,1,20)
        pygame.draw.rect(self.surface,'black',self.bg_rect,1,20)

        if self.opacity < 255:
            self.opacity += 4
        if self.time < self.end_time:
        	self.time += 4
        else:
            self.sound.play(-1)
            return 'menu'

        return 'branding'
