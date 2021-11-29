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
    """
    PacmanAgent class
    """
    
    def __init__(self, index = 0):
        """
        Default constructor.
        """
        self.index = index
        self.a_star = AStar()

    def get_reward(self, GameStateData):
        """
        Purpose:
            Gets the reward of the current state.
            # TODO
        Args:
            self - class instance.
            GameStateData - game state data object.
        Returns:
            The reward.
        """
        return GameStateData.scoreChange

    def get_state_representation(self, game, dist_thresh):
        """
        Purpose:
            Gets the state representation of the current game state.
            This representation is used to query the QTable.
        Args:
            self - class instance.
            game - the game state object.
            dist_thresh - the specified threshold used in determining
                          if the ghost is with a distance from pacman.
        Returns:
            The state object.
        """
        # Get Pacmans current position.
        pacman_pos = game.state.getPacmanPosition()
        # Binary representation of available actions Pacman can take.
        north, east, south, west = self.get_pacman_representation(game)
        # Direction of the closest food.
        closest_food_direction = self.get_food_representation(game, pacman_pos)
        # Direction of the closest ghost and if its within the distance threshold.
        closest_ghost_direction, proximity = self.ghost_representation(game, pacman_pos, dist_thresh)
        # Get state object.
        state = State(north, east, south, west, closest_food_direction, closest_ghost_direction, proximity)
        return state


    def get_pacman_representation(self, game):
        """
        Purpose:
            Gets the binary representation of the actions Pacman can take
            in his current position.
        Args:
            self - class instance.
            game - the game state object.
        Returns:
            Binary values for north, east, south, west respectively.
            E.g., 1, 1, 0, 0 is returned if Pacman can only move
            north and east.
        """
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
        """
        Purpose:
            Gets the direction of the closest food.
            If there is no food left, pacman won and is currently
            in a terminal state.
        Args:
            self - class instance.
            game - the game state object.
            pacman_pos - pacmans current position in terms of x and y
                         coordinates.
        Returns:
            The direction of the closest food (0 - 3). 4 is returned if Pacman is
            in a terminal state.
        """
        # Gets a list of coordinates (x, y) for each food on the board.
        food_positions = game.state.getFood().asList()
        # Check if Pacman is currently in a terminal state.
        if len(food_positions) > 0:
            # Get a sorted list of food positions. Ascending in distance from Pacman.
            _, sorted_food_positions = sort_coordinates(food_positions, pacman_pos)
            closest_food_position = [sorted_food_positions[0]]
            # Get the direction of the closest food position.
            return self.get_closest_position_direction(pacman_pos, closest_food_position, game)
        # Pacman is in a terminal state
        else:
            return 4

    def ghost_representation(self, game, pacman_pos, dist_thresh):
        """
        Purpose:
            Gets the ghost representation for the current state. Gets the direction of the ghost
            and if the ghost is within the distance threshold.
        Args:
            self - class instance.
            game - game state object.
            pacman_pos - Pacmans current position (x, y)
            dist_thresh - the distance threshold.
        Returns:
            The direction of the closest ghost (0 - 3), and if its within a proximity of Pacman (0/1).
        """
        ghost_positions = game.state.getGhostPositions()
        dist = manhattanDistance(pacman_pos, ghost_positions[0])
        closest_ghost_direction = self.get_closest_position_direction(pacman_pos, ghost_positions, game)

        if dist < dist_thresh:
            proximity = 0
        else:
            proximity = 1

        return closest_ghost_direction, proximity


    def get_closest_position_direction(self, pacman_position, positions, game):
        """
        Purpose:
            Gets the direction of the closest position from Pacman.
        Args:
            self - class instance.
            pacman_position - Pacmans current position in terms of (x, y).
            positions - a list of coordinates (x, y).
            game - the game state object.
        Returns:
            The direction of the closest position given (0-3). Returns 4 if in a terminal state.
        """
        closest = np.inf
        closest_path = None
        game_copy = copy.deepcopy(game)
        # Loop through each position to find the closest.
        for pos in positions:
            # Create a new copy of the game so it can be modified by the 
            # A* algorithm without modifying the actual game object.
            new_game = copy.deepcopy(game_copy)
            path = self.a_star.a_star(pacman_position, pos, new_game)
            # Checks if the path is None. If it is either the ghost and pacman
            # have the same position or there is no food left of the board.
            # returns 4 to represent a terminal state.
            if path is None: return 4
            # Check and update closest position/path.
            path_len = len(path)
            if path_len <= closest:
                closest = path_len
                closest_path = path
        # Get the direction of the closest position given the path from Pacman.
        closest_direction = self.a_star.get_direction_of_a_star(closest_path, game_copy)
        return closest_direction
