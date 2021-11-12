import numpy as np

from state import State
from graph import Graph
from graph import Node

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
        self.rewards = None
        self.graph = Graph(self)
        self.position_mapping = self.get_position_coordinates(self.length, self.width)
    
    @staticmethod
    def get_position_coordinates(length, width):
        coordinates = []
        for x in range(length):
            for y in range(width):
                coordinates.append((x, y))
        return coordinates
            
    def verify_position(self, position, action):
        """
        Purpose:
            Verifies if the provided position can be reached after taking an action.
        Args:
            position - the new position. The index of self.board
            action - the action that was taken.
        Returns:
            A boolean. True if the position is valid. False otherwise.
        """
        if action == 0:     
            if position >= self.north_bounds:       # Checks North bound.
                if self.board[position] != 0:       # Checks if position is in a wall.
                    return True
        elif action == 1:
            if position not in self.east_bounds:    # Checks East bound. 
                if self.board[position] != 0:       # Checks if position is in a wall. 
                    return True
        elif action == 2:
            if position < self.south_bounds:        # Checks South bound.
                if self.board[position] != 0:       # Checks if position is in a wall.
                    return True
        elif action == 3:
            if position not in self.west_bounds:    # Checks West bound.
                if self.board[position] != 0:       # Checks if position is in a wall.
                    return True
        return False

    def a_star(self, start, end):
        """
        
        """
        start_node = Node(start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(end)
        end_node.g = end_node.h = end_node.f = 0

        end_node_x = self.position_mapping[end_node.position][0]
        end_node_y = self.position_mapping[end_node.position][1]


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
            for index, action in enumerate(self.actions):

                new_node_position = current_node.position + action
                valid_new_position = self.verify_position(new_node_position, index)
                
                if valid_new_position:
                    new_node = Node(new_node_position, current_node)
                    children.append(new_node)

            
            for node in children:
                for closed_n in closed_list:
                    if node == closed_n:
                        continue
                
                node.g = current_node.g + 1
                node_x = self.position_mapping[node.position][0]
                node_y = self.position_mapping[node.position][1]
                node.h += abs(node_x - end_node_x) + abs(node_y - end_node_y)
                node.f = node.g + node.h

                for open_n in open_list:
                    if node == open_n and node.g > open_n.g:
                        continue

                open_list.append(node)
                


                
        # def generate_states(self):
    #     """
        
    #     """
    #     # states = []
    #     walls = []
    #     non_walls = []
    #     for elem in self.board:
    #         if elem == 0:
    #             walls.append(elem)
    #         else:
    #             non_walls.append(elem)

    #     for i in range(2**len(non_walls)):
    #         pellet_s = list(bin(i)[2:].zfill(len(non_walls)))
               
    #         for wall in walls:
    #             pellet_s.insert(wall, 0)
    #             for p in range(len(self.board)):
    #                 for g in range(len(self.board)):
    #                     if not (p in walls or g in walls):
    #                         print([p,g,pellet_s])
    #                         self.states.append([p,g,pellet_s])

    

if __name__ == '__main__':
    length = 5
    width = 4
    board = [
            1, 1, 1, 1,
            1, 0, 0, 1,
            1, 0, 1, 1,
            1, 0, 0, 1,
            1, 1, 1, 1]
    
    actions = [-4, 1, 4, -1]
    bounds = [0, [4, 8, 12, 16, 20], 20, [-1, 3, 7, 11, 15]]

    e = Environment(length, width, board, bounds, actions)

    path = e.a_star(0, 19)
    print(path)


    
