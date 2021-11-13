

class Graph:
    """
    
    """
    
    def __init__(self, env):
        """
        
        """
        self.env = env
        self.graph_edges = self.create_edge_list()
        self.root, self.nodes = self.create_graph()

    def create_edge_list(self):
        graph_edges = []
        for position in range(len(self.env.board)):
            node_edges = []
            if self.env.board[position] != 0:
                for index, action in enumerate(self.env.actions):
                    next_position = position + action
                    valid_position = self.env.verify_position(next_position, index)
                    if valid_position:
                        node_edges.append(next_position)
                    else:
                        node_edges.append(None)

            graph_edges.append(node_edges)
        return graph_edges
            
    def create_nodes(self):
        """
        
        """
        node_list = []
        for index, edge in enumerate(self.graph_edges):
            if edge == []:
                node = None
            else:
                if index == 0:
                    node = Node(index)
                    node.pellet = False
                elif index == 19:
                    node = Node(index)
                    node.ghost = True
                else:
                    node = Node(index)
            node_list.append(node)
                
        return node_list
    
    def create_graph(self):
        """
        
        """
        node_list = self.create_nodes()
        for node, edge in zip(node_list, self.graph_edges):
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
        self.pellet = True
        self.ghost = False
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.position == other.position
        return False
