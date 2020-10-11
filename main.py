import pygame
import settings
import numpy as np
from core import EventHandler
from core import ScreenState
from gametile import GameTile
from gameboard import GameBoard

class Main():

	#Init method
	def __init__(self):

		#Setup pygame and load the game-icon
		pygame.init()
		self.disp = pygame.display
		self.window = self.disp.set_mode((settings.screen_width, settings.screen_height))
		self.disp.set_caption(settings.display_name)
		icon = pygame.image.load("ICON.png")
		self.disp.set_icon(icon)

		#Create the state-stack, where the top-most 
		#ScreenState object on the stack gets updated and drawn.
		self.current_state = None

		#Creates the 'title' state and appends it to the state stack
		self.load_title()

		#Creates the event_handler, which handles every game event
		self.event_handler = EventHandler(self)

		#Begin the game-loop
		self.begin_game_loop()

	#Returns the current ScreenState object
	def state(self):
		return self.current_state

	#Starts the entire game loop.
	def begin_game_loop(self):
		self.running = True
		while self.running:
			pygame.time.delay(settings.refresh_rate)
			self.update_game()
			self.draw_screen()

	#Handles events and then updates every game object in the current state
	def update_game(self):
		self.event_handler.handle()
		self.state().update()

	#Draws every game object in the current state to the screen
	def draw_screen(self):
		self.window.fill(settings.background_color)
		self.state().draw(self.window)
		self.disp.update()

	#Loads the title state by creating a new ScreenState object and
	#adding messages / buttons to the screen. Appends the state to
	#the top of the state stack
	def load_title(self):
		title_state = ScreenState('title')
		title_state.add_message('Tic-Tac-Toe', 64, 0, -50)
		title_state.add_message('By Samuel Morris', 24, 0, 5)
		title_state.add_button('Singleplayer', 24, 0, 60, self.start_singleplayer, (0,180,240), (0,180,230), (0,0,0), (0,220,255))
		title_state.add_button('Multiplayer', 24, 0, 100, self.start_multiplayer, (0,180,240), (0,180,230), (0,0,0), (0,220,255))
		title_state.add_button('Info', 24, 0, 140, self.load_info, (0,180,240), (0,180,230), (0,0,0), (0,220,255))
		self.current_state = title_state

	#Loads the play state by creating a new ScreenState object and
	#adding a GameBoard to it.
	def load_game(self, turn, singleplayer):
		play_state = ScreenState('play')
		play_state.add_object(GameBoard(self, turn, singleplayer))
		self.current_state = play_state

	#Loads a ScreenState with a GameBoard object in 'singleplayer' mode
	#and pushed this ScreenState into the current_state variable.
	def start_singleplayer(self):
		self.load_game('o', True)

	#Loads a ScreenState with a GameBoard object in 'multiplayer' mode
	#and pushed this ScreenState into the current_state variable.
	def start_multiplayer(self):
		self.load_game('x', False)

	#Loads a ScreenState with GameMessages that describe how, and why, I built
	#this Tic-Tac-Toe ai.
	def load_info(self):
		off = -60
		info_state = ScreenState('info')
		info_state.add_message('Why Tic-Tac-Toe?', 48, 0, off + -150)
		info_state.add_message('I decided to build this Tic-Tac-Toe game to', 18, 0, off + -75)
		info_state.add_message('test out a machine-learning technique called', 18, 0, off + -50)
		info_state.add_message('"reinforcement learning". In this technique, the', 18, 0, off + -25)
		info_state.add_message('computer plays many games against itself and,', 18, 0, off + 0)
		info_state.add_message('eventually, learns how to win through', 18, 0, off + 25)
		info_state.add_message('trial and error.', 18, 0, off + 50)

		info_state.add_message('Because Tic-Tac-Toe is such a simple game, the', 18, 0, off + 100)
		info_state.add_message('computer was able to teach itself quickly, and', 18, 0, off + 125)
		info_state.add_message('I could spend more time figuring out how to get', 18, 0, off + 150)
		info_state.add_message('the computer to learn, and less time waiting for', 18, 0, off + 175)
		info_state.add_message('it to play against itself.', 18, 0, off + 200)
		info_state.add_message('Enjoy :)', 18, 0, off + 240)

		info_state.add_button('Back', 24, 0, 225, self.load_title, (0,180,240), (0,180,230), (0,0,0), (0,220,255))
		self.current_state = info_state

m = Main()