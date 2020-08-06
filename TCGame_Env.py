
# importing all the libraries needed for our environment
from itertools import groupby 
from gym import spaces
import numpy as np
import random
from itertools import product
import pandas as pd 
import random
import collections




class TicTacToe():

	''' This class will provide all the things we require for game environment
		when object created will return a fresh environment '''

	def __init__(self):
		"""initialising the board 
		initialises the board position, we will intialize as array here"""
		self.state = [np.nan for _ in range(9)]  
		self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] 
		self.reset()

	def is_winning(self, curr_state):
		''' # This below combinations of number will indicate player is winning. 
			if any pattern is satisfied we consider it as winning '''
		pattern_to_win = [(2,5,8),(0,4,8),(2,4,6),(0,3,6),(1,4,7),(0,1,2),(3,4,5),(6,7,8)]
		
		
		for pattern in pattern_to_win:
			if not np.isnan(curr_state[pattern[0]]) and not np.isnan(curr_state[pattern[1]]) and not np.isnan(curr_state[pattern[2]]):
				if curr_state[pattern[0]] + curr_state[pattern[1]] + curr_state[pattern[2]] == 15:
					return True
		return False

	def allowed_positions(self, curr_state):
		""" # takes a state and returns blank positions in the state"""
		return [i for i, val in enumerate(curr_state) if np.isnan(val)]


	def state_transition(self, curr_state, curr_action):
		'''  takes in state and action, It will return next state after action is taken to bring changes '''
		curr_state[curr_action[0]] = curr_action[1]
		return curr_state


	def allowed_values(self, curr_state):
		""" # Takes the current state  and returns all unused values that can be inserted on the board"""
		used_val = [val for val in curr_state if not np.isnan(val)]
		agent_val = [val for val in self.all_possible_numbers if val not in used_val and val % 2 !=0]
		env_val = [val for val in self.all_possible_numbers if val not in used_val and val % 2 ==0]
		return (agent_val, env_val)


	def is_terminal(self, curr_state):
		''' #  this method will tell us if current state is terminal state
		 This would happen in 3 cases either a draw situation or win or lose
		 If pattern is satisfied or no more space is left in the board '''
		if self.is_winning(curr_state) == True:
			return True, 'Win'

		elif len(self.allowed_positions(curr_state)) ==0:
			return True, 'Tie'

		else:
			return False, 'Resume'


	def action_space(self, curr_state):
		""" # Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

		agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
		env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
		return (agent_actions, env_actions)

	def step(self, curr_state, curr_action):
		final_state = False
		intermediate_state = self.state_transition(curr_state, curr_action)
		final_state, game_status = self.is_terminal(intermediate_state)
		if final_state == True:
			if game_status == 'Win':
				reward=10
			else:
				reward=0
		else:
			pos = random.choice(self.allowed_positions(intermediate_state))
			val = random.choice(self.allowed_values(intermediate_state)[1])
			intermediate_state[pos]= val
			final_state, game_status = self.is_terminal(intermediate_state)
			if final_state == True:
				if game_status == 'Win':
					reward=-10
				else:
					reward=0
			else:
				reward=-1
		return intermediate_state, reward, final_state

	def reset(self):
		# this method will reset the game board
		return self.state



