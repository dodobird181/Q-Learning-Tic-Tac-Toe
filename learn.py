import numpy as np
import pickle
import pygame

class GameState():
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		self.game_over = False
		self.player_symbol = -1
		self.board = np.zeros((3, 3))

	# Returns a unique 1-dimensional numpy array representing the board-state, 
	# essentially a R3x3 --> R9 matrix isomorphisim.
	def get_hash(self):
		return str(self.board.reshape(9))

	# Returns a list of the currently available positions on the board
	def get_available_positions(self):
		positions = []
		for i in range(0, 3):
			for j in range(0, 3):
				if self.board[i, j] == 0:
					positions.append((i, j))
		return positions

	# Places the current player symbol on the board at the 'position' tuple and
	# updates the player symbol
	def move_with_current_player(self, position):
		self.board[position] = self.player_symbol
		if self.player_symbol == 1:
			self.player_symbol = -1
		else: 
			self.player_symbol = 1

	# Updates the 'game_over' variable if the game has ended and returns the 
	# winner of the game, '0' if tie, 'None' if game is not over
	def check_win(self):
		# Check horizontal wins
		for i in range(0, 3):
			if sum(self.board[i, :]) == 3:
					self.game_over = True
					return 1
			elif sum(self.board[i, :]) == -3:
				self.game_over = True
				return -1
		# Check vertical wins
		for j in range(0, 3):
			if sum(self.board[:, j]) == 3:
				self.game_over = True
				return 1
			elif sum(self.board[:, j]) == -3:
				self.game_over = True
				return -1
		# Check diagonal wins
		b = self.board
		if b[0, 0] + b[1, 1] + b[2, 2] == 3:
			self.game_over = True
			return 1
		elif b[0, 2] + b[1, 1] + b[2, 0] == 3:
			self.game_over = True
			return 1
		if b[0, 0] + b[1, 1] + b[2, 2] == -3:
			self.game_over = True
			return -1
		elif b[0, 2] + b[1, 1] + b[2, 0] == -3:
			self.game_over = True
			return -1

		# Check for a tie..
		if len(self.get_available_positions()) == 0:
			self.game_over = True
			return 0

		# Otherwise return None if the game is not over
		self.game_over = False
		return None

	# Feeds each player reward based on their performance
	# after the game has finished
	def distribute_reward(self, result):
		if result == 1:
			self.p1.update_weights(0)
			self.p2.update_weights(1)
		elif result == -1:
			self.p1.update_weights(1)
			self.p2.update_weights(0)
		else:
			self.p1.update_weights(0.5)
			self.p2.update_weights(0.5)#p2 is now our agent

	def train(self, rounds = 1000):
		for i in range(rounds):
			if i % 10 == 0:
				print(f"Round {i}")
			# Plays 1 game
			while self.game_over == False:
				# Get player 1 action
				positions = self.get_available_positions()
				p1_action = self.p1.choose_action(positions, self.board, self.player_symbol)

				# Perform action and add the hashed board state to the player's list of states
				self.move_with_current_player(p1_action)
				self.p1.add_state(self.get_hash())
				#print(self.board)

				# Check for a win
				winner = self.check_win()
				if winner != None:
					self.distribute_reward(winner)
					self.p1.reset()
					self.p2.reset()
					self.reset()
					break

				else:# Move player 2
					# Get player 2 action
					positions = self.get_available_positions()
					p2_action = self.p2.choose_action(positions, self.board, self.player_symbol)

					# Perform action and add the hashed board state to the player's list of states
					self.move_with_current_player(p2_action)
					self.p2.add_state(self.get_hash())
					#print(self.board)

					# Check for a win
					winner = self.check_win()
					if winner != None:
						self.distribute_reward(winner)
						self.p1.reset()
						self.p2.reset()
						self.reset()
						break
		#print(f'dict1: {self.p1.state_value_dictionary}')
		#print(f'dict2: {self.p2.state_value_dictionary}')
		self.p1.save_policy()
		self.p2.save_policy()

	# Resets the entire game state
	def reset(self):
		self.board = np.zeros((3, 3))
		self.game_over = False
		self.player_symbol = -1


class Player():
	def __init__(self, name, exp_rate = 0.3):
		self.name = name
		self.states = [] # List to record all positions taken
		self.learning_rate = 0.2
		self.exp_rate = exp_rate # Explore v.s. exploit, 30% chance to take random action, i.e. 'explore'
		self.gamma_decay = 0.9
		self.state_value_dictionary = {} # Dictionary to score any given state's value

	def choose_action(self, positions, current_board, player_symbol):
		if np.random.uniform(0, 1) <= self.exp_rate:# Explore
			index = np.random.choice(len(positions))
			action = positions[index]
			#print(f'{player_symbol} player explored at {action}')
		else:# Exploit
			max_value = -999
			for p in positions:
				next_board = current_board.copy()
				next_board[p] = player_symbol
				next_board_hash = str(next_board.reshape(9))
				value = None
				if self.state_value_dictionary.get(next_board_hash) == None:
					value = 0
				else:
					value = self.state_value_dictionary.get(next_board_hash)
				if value > max_value:
					max_value = value
					action = p
			#print(f'{player_symbol} player exploited at {action}')
		return action

	# Adds a board state to the end of the 'states' list
	def add_state(self, board_state):
		self.states.append(board_state)

	# Resets the player's list of states BUT NOT their stored dictionary values!
	# Important so that we can use the same player multiple times during training
	def reset(self):
		self.states = []

	# TODO
	def update_weights(self, reward):
		for state in reversed(self.states):
			# Sets the corresponding value to all known hashed-state keys to zero if not yet encountered
			if self.state_value_dictionary.get(state) is None:
				self.state_value_dictionary[state] = 0
			# Propagates the reward backwards through each state
			self.state_value_dictionary[state] += (self.learning_rate * (self.gamma_decay * reward - self.state_value_dictionary[state]))
			reward = self.state_value_dictionary[state]

	def save_policy(self):
		file = open('policy' + str(self.name), 'wb')
		pickle.dump(self.state_value_dictionary, file)
		file.close()

	def load_policy(self, filename):
		file = open(filename, 'rb')
		self.state_value_dictionary = pickle.load(file)
		file.close()

	# Returns a list of the currently available positions on the board
	def get_available_positions(self, board):
		positions = []
		for i in range(0, 3):
			for j in range(0, 3):
				if board[i, j] == 0:
					positions.append((i, j))
		return positions

'''
'
' The AiPlayer class is a wrapper for the Player class that has
' been programmed to interact with the GameBoard GUI, essentially
' connecting the AI's state value dictionary to the GameBoard in order
' to choose the best possible move.
'
'''
class AiPlayer(Player):

	#Init Function
	def __init__(self, filename):
		super().__init__(filename, 0.0)
		self.filename = filename
		self.load_policy(self.name)

	#
	def update_board(self, board):
		if board.turn == 'x' and board.winner == 'b':
			abstract_board = self.get_abstract_board(board)
			positions = self.get_available_positions(abstract_board)
			generated_move = self.choose_action(positions, abstract_board, 1)
			board.tiles[generated_move[0]][generated_move[1]].mouse_up()
			board.check_win()

			#Disable the scheduled event timer that triggered this function
			board.game.event_handler.schedule_event(board.AIMOVE, None, None, 0)

	##Generates and returns an abstract board that the Ai, Player, and GameState classes can interact with
	def get_abstract_board(self, board):
		b = np.zeros((3, 3))
		for i in range(0, 3):
			for j in range(0, 3):
				if board.tiles[i][j].state == 'x':
					b[i, j] = 1
				elif board.tiles[i][j].state == 'o':
					b[i, j] = -1
		return b

game_state = GameState(Player('1'), Player('2'))
#game_state.train(rounds = 300000)