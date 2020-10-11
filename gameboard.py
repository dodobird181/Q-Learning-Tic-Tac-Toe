import pygame
import settings
from core import ClickableGameObject
from gametile import GameTile
from learn import AiPlayer

'''
'
' The GameBoard class is responsible for creating and drawing the Tic-Tac-Toe board,
' as well as managing its various tiles and their respective states.
'
'''
class GameBoard(ClickableGameObject):

	#Makes and populates the 'tiles' array
	def __init__(self, game, turn, singleplayer):
		self.tiles = [['00', '01', '02'], ['10', '11', '12'], ['20', '21', '22']]
		self.make_tiles()
		self.turn = turn
		self.started = turn
		self.winner = 'b'
		self.game = game
		self.rect = pygame.Rect(0, 0, settings.screen_width, settings.screen_height)
		self.singleplayer = singleplayer
		self.AIMOVE = pygame.USEREVENT+1
		if turn == 'x':
			self.ai = AiPlayer('policyfirstmove')
		else:
			self.ai = AiPlayer('policysecondmove')

		if singleplayer:
			self.game.event_handler.schedule_event(self.AIMOVE, self.ai.update_board, self, 500)

	#Draws the lines of the tic-tac-toe board and the 3x3 grid of tiles
	def draw(self, window):
		self.draw_tiles(window)
		self.draw_board(window)

	#Draws the four lines of the tic-tac-toe board
	def draw_board(self, window, line_length = 300, color = (0, 0, 0)):

		#Two vertical lines
		pygame.draw.rect(window, color, (int(settings.screen_width/2) - 1 + int(settings.square_size/2), int(settings.screen_height/2) - int(line_length/2), 2, line_length))
		pygame.draw.rect(window, color, (int(settings.screen_width/2) - 1 - int(settings.square_size/2), int(settings.screen_height/2) - int(line_length/2), 2, line_length))

		#Two horizontal lines
		pygame.draw.rect(window, color, (int(settings.screen_width/2) - int(line_length/2), int(settings.screen_height/2) - 1 + int(settings.square_size/2), line_length, 2))
		pygame.draw.rect(window, color, (int(settings.screen_width/2) - int(line_length/2), int(settings.screen_height/2) - 1 - int(settings.square_size/2), line_length, 2))

	#Draws the tiles in a 3x3 grid
	def draw_tiles(self, window):
		for i in range(0, 3):
			for j in range(0, 3):
				t = self.tiles[i][j]
				t.draw(window)

	#Creates and positions the 3x3 grid of tic-tac-toe tiles
	def make_tiles(self):
		size = settings.square_size
		for i in range(0, 3):
			for j in range(0, 3):
				self.tiles[i][j] = GameTile(int(settings.screen_width/2) - int(size/2) - size + (size*i), int(settings.screen_height/2) - int(size/2) - size + (size*j), self)

	#Checks to see if a player has won the game by looking at
	#the states of tiles in the 'tiles' list, assigns the 'winner'
	#variable to a 'x', 'o', or 't', for X, O, or TIE respectivly.
	def check_win(self):

		#Checks vertical and horizontal wins for both 'x' and 'o'
		ver_score = 0
		hor_score = 0
		for i in range(0, 3):
			for j in range(0, 3):
				t = self.tiles[i][j]
				if t.state == 'x': ver_score += 1
				elif t.state == 'o': ver_score -= 1
				t = self.tiles[j][i]
				if t.state == 'x': hor_score += 1
				elif t.state == 'o': hor_score -= 1
			if ver_score == 3 or hor_score == 3: self.winner = 'x'
			elif ver_score == -3 or hor_score == -3: self.winner = 'o'
			ver_score = 0
			hor_score = 0

		#Checks diagonal wins for both 'x' and 'o'
		if self.tiles[0][0].state == 'x' and self.tiles[1][1].state == 'x' and self.tiles[2][2].state == 'x':
			self.winner = 'x'
		elif self.tiles[0][0].state == 'o' and self.tiles[1][1].state == 'o' and self.tiles[2][2].state == 'o':
			self.winner = 'o'
		elif self.tiles[0][2].state == 'x' and self.tiles[1][1].state == 'x' and self.tiles[2][0].state == 'x':
			self.winner = 'x'
		elif self.tiles[0][2].state == 'o' and self.tiles[1][1].state == 'o' and self.tiles[2][0].state == 'o':
			self.winner = 'o'

		#Checks for ties
		tie = True
		for i in range(0, 3):
			for j in range(0, 3):
				t = self.tiles[i][j]
				if t.state == 'b':
					tie = False
		if tie and self.winner == 'b':
			self.winner = 't'

		self.display_win()

	#Display the winner message if someone won / tied, and
	#change the color of the board tiles depending on the winner.
	def display_win(self):
		if self.winner != 'b':

			#Display who won the game
			if self.winner == 't':
				self.game.state().add_message('Tie!', 48, 0, -200)
				self.set_board_color((200, 255, 200))
			elif self.winner == 'x':
				self.game.state().add_message('X Wins!', 48, 0, -200)
				self.set_board_color((255, 200, 200))
			else:
				self.game.state().add_message('O Wins!', 48, 0, -200)
				self.set_board_color((255, 200, 200))

			#Ask whether or not they want to play again, or go back to 'title'
			self.game.state().add_message('Play again?', 24, -125, 200)
			self.game.state().add_button('Yes', 24, 0, 200, self.reset_game_board)
			self.game.state().add_button('No', 24, 75, 200, self.back_to_title)

	#
	def reset_game_board(self):
		if self.singleplayer:
			if self.started == 'x':
				self.game.load_game('o', True)
			else:
				self.game.load_game('x', True)
		else:
			self.game.start_multiplayer()

	#
	def back_to_title(self):
		self.game.load_title()

	#
	def set_board_color(self, color = settings.background_color):
		for i in range(0, 3):
			for j in range(0, 3):
				self.tiles[i][j].color = color

	#
	def mouse_up(self):
		if self.singleplayer:
			if self.turn == 'o':
				self.try_click_tile()

				#If the game is in singleplayer mode, schedule for the ai to move
				#after 500 ms have passed.
				if self.singleplayer:
					self.game.event_handler.schedule_event(self.AIMOVE, self.ai.update_board, self, 500)
		else:
			self.try_click_tile()

	#
	def try_click_tile(self):
		mouse_pos = pygame.mouse.get_pos()
		for i in range(0, 3):
			for j in range(0, 3):
				if self.tiles[i][j].rect.collidepoint(mouse_pos):
					self.tiles[i][j].mouse_up()

	#
	def mouse_over(self):
		mouse_pos = pygame.mouse.get_pos()
		for i in range(0, 3):
			for j in range(0, 3):
				if self.tiles[i][j].rect.collidepoint(mouse_pos):
					self.tiles[i][j].mouse_over()
				else:
					self.tiles[i][j].mouse_not_over()