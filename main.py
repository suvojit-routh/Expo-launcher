import pygame
import requests
import json
from enum import Enum,auto
from pygame.locals import *
pygame.init()

screen_width = 1366
screen_height = 768
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Expo Launcher")
clock = pygame.time.Clock()
FPS = 60

# importing the updater json 
updater_json_url = "https://raw.githubusercontent.com/suvojit-routh/Expo-launcher/main/updater.json"
try:
    response = requests.get(updater_json_url)
    response.raise_for_status()  
    data = response.json()      
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    data = {}  

print(data)

class State(Enum):
	INTERSTELLAR_PIRATE = auto()
	FRUIT_DELIVERY = auto()
	HEADBALL_FOOTBALL = auto()


# BUTTONS CLASS
mouse_released = True

class Button:
    def __init__(self, display, width, height, pos_x, pos_y, text, rect_color, hover_color, text_color, font_size=35, adjustment = 0 , border_color="black", visibility=True):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.display = display
        self.text = text
        self.text_color = text_color
        self.hover_color = hover_color
        self.rect_color = rect_color
        self.color = rect_color
        self.border_color = border_color
        self.visibility = visibility
        self.image = pygame.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        self.font_size = font_size
        self.adjustment = adjustment
        self.font = pygame.font.Font('assets/font/font-1.ttf', self.font_size)
        self.hover_font = pygame.font.Font('assets/font/subatomic.ttf', 20)

        

    def draw(self, radius=8):
        global mouse_released

        action = False
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.image.collidepoint(pos):
            pygame.draw.rect(self.display, self.rect_color, self.image, border_radius=radius)
            self.rect_color = self.hover_color
            if mouse_pressed and mouse_released:  # Only trigger if mouse is released
                mouse_released = False  # Lock further clicks
                action = True

        else:
            self.rect_color = self.color


        if not mouse_pressed:
            mouse_released = True

        if self.visibility:
            pygame.draw.rect(self.display, self.rect_color, self.image, border_radius=radius)
        

        pygame.draw.rect(self.display, self.border_color, self.image, width=1, border_radius=radius)

        text = self.font.render(self.text, True, self.text_color)
        text_pos_x = self.pos_x + (self.width - text.get_width()) // 2
        text_pos_y = self.pos_y + (self.height - text.get_height()) // 2
        self.display.blit(text, (text_pos_x, text_pos_y - self.adjustment))
        return action

    def hover(self,hover_text,side,adjustment):
        self.font2 = pygame.font.Font('assets/font/font-1.ttf', 20)
        self.hover_text = self.font2.render(hover_text,True,'white')
        self.text_width = self.hover_text.get_width()
        self.text_height = self.hover_text.get_height()
        self.side = side
        self.below_x = self.pos_x + (self.width - self.text_width) //2
        self.below_y = self.pos_y + (self.height + adjustment)
        self.right_x = self.pos_x + (self.width + adjustment)
        self.right_y = self.pos_y + (self.height - self.text_height)//2
        self.gap = 5
        mouse_pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked condition
        if self.image.collidepoint(mouse_pos):
            if self.side == 'below':
                pygame.draw.rect(screen,'black',[self.below_x - self.gap,self.below_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],0,4)
                pygame.draw.rect(screen,'white',[self.below_x - self.gap,self.below_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],2,4)
                screen.blit(self.hover_text,(self.below_x,self.below_y+2))
            if self.side == 'right':
                pygame.draw.rect(screen,'black',[self.right_x - self.gap,self.right_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],0,4)
                pygame.draw.rect(screen,'white',[self.right_x - self.gap,self.right_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],2,4)
                screen.blit(self.hover_text,(self.right_x,self.right_y+2))

# PICTURE BUTTONS
class Picture_Button:
    def __init__(self,surface,x,y,image):
        self.image = image
        self.x = x 
        self.y = y
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.clicked = False
        self.surface = surface
        self.font = pygame.font.Font('assets/font/font-1.ttf',20)

    def hover(self,text,color):
        self.text = text
        self.color = color
        self.text_surf = self.font.render(self.text,True,self.color)
        self.text_width = self.text_surf.get_width()
        self.text_height = self.text_surf.get_height()
        self.gap = 4
        self.adjustment = 50
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen,"white",[(self.x + self.image.get_width()) + self.adjustment - self.gap,self.y + (self.image.get_height()/2) - self.gap,self.text_width + self.gap * 2,self.text_height + self.gap * 2],0,8)
            pygame.draw.rect(screen,"black",[(self.x + self.image.get_width()) + self.adjustment - self.gap,self.y + (self.image.get_height()/2) - self.gap,self.text_width + self.gap * 2,self.text_height + self.gap * 2],2,8)
            screen.blit(self.text_surf,((self.x + self.image.get_width()) + self.adjustment,self.y + (self.image.get_height()/2)))

    
        
    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        gap = 2
        
        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen,"white",[self.x  - gap,self.y - gap,self.image.get_width() + gap * 2,self.image.get_height() + gap * 2],2,10)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
        	pygame.draw.rect(screen,"black",[self.x  - gap,self.y - gap,self.image.get_width() + gap * 2,self.image.get_height() + gap * 2],2,10)
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        self.surface.blit(self.image,(self.rect.x ,self.rect.y ))
        return action
# BACKGROUND CLASS
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("assets/bg/0.png").convert()
        self.image = pygame.transform.scale(img,(screen_width,screen_height))
        self.rect = self.image.get_rect()
        self.pos_x = 0
        self.pos_y = 0
        self.rect.topleft = [self.pos_x, self.pos_y]


    def update(self):
        self.pos_y += 10
        screen.blit(self.image, (self.pos_x, self.pos_y))

        next_pos_y = self.pos_y - screen_height
        if next_pos_y > -screen_height:
            screen.blit(self.image, (self.pos_x, next_pos_y))

        if self.pos_y >= screen_height:
            self.pos_y = 0


        self.rect.topleft = [self.pos_x, self.pos_y]

background_group = pygame.sprite.Group()
background = Background()
background_group.add(background)

class Launcher():
	def __init__(self):
		self.state = State.INTERSTELLAR_PIRATE
		self.running = True 
		self.games_btn = Button(screen,50,50,50,screen_height - 60,"::","gray","white","black",60,4)
		self.close_button = Button(screen,50,50,50,10,"X","gray","white","black",40)
		self.show_all = False
		self.transition = False
        # icon list
		self.icon_list = []
		for i in range(3):
			img = pygame.transform.smoothscale(pygame.image.load(f"assets/icons/{i}.png"),(100,100)).convert_alpha()
			self.icon_list.append(img)
		#loading bgs
		self.bg_list = []
		for i in range(1,3):
			img = pygame.transform.smoothscale(pygame.image.load(f"assets/bg/{i}.png"),(screen_width,screen_height)).convert_alpha()
			self.bg_list.append(img)
        # PICTURE BUTTONS
		self.interstellar_pirate_btn = Picture_Button(screen,25,screen_height - 170,self.icon_list[0])
		self.fruit_delivery_btn = Picture_Button(screen,25,screen_height - 300,self.icon_list[1])
		self.headball_football_btn = Picture_Button(screen,25,screen_height - 430,self.icon_list[2])
		#SIDEBAR
		self.sidebar_y = screen_height  
		self.sidebar_target_y = 0       
		self.sidebar_width = 150
		self.sidebar_speed = 40
	def draw_glass_sidebar(self):
		glass_surface = pygame.Surface((self.sidebar_width, screen_height), pygame.SRCALPHA)
		glass_surface.fill((255, 255, 255, 20))
		pygame.draw.rect(glass_surface, (211, 211, 211, 120), (0, 0, self.sidebar_width, screen_height), 2) 
		screen.blit(glass_surface, (0, self.sidebar_y))   


	def sidebar_buttons(self):
		if not self.show_all:
			if not self.sidebar_y > screen_height - 170:
				if self.interstellar_pirate_btn.draw():
					self.state = State.INTERSTELLAR_PIRATE
				self.interstellar_pirate_btn.hover("Interstellar Pirate","black")
			if not self.sidebar_y > screen_height - 300:		
				if self.fruit_delivery_btn.draw():
					self.state = State.FRUIT_DELIVERY
				self.fruit_delivery_btn.hover("Fruit Delivery","black")
			if not self.sidebar_y > screen_height - 430:
				if self.headball_football_btn.draw():
					self.state = State.HEADBALL_FOOTBALL
				self.headball_football_btn.hover("Headball Football","black")
		if self.show_all:
			if self.sidebar_y < screen_height - 170:
				if self.interstellar_pirate_btn.draw():
					self.state = State.INTERSTELLAR_PIRATE
				self.interstellar_pirate_btn.hover("Interstellar Pirate","black")
			if self.sidebar_y < screen_height - 300:		
				if self.fruit_delivery_btn.draw():
					self.state = State.FRUIT_DELIVERY
				self.fruit_delivery_btn.hover("Fruit Delivery","black")
			if self.sidebar_y < screen_height - 430:
				if self.headball_football_btn.draw():
					self.state = State.HEADBALL_FOOTBALL
				self.headball_football_btn.hover("Headball Football","black")
			

	def sidebar(self):
		if self.show_all:		    
		    if self.sidebar_y > self.sidebar_target_y:
		        self.sidebar_y -= self.sidebar_speed
		        if self.sidebar_y < self.sidebar_target_y:
		            self.sidebar_y = self.sidebar_target_y
		            self.transition = True  
		            
		else:
		    if self.sidebar_y < screen_height:
		        self.sidebar_y += self.sidebar_speed
		        if self.sidebar_y > screen_height:
		            self.sidebar_y = screen_height  
		            self.transition =  False
		

	def run(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						self.running = False


				
			if self.state == State.INTERSTELLAR_PIRATE:
				background_group.draw(screen)
				background_group.update()
				self.sidebar()
				self.draw_glass_sidebar()
				self.sidebar_buttons()
			elif self.state == State.FRUIT_DELIVERY:
				screen.blit(self.bg_list[0],(0,0))
				self.sidebar()
				self.draw_glass_sidebar()
				self.sidebar_buttons()
			else:
				screen.blit(self.bg_list[1],(0,0))
				self.sidebar()
				self.draw_glass_sidebar()
				self.sidebar_buttons()

					

			if not self.show_all and self.transition==False:
				if self.games_btn.draw():
					self.show_all = True
			if self.show_all and self.transition:				
				if self.close_button.draw():
					self.show_all = False



			clock.tick(FPS)
			pygame.display.flip()

app = Launcher()
app.run()