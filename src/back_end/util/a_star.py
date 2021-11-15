from a_star_node import AStarNode

class AStar:

    def __init__(self, environment):
        self.env = environment
        self.position_mapping = self.get_position_coordinates(self.env.length, self.env.width)
        
    @staticmethod
    def get_position_coordinates(length, width):
        coordinates = []
        for x in range(length):
            for y in range(width):
                coordinates.append((x, y))
        return coordinates
    
    def a_star(self, start, end):
        """
        Performes A Star Algorithm, on an environment's graph.
        Returns shortest dist to path
        """
        start_node = AStarNode(start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = AStarNode(end)
        end_node.g = end_node.h = end_node.f = 0

        end_node_x = self.env.position_mapping[end_node.position][0]
        end_node_y = self.env.position_mapping[end_node.position][1]

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
            for index, action in enumerate(self.env.actions):

                new_node_position = current_node.position + action
                valid_new_position = self.env.verify_position(new_node_position, index)
                
                if valid_new_position:
                    new_node = AStarNode(new_node_position, current_node)
                    children.append(new_node)

            for node in children:
                for closed_n in closed_list:
                    if node == closed_n:
                        continue
                
                node.g = current_node.g + 1
                node_x = self.env.position_mapping[node.position][0]
                node_y = self.env.position_mapping[node.position][1]
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
        starting_node = self.env.graph.nodes[starting_node_index]
        next_node = self.env.graph.nodes[next_node_index]
        if starting_node.north == next_node: return 0
        if starting_node.east == next_node: return 1
        if starting_node.south == next_node: return 2
        if starting_node.west == next_node: return 3