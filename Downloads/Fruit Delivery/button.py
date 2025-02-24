import pygame

class Button:
    def __init__(self, surface, width, height, pos_x, pos_y, text, rect_color, hover_color, text_color,sound,font_size = 40):
        self.surface = surface
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.hover_color = hover_color
        self.rect_color = rect_color
        self.color = rect_color
        self.image = pygame.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        self.clicked = False
        self.font_size = font_size
        self.font = pygame.font.Font('font/font.ttf', self.font_size)
        self.sound = sound
        
    def draw(self):
        gap = 1
        action = False
        pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked condition
        if self.image.collidepoint(pos):
            self.rect_color = self.hover_color
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if self.sound is not None:
                    self.sound.play()
                self.clicked = True
                action = True
        else:
            self.rect_color = self.color
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        text = self.font.render(self.text, True, self.text_color)
        text_pos_x = self.pos_x + (self.width - text.get_width()) // 2
        text_pos_y = self.pos_y + (self.height - text.get_height()) // 2
        pygame.draw.rect(self.surface, self.rect_color, self.image, border_radius=20)
        pygame.draw.rect(self.surface, 'black', self.image,width = 2, border_radius=20)
        self.surface.blit(text, (text_pos_x, text_pos_y + 2))

        return action
    def hover(self,width,border_radius,color,text):
        pos = pygame.mouse.get_pos()
        gap = 5
        hover_text = self.font.render(text,True,'black')
        pos_x = self.pos_x + self.width + gap*4
        
        pos_y = self.pos_y + (self.height - hover_text.get_height())//2

        
        # check mouseover and clicked condition
        if self.image.collidepoint(pos):
            pygame.draw.rect(self.surface,color,[self.pos_x,self.pos_y,self.width,self.height],width = width,border_radius = border_radius)
            pygame.draw.rect(self.surface,'white',[pos_x - gap,pos_y - gap,hover_text.get_width() + gap*2,hover_text.get_height() + gap*2],border_radius = 10)
            pygame.draw.rect(self.surface,'black',[pos_x - gap,pos_y - gap,hover_text.get_width() + gap*2,hover_text.get_height() + gap*2],width = 2,border_radius = 10)
            self.surface.blit(hover_text,(pos_x,pos_y))