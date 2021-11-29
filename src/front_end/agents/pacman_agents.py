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

import copy
import numpy as np

from front_end.agents.agent import Agent
from front_end.util import manhattanDistance

from back_end.util.a_star import AStar
from back_end.util.sorts import sort_coordinates
from back_end.reinforcement_learning.qtable import State

class PacmanAgent(Agent):
    
    def __init__(self, index = 0):
        self.index = index
        self.a_star = AStar(None)

    def get_state_representation(self, game, dist_thresh):
        legal_actions = game.state.getLegalPacmanActions()
        pacman_pos = game.state.getPacmanPosition()

        ghost_positions = game.state.getGhostPositions()
        food_positions = game.state.getFood().asList()
        if len(food_positions) > 0:
            _, sorted_food_positions = sort_coordinates(food_positions, pacman_pos)
        
            closest_food_position = [sorted_food_positions[0]]
            cpd = self.get_closest_position_direction(pacman_pos, closest_food_position, game)
        else:
            cpd = 4     # Terminal state
        north, east, south, west = self.get_pacman_position_binary_rep(legal_actions)
        
        dist = self.manhattan(pacman_pos, ghost_positions[0])
        cgd = self.get_closest_position_direction(pacman_pos, ghost_positions, game)
        if dist < dist_thresh:
            prox = 0
        else:
            prox = 1

        state = State(north, east, south, west, cpd, cgd, prox)
        return state

    def manhattan(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def get_pacman_position_binary_rep(self, legal_actions):
        north = 0
        east = 0
        south = 0
        west = 0
        for action in legal_actions:
            if action == "North": north = 1
            elif action == "East": east = 1
            elif action == "South": south = 1
            elif action == "West": west = 1
            else: continue
        return north, east, south, west

    def get_closest_position_direction(self, pacman_position, positions, game):
        closest = np.inf
        closest_path = None
        game_copy = copy.deepcopy(game)
        for pos in positions:
            new_game = copy.deepcopy(game_copy)
            path = self.a_star.a_star(pacman_position, pos, new_game)
            if path is None: return 4
            path_len = len(path)
            if path_len <= closest:
                closest = path_len
                closest_path = path
        
        closest_direction = self.a_star.get_direction_of_a_star(closest_path, game_copy)
        return closest_direction

    def get_reward(self, GameStateData):
        return GameStateData.scoreChange