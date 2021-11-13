import numpy as np

from state import State, States
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
                
    def get_direction_of_a_star(self, path):
        """
        Purpose:
            Gets the direction of the next step in the given path.
            The first position in the path is the current position.
            Thus we are only concerned with the first to indexes of path.
        Args:
            path - the optimal path to some position from a starting position
        Returns:
            The direction of the next step to follow the path.
        """
        starting_node_index = path[0]
        next_node_index = path[1]
        starting_node = self.graph.nodes[starting_node_index]
        next_node = self.graph.nodes[next_node_index]
        if starting_node.north == next_node: return 0
        if starting_node.east == next_node: return 1
        if starting_node.south == next_node: return 2
        if starting_node.west == next_node: return 3

    def get_reward(self, position, action):
        """
        Purpose:
            Function gets the reward after taking an action.
        Args:
            position - the index 
        Action is an index
        """

        node = self.env.nodes[position]
        valid_action = self.verify_position(position, action)
        if valid_action:
            next_position = position + self.env.actions[action]
            next_node = self.env.nodes[next_position]
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
                    path = self.a_star(pac_man_position, end)
                    if (len(path) < closest[1]):
                        direction = self.get_direction_of_a_star(path)
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
                    path = self.a_star(pac_man_position, end)
                    direction = self.get_direction_of_a_star(path)
                    return direction

if __name__ == '__main__':
    length = 5
    width = 4
    board = [
            1, 1, 1, 1,
            1, 0, 0, 1,
            1, 0, 1, 1,
            1, 0, 0, 1,
            1, 1, 1, 1
            ]
    
    actions = [-4, 1, 4, -1] # [ north, east, south, west] (index modifiers for the board)
    bounds = [0, [4, 8, 12, 16, 20], 20, [-1, 3, 7, 11, 15]] # [ north, [east], south, [west] ]

    e = Environment(length, width, board, bounds, actions)

    path = e.a_star(0, 19)
    print(path)
    direction = e.get_direction_of_a_star(path)
    print(direction)
    s = States()
    print(s)




    
