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
        pacman_pos = game.state.getPacmanPosition()

        
        
        north, east, south, west = self.get_pacman_representation(game)
        closest_food_direction = self.get_food_representation(game, pacman_pos)
        closest_ghost_direction, proximity = self.ghost_representation(game, pacman_pos, dist_thresh)
        
        state = State(north, east, south, west, closest_food_direction, closest_ghost_direction, proximity)
        return state


    def get_pacman_representation(self, game):
        legal_actions = game.state.getLegalPacmanActions()
        north = east = south = west = 0
        for action in legal_actions:
            if action == "North": north = 1
            elif action == "East": east = 1
            elif action == "South": south = 1
            elif action == "West": west = 1
            else: continue
        return north, east, south, west

    def get_food_representation(self, game, pacman_pos):
        food_positions = game.state.getFood().asList()
        if len(food_positions) > 0:
            _, sorted_food_positions = sort_coordinates(food_positions, pacman_pos)
        
            closest_food_position = [sorted_food_positions[0]]
            return self.get_closest_position_direction(pacman_pos, closest_food_position, game)
        else:
            return 4     # Terminal state

    def ghost_representation(self, game, pacman_pos, dist_thresh):
        ghost_positions = game.state.getGhostPositions()
        dist = manhattanDistance(pacman_pos, ghost_positions[0])
        closest_ghost_direction = self.get_closest_position_direction(pacman_pos, ghost_positions, game)

        if dist < dist_thresh:
            proximity = 0
        else:
            proximity = 1

        return closest_ghost_direction, proximity


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