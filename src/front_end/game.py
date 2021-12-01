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

import traceback

from front_end.util import *
from front_end.run_game import RunGame


class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__( self, agents, display, method, rules, episodes, verbose, multithreaded, startingIndex=0):
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.verbose = verbose
        self.startingIndex = startingIndex
        self.multithreaded = multithreaded
        self.gameOver = False
        self.method = method
        self.episodes = episodes
        self.moveHistory = []
        self.totalAgentTimes = [0 for agent in agents]
        self.totalAgentTimeWarnings = [0 for agent in agents]
        self.agentTimeout = False
        
    def getProgress(self):
        if self.gameOver:
            return 1.0
        else:
            return self.rules.getProgress(self)

    def _agentCrash( self, agentIndex, quiet=False):
        "Helper method for handling agent crashes"
        if not quiet: traceback.print_exc()
        self.gameOver = True
        self.agentCrashed = True
        self.rules.agentCrash(self, agentIndex)


    def run( self ):
        """
        Creates a RunGame instance which has its run() method called.
        """
        game = RunGame(self)
        return game.games, game.data
