import numpy as np

from state import State
from graph import Graph
from graph import Node

class Environment:
    """
    
    """

    def __init__(self):
        """
        
        """
        self.board = [
            1, 1, 1, 1,
            1, 0, 0, 1,
            1, 0, 1, 1,
            1, 0, 0, 1,
            1, 1, 1, 1
        ]
        self.position_mapping = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 0), (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 1), (3, 2), (3, 3),
            (4, 0), (4, 1), (4, 2), (4, 3)]

        self.graph = Graph(self.board)
        self.actions = [-4, 1, 4, -1]
        self.rewards = None
    
    def set_state(self):
        pass
    
    def get_state(self):
        pass

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
            for index, action in enumerate(self.graph.actions):

                new_node_position = current_node.position + action
                n = e = s = w = False
                if index == 0:
                    if new_node_position >= 0:
                        if self.graph.board_arr[new_node_position] != 0:
                            n = True 
                if index == 1:
                    if new_node_position not in self.graph.east_bounds:
                        if self.graph.board_arr[new_node_position] != 0:
                            e = True
                if index == 2:
                    if new_node_position < 20:
                        if self.graph.board_arr[new_node_position] != 0:
                            s = True
                if index == 3:
                    if new_node_position not in self.graph.west_bounds:
                        if self.graph.board_arr[new_node_position] != 0:
                            w = True
                
                if n or e or s or w:
                    new_node = Node(new_node_position, current_node)
                    children.append(new_node)
                else: continue

            
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
                


                


    def validate_state(self, state):
        """
        Function will return true if state can be visited, false otherwise.
        """
        pass

    def set_action(self, action, index):
        """
        """
        self.actions[index] = action
    
    def get_action(self, index):
        """
        """
        return self.actions[index]

    def generate_actions(self):
        """
        
        """
        self.actions = np.ndarray([])
        

    def generate_rewards(self):
        """
        
        """
        pass

if __name__ == '__main__':
    # print("here")
    e = Environment()
    path = e.a_star(0, 19)
    print(path)


    
