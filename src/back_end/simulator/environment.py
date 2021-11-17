import numpy as np

from state import State, States
from graph import Node
from back_end.util.a_star import AStar


class Environment:
    """
    
    """

    def __init__(self, graph):
        """
        
        """
        self.nodes = graph.nodes
        self.actions = graph.actions
        self.a_star = AStar(self)
        
    def verify_position(self, position, action):
        """
        Purpose:
            Verifies if the provided position can be reached after taking an action.
        Args:
            position - the new position. The index of self.board.
            action - the action that was taken.
        Returns:
            A boolean. True if the position is valid. False otherwise.
        """
        node = self.nodes[position]
        if action == 0:     
            if node.north: return True
        elif action == 1:
            if node.east: return True
        elif action == 2:
            if node.south: return True
        elif action == 3:
            if node.west: return True
        return False
