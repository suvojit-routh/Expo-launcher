import pygame,os
import requests
import json
import threading
import zipfile
import tkinter as tk
import subprocess
from tkinter import filedialog
from tkinter import messagebox
from enum import Enum,auto
from pygame.locals import *
from time import sleep
pygame.init()

# LAUNCHER DATA 
if not os.path.exists("data.json"):
    # Default data to write in the JSON file
    default_data = {"fruit delivery" : {
    				"version" : 0,
    				"path" : "",
    				"update_path" : "",
    				"uninstall_path" : "",
    				"downloaded" : False
    },
    "interstellar pirates" : {
    				"version" : 0,
    				"path" : "",
    				"update_path" : "",
    				"uninstall_path" : "",
    				"downloaded" : False
    },
    "headball football" : {
    				"version" : 0,
    				"path" : "",
    				"update_path" : "",
    				"uninstall_path" : "",
    				"downloaded" : False
    }
    }
    with open("data.json", 'w') as file:
        json.dump(default_data, file, indent=4)
# READ THE JSON DATA
with open("data.json",'r') as file:
    app_data = json.load(file)

def save_data():
    with open("data.json",'w') as file:
        json.dump(app_data,file,indent = 4)

info = pygame.display.Info()  
screen_width = info.current_w
screen_height = info.current_h
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



class State(Enum):
	INTERSTELLAR_PIRATE = auto()
	FRUIT_DELIVERY = auto()
	HEADBALL_FOOTBALL = auto()
	MANAGE = auto()

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
        

        pygame.draw.rect(self.display, self.border_color, self.image, width=2, border_radius=radius)

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
        self.left_x = self.pos_x - (self.text_width + adjustment)
        self.left_y = self.pos_y + (self.height - self.text_height)//2
        self.gap = 5
        mouse_pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked condition
        if self.image.collidepoint(mouse_pos):
            if self.side == 'below':
                pygame.draw.rect(screen,'black',[self.below_x - self.gap,self.below_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],0,4)
                pygame.draw.rect(screen,'white',[self.below_x - self.gap,self.below_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],2,4)
                screen.blit(self.hover_text,(self.below_x,self.below_y))
            if self.side == 'right':
                pygame.draw.rect(screen,'black',[self.right_x - self.gap,self.right_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],0,4)
                pygame.draw.rect(screen,'white',[self.right_x - self.gap,self.right_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],2,4)
                screen.blit(self.hover_text,(self.right_x,self.right_y))
            if self.side == "left":
                pygame.draw.rect(screen,'black',[self.left_x - self.gap,self.left_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],0,4)
                pygame.draw.rect(screen,'white',[self.left_x - self.gap,self.left_y - self.gap, self.text_width + self.gap*2,self.text_height + self.gap*2],2,4)
                screen.blit(self.hover_text,(self.left_x,self.left_y))


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
            pygame.draw.rect(screen,"black",[(self.x + self.image.get_width()) + self.adjustment - self.gap,self.y + (self.image.get_height()/2) - self.gap,self.text_width + self.gap * 2,self.text_height + self.gap * 2],0,4)
            pygame.draw.rect(screen,"white",[(self.x + self.image.get_width()) + self.adjustment - self.gap,self.y + (self.image.get_height()/2) - self.gap,self.text_width + self.gap * 2,self.text_height + self.gap * 2],2,4)
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

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    folder_path = filedialog.askdirectory(title="Select Folder to Download")
    return folder_path

def download_and_extract_zip(url, extract_to, progress_callback=None,extraction_callback=None, max_retries=20):
    retries = 0
    while retries < max_retries:
        try:
            # print(f"Attempt {retries + 1}/{max_retries}: Downloading {url}")
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open('temp.zip', 'wb') as f:
                    for data in response.iter_content(chunk_size=100000):
                        downloaded += len(data)
                        f.write(data)

                        # Update progress
                        if progress_callback:
                            progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                            progress_callback(progress)

                        # Ensure Pygame events are processed
                            pygame.display.flip()

                # Extract the downloaded zip file
                with zipfile.ZipFile('temp.zip', 'r') as zip_ref:
                    file_list = zip_ref.infolist()
                    total_files = len(file_list)
                    
                    for index, file in enumerate(file_list, start=1):
                        zip_ref.extract(file, extract_to)
                        
                        # Update extraction progress
                        if extraction_callback:
                            extraction_progress = (index / total_files) * 100
                            extraction_callback(extraction_progress)
                        
                        # Ensure Pygame events are processed
                            pygame.display.flip()

                os.remove('temp.zip')  # Clean up temp file
                print("Download and extraction complete!")
                return  # Exit after successful download
            else:
                print(f"Failed to download the file: HTTP {response.status_code}")
                break

        except requests.exceptions.ConnectionError as e:
            retries += 1
            print(f"Connection lost, retrying ({retries}/{max_retries})...")
            if retries >= max_retries:
                print("Max retries reached, aborting download.")
                raise e
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def launch_game(game_path):
    try:
        original_dir = os.getcwd()  # Save current working directory
        game_path_abs = os.path.abspath(game_path)
        game_dir = os.path.dirname(game_path_abs)
        os.chdir(game_dir)  # Change to game's directory
        subprocess.Popen([game_path_abs])  # Launch the .bat file
    except Exception as e:
        print(f"Failed to launch game: {e}")
    finally:
        os.chdir(original_dir)  # Restore original directory

def open_file_explorer(path):
    try:
        subprocess.run(['explorer', path])
    except Exception as e:
        print(f"Failed to open directory: {e}")

class Launcher():
	def __init__(self):
		self.state = State.INTERSTELLAR_PIRATE
		self.running = True 
		self.games_btn = Button(screen,50,50,50,screen_height - 60,"::","gray","white","black",60,4)
		self.close_button = Button(screen,50,50,50,10,"x","gray","white","black",40)
		self.show_all = False
		self.transition = False
		self.font2 = pygame.font.Font("assets/font/copperplate.ttf", 30)
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
		# RECT BUTTONS
		self.download_button = Button(screen,200,50,screen_width - 210,screen_height - 60,"Download","white","#00ff79","black")
		self.launch_button = Button(screen,200,50,screen_width - 210,screen_height - 60,"Launch","white","#00ff79","black")
		self.update_button = Button(screen,200,50,screen_width - 210,screen_height - 60,"Update","white","#00ff79","black")
		self.quit_button = Button(screen,50,50,screen_width - 60 ,10,"x","white","#00ff79","black")
		self.settings_button = Button(screen,50,50,screen_width - 60 ,110,"s","white","#00ff79","black")

		#DOWNLOAD VARS
		self.selected_folder = None
		self.download_progress = 0 
		self.downloaded = False
		self.downloading = False
		self.extraction_progress = 0
		self.extracted = False
		self.extracting = False
	def header(self,data_tree):
		header_font = pygame.font.Font("assets/font/Logo.ttf", 18)
		header_text = header_font.render(f"{data_tree.replace(" ","    ")}",True,"black")
		header_text_width = header_text.get_width()
		header_text_height = header_text.get_height()
		header_pos_x = (screen_width - header_text_width)//2
		header_pos_y = 20
		gap = 10
		pygame.draw.rect(screen,"white",[header_pos_x - gap,header_pos_y -gap,header_text_width + gap*2,header_text_height+gap*2],0,4)
		pygame.draw.rect(screen,"black",[header_pos_x - gap,header_pos_y -gap,header_text_width + gap*2,header_text_height+gap*2],2,4)
		screen.blit(header_text,(header_pos_x,header_pos_y))

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
				self.interstellar_pirate_btn.hover("Interstellar Pirate","white")
			if not self.sidebar_y > screen_height - 300:		
				if self.fruit_delivery_btn.draw():
					self.state = State.FRUIT_DELIVERY
				self.fruit_delivery_btn.hover("Fruit Delivery","white")
			if not self.sidebar_y > screen_height - 430:
				if self.headball_football_btn.draw():
					self.state = State.HEADBALL_FOOTBALL
				self.headball_football_btn.hover("Headball Football","white")
		if self.show_all:
			if self.sidebar_y < screen_height - 170:
				if self.interstellar_pirate_btn.draw():
					self.state = State.INTERSTELLAR_PIRATE
				self.interstellar_pirate_btn.hover("Interstellar Pirate","white")
			if self.sidebar_y < screen_height - 300:		
				if self.fruit_delivery_btn.draw():
					self.state = State.FRUIT_DELIVERY
				self.fruit_delivery_btn.hover("Fruit Delivery","white")
			if self.sidebar_y < screen_height - 430:
				if self.headball_football_btn.draw():
					self.state = State.HEADBALL_FOOTBALL
				self.headball_football_btn.hover("Headball Football","white")

		if self.quit_button.draw():
			save_data()
			self.running = False
		self.quit_button.hover("Quit","left",20)
		if self.settings_button.draw():
			self.state = State.MANAGE
		self.settings_button.hover("Settings","left",20)

			

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

	def update_progress(self, progress):
		self.download_progress = progress
		if int(self.download_progress) >= 100:
			self.downloaded = True
			self.download_progress = 0
			self.extracting = True
		sleep(0.05)
	def update_extraction(self, extract):
		self.extraction_progress = extract
		if int(self.extraction_progress) >= 100:
			self.extracted = True
			self.extraction_progress = 0
		sleep(0.05)

	def download_func(self,data_tree):
		if app_data[data_tree]["downloaded"] == False and self.downloading == False:
			if self.download_button.draw():
				self.selected_folder = select_folder()
				if self.selected_folder:
					self.download_thread = threading.Thread(target=download_and_extract_zip, args=(data[data_tree]["download_url"], self.selected_folder, self.update_progress,self.update_extraction))
					self.download_thread.daemon = True
					self.download_thread.start()
					self.downloading = True

		# Draw the download progress bar if downloading
		if self.download_progress > 0:
			rect_width, rect_height = 600, 50
			pos_x = (screen.get_width() - rect_width) // 2
			pos_y = screen.get_height() - (rect_height + 20)
			bg_rect = pygame.Rect((pos_x, pos_y), (rect_width, rect_height))

			# Ensure main_rect has a minimum width for the border radius
			progress_width = max(self.download_progress * 6, 20)  # Set minimum width for proper border radius rendering
			main_rect = pygame.Rect((pos_x, pos_y), (progress_width, rect_height))

			# Draw background rectangle
			pygame.draw.rect(screen, 'white', bg_rect, 0, 8)
			pygame.draw.rect(screen, "cyan", main_rect, 0, 8)
			pygame.draw.rect(screen, 'black', bg_rect, 2, 8)

			# Render and position the downloading text
			self.downloading_text = self.font2.render(f"Downloading - {self.download_progress:.2f}%", True, 'white')
			self.text_x = (screen.get_width() - self.downloading_text.get_width()) // 2
			self.text_y = pos_y - (self.downloading_text.get_height() + 10)
			screen.blit(self.downloading_text, (self.text_x, self.text_y))
			pygame.display.flip()


		if self.extraction_progress > 0:
			rect_width, rect_height = 600, 50
			pos_x = (screen.get_width() - rect_width) // 2
			pos_y = screen.get_height() - (rect_height + 20)
			bg_rect = pygame.Rect((pos_x, pos_y), (rect_width, rect_height))

			# Ensure main_rect has a minimum width for the border radius
			progress_width = max(self.extraction_progress * 6, 20)  # Set minimum width for proper border radius rendering
			main_rect = pygame.Rect((pos_x, pos_y), (progress_width, rect_height))

			# Draw background rectangle
			pygame.draw.rect(screen, 'white', bg_rect, 0, 8)
			pygame.draw.rect(screen, "red", main_rect, 0, 8)
			pygame.draw.rect(screen, 'black', bg_rect, 2, 8)
			self.extraction_text = self.font2.render(f"Extracting - {self.extraction_progress:.2f}%", True, 'white')
			self.text_x = (screen.get_width() - self.extraction_text.get_width()) // 2
			self.text_y = pos_y - (self.extraction_text.get_height() + 10)
			screen.blit(self.extraction_text, (self.text_x, self.text_y))
			pygame.display.flip()
		self.save_app_data(data_tree)
	def save_app_data(self,data_tree):
		if self.downloaded and self.extracted:
			app_data[data_tree]["downloaded"] = True
			app_data[data_tree]["path"] = f"{self.selected_folder}/{data[data_tree]['folder_name']}/{data[data_tree]['file_name']}"
			app_data[data_tree]["uninstall_path"] = f"{self.selected_folder}/{data[data_tree]['folder_name']}"
			app_data[data_tree]["update_path"] = self.selected_folder
			app_data[data_tree]["version"] = data[data_tree]["version"]
			save_data()

			self.downloaded = False 
			self.downloading = False
			self.extracted = False
			self.extracting = False
			self.selected_folder = None


	def launch_func(self,data_tree):
		if app_data[data_tree]["downloaded"] and app_data[data_tree]["version"] == data[data_tree]["version"]:
			if self.launch_button.draw():
				launch_game(app_data[data_tree]["path"])
	def update_func(self,data_tree):
		if app_data[data_tree]["downloaded"] == True and app_data[data_tree]["version"] != data[data_tree]["version"] and self.downloading == False:
			if self.update_button.draw():
				self.update_thread = threading.Thread(target=download_and_extract_zip, args=(data[data_tree]["update_url"],app_data[data_tree]["update_path"], self.update_progress,self.update_extraction))
				self.update_thread.daemon = True
				self.update_thread.start()
				self.downloading = True
				self.selected_folder = app_data[data_tree]["update_path"]

	
	def reset_data(self,data_tree):
		app_data[data_tree]["downloaded"] = False
		app_data[data_tree]["path"] = ""
		app_data[data_tree]["uninstall_path"] = ""
		app_data[data_tree]["update_path"] = 	""
		app_data[data_tree]["version"] = 0

	def check_if_game_exists(self,data_tree):
		path = app_data[data_tree]["uninstall_path"]
		if not os.path.exists(path):
			self.reset_data(data_tree)

	def all_apps_func(self):
		if not self.show_all and self.transition==False:
			if self.games_btn.draw():
				self.show_all = True
			self.games_btn.hover("All Games","right",20)
		if self.show_all and self.transition:				
			if self.close_button.draw():
				self.show_all = False
			self.close_button.hover("Close Menu","right",20)

	def template(self,data_tree):
		self.header(data_tree)
		self.sidebar()
		self.draw_glass_sidebar()
		self.sidebar_buttons()
		self.all_apps_func()
		self.download_func(data_tree)
		self.update_func(data_tree)
		self.launch_func(data_tree)
		self.check_if_game_exists(data_tree)
	def manage(self):
		screen.fill("white")
		self.header("Mange")
		self.manage_icons = []
		for i in range(3):
			img = pygame.transform.scale(pygame.image.load(f"assets/icons/{i}.png"),(100,100)).convert_alpha()
			self.manage_icons.append(img)

		# Set dynamic y-position for each icon
		icon_spacing = 150  # Space between icons
		start_y = 100  # Starting y position
		locate_game_button_list = []
		uninstall_game_button_list = []

		for i in range(len(self.manage_icons)):
			pos_y = start_y + i * icon_spacing  # Calculate the y-position
			screen.blit(self.manage_icons[i], (100, pos_y))
			locate_game_button_list.append(Button(screen,300,50,screen_width - 400,pos_y + (100-50)//2,"Locate Game","darkgray","cyan","black"))
			uninstall_game_button_list.append(Button(screen,300,50,screen_width - 400,pos_y + (100-50)//2,"Uninstall Game","darkgray","cyan","black"))

		if app_data["interstellar pirates"]["downloaded"]:
			if uninstall_game_button_list[0].draw():
				pass 
		else:
			if locate_game_button_list[0].draw():
				pass


		if app_data["fruit delivery"]["downloaded"]:
			self.check_if_game_exists("fruit delivery")
			if uninstall_game_button_list[1].draw():
				open_file_explorer(app_data["fruit delivery"]["update_path"].replace("/","\\"))
		else:
			if locate_game_button_list[1].draw():
				self.selected_folder = select_folder()
				if self.selected_folder:
					path = f"{self.selected_folder}/{data["fruit delivery"]["folder_name"]}/{data["fruit delivery"]["file_name"]}"
					print(path)
					if os.path.exists(path):
						self.downloaded = True 
						self.extracted = True 
						self.save_app_data("fruit delivery")
						self.state = State.FRUIT_DELIVERY
					else:
						self.state = State.FRUIT_DELIVERY

		if app_data["headball football"]["downloaded"]:
			if uninstall_game_button_list[2].draw():
				pass
		else:
			if locate_game_button_list[2].draw():
				pass


	def run(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						self.running = False
						save_data()


				
			if self.state == State.INTERSTELLAR_PIRATE:
				background_group.draw(screen)
				background_group.update()				
				self.template("interstellar pirates")
			elif self.state == State.FRUIT_DELIVERY:
				screen.blit(self.bg_list[0],(0,0))
				self.template("fruit delivery")

			elif self.state == State.HEADBALL_FOOTBALL:
				screen.blit(self.bg_list[1],(0,0))
				self.template("headball football")
			elif self.state == State.MANAGE:
				self.manage()


					

			



			clock.tick(FPS)
			pygame.display.flip()

app = Launcher()
app.run()