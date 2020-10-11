import pygame
import settings
from core import ClickableGameObject

'''
'
' The GameTile class is a ClickableGameObject that stores x's and o's 
' and provides all the player interaction for the GameBoard class.
'
'''
class GameTile(ClickableGameObject):

	#Init Function
	def __init__(self, x, y, game_board, color = settings.background_color):
		self.rect = pygame.Rect(x, y, settings.square_size, settings.square_size)
		self.color = color
		self.state = 'b' # b for blank
		self.board = game_board

	#Draws an 'x', 'o', or nothing, depending on the state of the tile.
	def draw(self, window, circle_rad = 30, x_pad = 25):
		pygame.draw.rect(window, self.color, self.rect)
		if self.state == 'x':
			pygame.draw.line(window, (0,0,0), (self.rect.x+x_pad, self.rect.y+x_pad), (self.rect.x+settings.square_size-x_pad, self.rect.y+settings.square_size-x_pad), 3)
			pygame.draw.line(window, (0,0,0), (self.rect.x+settings.square_size-x_pad, self.rect.y+x_pad), (self.rect.x+x_pad, self.rect.y+settings.square_size-x_pad), 3)
		elif self.state == 'o':
			pygame.draw.circle(window, (0,0,0), (self.rect.x + int(settings.square_size/2), self.rect.y + int(settings.square_size/2)), circle_rad, 2)

	#Changes the 'tile.state' and 'board.turn' appropriately when clicked
	#and checks to see if either player has won
	def mouse_up(self):
		if self.state == 'b' and self.board.winner == 'b':
			if self.board.turn == 'x': 
				self.board.turn = 'o'
				self.state = 'x'
			else:
				self.board.turn = 'x'
				self.state = 'o'
		self.board.check_win()

	def mouse_over(self):
		if self.board.winner == 'b':
			self.color = (220, 255, 255)

	def mouse_not_over(self):
		if self.board.winner == 'b':
			self.color = (255, 255, 255)