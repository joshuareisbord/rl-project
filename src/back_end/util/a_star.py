import numpy as np
import copy 

class AStar:
    """
    AStar class
    """

    def __init__(self):
        """
        Default constructor.
        """
        pass
    
    def a_star(self, start, end, game):
        """
        Purpose:
            Performes A Star Algorithm given a starting and ending position.
            An AStarNode node is created for the start and end position. It then checks
            which direction from the start is the closest to the end. It then creates a 
            new AStarNode at that position and makes the previous position its parent.
            This process is repeated until the new AStarNode created is equal to the 
            end node. Then we loop backwards through the nodes parent attribute to get 
            the path from the start to the end.
        Args:
            self - class instance.
            start - the starting position in the 1D board representation.
            end - the ending position in the 1D board representation.
        Returns:
            A 1D array of the shortest path from the start to the end position. Each index
            of the path represents a position on the 1D board representation.
        Reference:
            This algorithm was adapted from the following article:
            https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
        """
        # Converts end coordinates to ints.
        end = (int(end[0]), int(end[1]))
        # Setup start and end nodes.
        start_node = AStarNode(start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = AStarNode(end)
        end_node.g = end_node.h = end_node.f = 0
        end_node_x = end_node.position[0]
        end_node_y = end_node.position[1]
        
        open_list = []
        closed_list = []
        game_copy = copy.deepcopy(game)
        
        open_list.append(start_node)
        # Loops until open_list is empty
        while open_list != []:
            current_node = open_list[0]
            
            current_index = 0
            # Sets the node closest to current node as the new current node.
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    # Used to update pacmans position so the call to getLegalPacmanActions
                    # will return the correct actions for the current node.
                    game_copy.state.data.agentMoved = 0
            
            open_list.pop(current_index)
            closed_list.append(current_node)
            # Current node is the end node.
            if current_node == end_node:
                path = []
                current = current_node
                # Traverse and save path.
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                # Return path from the start to the end.
                return path[::-1]

            children = []
            # Get actions for current position.
            actions = self.get_actions(game_copy.state, current_node.position)
            # Removes 'Stop' from actions if present.
            if 'Stop' in actions:
                actions.remove('Stop')
            # Loops through each action and creates a new node for each.
            # Adds the new node to children array.
            for index, action_name in enumerate(actions):
                action = self.get_action_coordinates(action_name)
                new_node_position = tuple(np.array(current_node.position) + action)
                new_node = AStarNode(new_node_position, current_node, action_name)
                children.append(new_node)
            # Loops through each child.
            for child in children:
                # Loops through each node in closed_list.
                for closed_child in closed_list:
                    # If the child is in the closed_list skip to next child.
                    if child == closed_child:
                        continue
                child_x = child.position[0]
                child_y = child.position[1]
                child_to_cur_dist = abs(child_x - current_node.position[0]) + abs(child_y - current_node.position[1])
                child_to_end_dist = abs(child_x - end_node_x) + abs(child_y - end_node_y)
                # Updates the heuristics for the child node.
                child.g = current_node.g + child_to_cur_dist
                child.h = child_to_end_dist
                child.f = child.g + child.h
                # Loops through each node in the open list.
                for open_node in open_list:
                    # If the child is in the open list and has a higher distance, g.
                    # Skip to the next child.
                    if child == open_node and child.g > open_node.g:
                        continue
                # Adds child to open_list
                open_list.append(child)
               
    def get_actions(self, game, position):
        """
        Purpose:
            Sets the position of pacman in the game object to the current nodes position.
            Then gets the legal actions of the given position.
        Args:
            self - class instance.
            game - the game state object.
            position - the position of the current node (x, y)
        Returns:
            A list of actions that can be taken in the current position.
        """
        game.data.agentStates[0].configuration.pos = position
        actions = game.getLegalPacmanActions()
        return actions

    def get_direction_of_a_star(self, path, game):
        """
        Purpose:
            Gets the direction of the next step in the given path.
            The first position in the path is the current position.
            Thus we are only concerned with the first two indexes of the path.
        Args:
            self - class instance.
            path - the optimal path to some position from a starting position.
            game - the game state object.
        Returns:
            The direction of the next step to follow the path (0-3). Returns 4 if
            in a terminal state.
        """
        # Checks if that path is one. i.e., the start and end positions given to 
        # A* were the same.
        if len(path) == 1:
            return 4
        # Get the starting position and the next position in the path.
        starting_pos = path[0]
        next_pos = path[1]
        # Get the available actions for the starting position.
        actions = game.state.getLegalPacmanActions()
        # Removes stop from list of actions.
        if 'Stop' in actions:
            actions.remove('Stop') 
        # Loops through each action to determine the action taken
        # from starting_pos to get next_pos.
        for action in actions:
            # Get the action in terms of (x, y).
            action_cord = self.get_action_coordinates(action)
            # Apply action to starting_pos
            pos_after_action = tuple(np.array(starting_pos) + action_cord)
            if pos_after_action == next_pos:
                if action == 'North': return 0
                if action == 'East': return 1
                if action == 'South': return 2
                if action == 'West': return 3

    @staticmethod
    def get_action_coordinates(action):
        """
        Purpose:
            Gets the (x, y) coordinates of a given action.
        Args:
            action - the action to get the coordinates of.
        Returns:
            A np array of the coordinates.
        """
        if action == "North":
            return np.array([0, 1])
        elif action == "East":
            return np.array([1, 0])
        elif action == "South":
            return np.array([0, -1])
        elif action == "West":
            return np.array([-1, 0])
        elif action == "Stop":
            return np.array([0, 0])
        else:
            raise ValueError(f"{action} is not a valid action.")

class AStarNode:
    """
    A* Node class.
    """    

    def __init__(self, position, parent=None, action_name=None):
        """
        Default constructor for A* Node class.
        """
        self.position = position
        self.parent = parent
        self.action_name = action_name
        self.g = 0
        self.h = 0
        self.f = 0
        
    def __eq__(self, other):
        """ 
        Evaluates AStarNode objects based on their position.
        """
        if isinstance(other, AStarNode):
            return np.all(self.position == other.position)
        return False