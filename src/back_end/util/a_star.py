import numpy as np

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
        self.position_mapping = self.get_position_coordinates(self.env.length, self.env.width)
        
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
    
    def a_star(self, start, end, state):
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
        start_node = AStarNode(start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = AStarNode(end)
        end_node.g = end_node.h = end_node.f = 0

        end_node_x = end_node.position[0]
        end_node_y = end_node.position[1]

        open_list = []
        closed_list = []

        open_list.append(start_node)

        while open_list != []:

            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            
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
            actions = state.getLegalPacmanActions()
            for index, action in enumerate(actions):
                action = self.get_action_coordinates(action)
                new_node_position = np.array(current_node.position) + action
                new_node = AStarNode(new_node_position, current_node)
                children.append(new_node)

            for node in children:
                for closed_n in closed_list:
                    if node == closed_n:
                        continue
                
                node.g = current_node.g + 1
                node_x = node.position[0]
                node_y = node.position[1]
                node.h += abs(node_x - end_node_x) + abs(node_y - end_node_y)
                node.f = node.g + node.h

                for open_n in open_list:
                    if node == open_n and node.g > open_n.g:
                        continue

                open_list.append(node)
                
    def get_direction_of_a_star(self, path):
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
        starting_node_index = path[0]
        next_node_index = path[1]
        starting_node = self.env.nodes[starting_node_index]
        next_node = self.env.nodes[next_node_index]
        if starting_node.north == next_node: return 0
        if starting_node.east == next_node: return 1
        if starting_node.south == next_node: return 2
        if starting_node.west == next_node: return 3

    @staticmethod
    def get_action_coordinates(action):
        if action == "North":
            return np.array([-1, 0])
        elif action == "East":
            return np.array([0, 1])
        elif action == "South":
            return np.array([1, 0])
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

    def __init__(self, position, parent=None):
        """
        Default constructor for A* Node class.
        """
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        
    def __eq__(self, other):
        """ 
        Evaluates AStarNode objects based on their position.
        """
        if isinstance(other, AStarNode):
            return self.position == other.position
        return False