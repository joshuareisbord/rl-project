import numpy as np

from state import State, States
from graph import Graph
from graph import Node
from back_end.util.a_star import AStar


class Environment:
    """
    
    """

    def __init__(self, length, width, board, bounds, actions):
        """
        
        """
        self.length = length
        self.width = width
        self.board = board
        self.north_bounds = bounds[0]
        self.east_bounds = bounds[1]
        self.south_bounds = bounds[2]
        self.west_bounds = bounds[3]
        self.actions = actions
        self.graph = Graph(self)
        
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
        node = self.graph.nodes[position]
        if action == 0:     
            if node.north: return True
        elif action == 1:
            if node.east: return True
        elif action == 2:
            if node.south: return True
        elif action == 3:
            if node.west: return True
        return False

    def get_reward(self, position, action):
        """
        Purpose:
            Function gets the reward after taking an action.
        Args:
            position - the index 
        Action is an index
        """
        node = self.graph.nodes[position]
        valid_action = self.verify_position(position, action)
        if valid_action:
            next_position = position + self.graph.actions[action]
            next_node = self.graph.nodes[next_position]
            if next_node.ghost:
                return -10
            else:
                if next_node.pellet:
                    return 1
                else:
                    return -0.5
        return -0.5
    
    def get_next_state(self, pac_man_position, action):
        """
        Returns state hash to look up the states value in the q table.
        """
        node = self.graph.nodes[pac_man_position]
        pac_man_next_position = pac_man_position + self.actions[action]
        next_node = self.graph.nodes[pac_man_next_position]
        state = []
        
        if next_node == None:
            return state, pac_man_position
        
        for index, _ in enumerate(self.actions):
            valid = self.verify_position(pac_man_next_position, index)
            if valid:
                state.append(1)
            else:
                state.append(0)
        state.append(self.get_dir_closest_pellet(pac_man_next_position))
        # Change here if more ghosts are added.
        state.append(self.get_dir_ghost(pac_man_next_position))
        state = State(state[0], state[1], state[2], state[3], state[4], state[5])
        state_hash = state.__hash__()
        return state_hash, pac_man_next_position
        
    def get_dir_closest_pellet(self, pac_man_position):
        """
        Purpose:
            Function gets the closest pellet to pac_man and 
            calculates its relative direction to pac_man
        Args:
            pac_man_position - the index of pac_man's position in the graph 
        Returns: 
            The direction of the pellet (0-3)
        """

        closest = [None, None, np.inf]
        for end in range(len(self.board)):
            node = self.graph.nodes[end]
            if node is not None:
                if node.pellet:
                    # a star
                    path = self.a_star.a_star(pac_man_position, end)
                    if (len(path) < closest[1]):
                        direction = self.a_star.get_direction_of_a_star(path)
                        closest = [node, direction, len(path)]
                
        return direction

    def get_dir_ghost(self, pac_man_position):
        """
        Purpose:
            Function finds the position of the ghost and 
            computes its relative position to pac_man
        Args:
            pac_man_position - the index of pac_man's position in the graph 
        Returns: 
            The direction of the ghost(0-3)
        """

        for end in range(len(self.board)):
            node = self.graph.nodes[end]
            if node is not None:
                if node.ghost:
                    path = self.a_star_a_star(pac_man_position, end)
                    direction = self.a_star_get_direction_of_a_star(path)
                    return direction
