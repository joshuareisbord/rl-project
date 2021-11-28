import numpy as np
import time
from queue import PriorityQueue
import copy 

class AStar:
    """
    AStar class
    """

    def __init__(self, environment):
        """
        Purpose:
            Default constructor. Set environment and position mapping attributes.
        Args:
            self - class instance.
            environment - instance of the Environment class.
        """
        self.env = environment
        # self.position_mapping = self.get_position_coordinates(self.env.length, self.env.width)
        
    @staticmethod
    def get_position_coordinates(length, width):
        """
        Purpose:
            Gets a 2D representation of the board. Is used to calculate Manhattan distance in
            a star method.
        Args:
            length - the length of the board.
            width - the width of the board.
        Returns:
            A 2D array of coordinates.
        """
        coordinates = []
        for x in range(length):
            for y in range(width):
                coordinates.append((x, y))
        return coordinates
    
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
        """
        end = (int(end[0]), int(end[1]))

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
        while open_list != []:
            current_node = open_list[0]
            
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    game_copy.state.data.agentMoved = 0
                    # game_copy.display.update( game_copy.state.data )
            
            open_list.pop(current_index)
            closed_list.append(current_node)
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            children = []
            actions = self.get_actions(game_copy.state, current_node.position)
            if 'Stop' in actions:
                actions.remove('Stop')
            for index, action_name in enumerate(actions):
                action = self.get_action_coordinates(action_name)
                new_node_position = tuple(np.array(current_node.position) + action)
                new_node = AStarNode(new_node_position, current_node, action_name)
                children.append(new_node)

            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                child_x = child.position[0]
                child_y = child.position[1]
                child_to_cur_dist = abs(child_x - current_node.position[0]) + abs(child_y - current_node.position[1])
                child_to_end_dist = abs(child_x - end_node_x) + abs(child_y - end_node_y)
                
                child.g = current_node.g + child_to_cur_dist
                child.h = child_to_end_dist
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)
               
    def get_actions(self, game, position):
        game.data.agentStates[0].configuration.pos = position
        actions = game.getLegalPacmanActions()
        return actions


   
    def get_direction_of_a_star(self, path, game):
        """
        Purpose:
            Gets the direction of the next step in the given path.
            The first position in the path is the current position.
            Thus we are only concerned with the first to indexes of path.
        Args:
            self - class instance.
            path - the optimal path to some position from a starting position
        Returns:
            The direction of the next step to follow the path.
        """
        if len(path) == 1:
            return 4
        starting_node_index = path[0]
        next_node_index = path[1]
        actions = game.state.getLegalPacmanActions()
        if 'Stop' in actions:
            actions.remove('Stop') 
        for action in actions:
            action_cord = self.get_action_coordinates(action)
            new_node_position = tuple(np.array(starting_node_index) + action_cord)
            if new_node_position == next_node_index:
                if action == 'North': return 0
                if action == 'East': return 1
                if action == 'South': return 2
                if action == 'West': return 3

    @staticmethod
    def get_action_coordinates(action):
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
            print("Not a valid action.")
            exit(1)

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