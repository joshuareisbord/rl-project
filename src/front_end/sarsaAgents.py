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


from game import Agent
from game import Directions
import random

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
