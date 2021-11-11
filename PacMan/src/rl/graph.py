
class Graph:
    def __init__(self, board_arr):
        self.actions = [-4, 1, 4, -1] # North, East, South, West
        self.board_arr = board_arr
        self.edges = self.initialize_edge_table()
        self.east_bounds = [4, 8, 12, 16, 20]
        self.west_bounds = [-1, 3, 7, 11, 15]
        self.create_edge_list()
        self.root, self.nodes = self.create_graph()

    def initialize_edge_table(self):
        edges = []
        for _ in self.board_arr:
            edges.append([])
        return edges

    def create_edge_list(self):
        for position in range(len(self.board_arr)):
            if self.board_arr[position] == 0: continue
            n, e, s, w = self.get_all_valid_actions(position)
            self.edges[position].append(n[1])
            self.edges[position].append(e[1])
            self.edges[position].append(s[1])
            self.edges[position].append(w[1])
            
    def create_nodes(self):
        node_list = []
        for index, edge in enumerate(self.edges):
            if edge == []:
                node_list.append(None)
            else:
                if index == 0:
                    node = Node(index)
                elif index == 19:
                    node = Node(index)
                else:
                    node = Node(index)
                node_list.append(node)
                
        return node_list
    
    def create_graph(self):
        node_list = self.create_nodes()
        for node, edge in zip(node_list, self.edges):
            if node != None:
                if edge[0] != None: # North
                    north_node = node_list[edge[0]]
                    node.north = north_node
                if edge[1] != None: # East
                    east_node = node_list[edge[1]]
                    node.east = east_node
                if edge[2] != None: # South
                    south_node = node_list[edge[2]]
                    node.south = south_node
                if edge[3] != None: # West
                    west_node = node_list[edge[3]]
                    node.west = west_node
        return node_list[0], node_list


    def get_all_valid_actions(self, position):
        n = (False, None)
        e = (False, None)
        s = (False, None)
        w = (False, None)
        for index, action in enumerate(self.actions):
            next_position = position + action
            if index == 0:
                if next_position >= 0:
                    if self.board_arr[next_position] != 0:
                        n = (True, next_position) 
            if index == 1:
                if next_position not in self.east_bounds:
                    if self.board_arr[next_position] != 0:
                        e = (True, next_position)
            if index == 2:
                if next_position < 20:
                    if self.board_arr[next_position] != 0:
                        s = (True, next_position)
            if index == 3:
                if next_position not in self.west_bounds:
                    if self.board_arr[next_position] != 0:
                        w = (True, next_position)
        return n, e, s, w

class Node:

    def __init__(self, position, parent=None, north=None, south=None, east=None, west=None):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.position == other.position
        return False

if __name__ == '__main__':
    board = [
            1, 1, 1, 1,
            1, 0, 0, 1,
            1, 0, 1, 1,
            1, 0, 0, 1,
            1, 1, 1, 1
        ]
    b = Graph(board)
