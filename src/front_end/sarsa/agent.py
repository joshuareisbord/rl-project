# keyboardAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import numpy as np
from back_end.util.a_star import AStar
from front_end.game.game import Agent, Directions
# from game import Directions
import random
import copy
from back_end.util.sorts import sort_coordinates

class SarsaAgent(Agent):
    """
    An agent controlled by the keyboard.

    Note: This is a hack way of getting it done, but it works.
    
    Legal Actions from: state.getLegalPacmanActions()
    Pacman Position: state.getPacmanPosition()
    Ghost Positions: state.getGhostPositions() or state.getGhostPositions(agentIndex)

    Next PacMan state after action from: state.generatePacmanSuccessor(action)

    Possible Directions: {Directions.STOP, Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST}
    """

    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []
        self.a_star = AStar(None)

    def getAction(self, state):
        """
        Function called when it's the agent's turn to move.

        :return move: The move to be made {'Left', 'Right', 'Up', 'Down'}
        """

        legal_actions = state.getLegalPacmanActions()
        move = self.getMove(legal_actions)

        return move

    def getMove(self, legal_actions):
        move = None
        
        # If no action is chosen, then STOP will be returned to avoid None type.
        if move == None:
            move = Directions.STOP
        return move
    
    def get_state_representation(self, state):
        legal_actions = state.getLegalPacmanActions()
        pacman_pos = state.getPacmanPosition()

        ghost_positions = state.getGhostPositions()
        food_positions = state.getFood().asList()
        _, sorted_food_positions = sort_coordinates(food_positions, pacman_pos)
        closest_food_position = [sorted_food_positions[0]]
        north, east, south, west = self.get_pacman_position_binary_rep(legal_actions)
        cpd = self.get_closest_position_direction(pacman_pos, closest_food_position, state)
        cgd = self.get_closest_position_direction(pacman_pos, ghost_positions, state)
        state = (north, east, south, west, cpd, cgd)
        return state

    def get_pacman_position_binary_rep(self, legal_actions):
        north = east = south = west = 0
        for action in legal_actions:
            if action == "North": north += 1
            elif action == "East": east += 1
            elif action == "South": south += 1
            elif action == "West": west += 1
            else: continue
        return north, east, south, west

    def get_closest_position_direction(self, pacman_position, positions, state):
        closest = np.inf
        closest_path = None
        for pos in positions:
            state_copy = copy.deepcopy(state)
            path = self.a_star.a_star(pacman_position, pos, state_copy)
            path_len = len(path)
            if path_len <= closest:
                closest = path_len
                closest_path = path
        closest_direction = self.a_star.get_direction_of_a_star(closest_path, state)
        return closest_direction

    def get_reward(self, GameStateData):
        return GameStateData.scoreChange
