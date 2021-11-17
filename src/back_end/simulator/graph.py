class Graph:
    """
    Graph class.
    """
    
    def __init__(self, length, width, board, actions, bounds):
        """
        Default constructor for Graph class.
        """
        self.board = board
        self.actions = actions
        self.length = length
        self.width = width
        self.north_bound = bounds[0]
        self.east_bound = bounds[1]
        self.south_bound = bounds[2]
        self.west_bound = bounds[3]
        self.graph_edges = self.create_edge_list()
        self.nodes = self.create_graph()

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

    def create_edge_list(self):
        """
        Purpose:
            Creates a 2D array, each position represents the connections between nodes.
            If a connection exists, the position is added to the list, if not None is added.
            Thus each edge list has 4 indexes, representing North, East, South, West respectively.
        Args:
            self - the class instance.
        Returns:
            A 2D array of the graphs edges.
        """
        graph_edges = []
        # Loop through each position in the 1D board representation.
        for position in range(len(self.board)):
            node_edges = []
            # Check if the position is not a wall.
            if self.board[position] != 0:
                # Loop through each action.
                for index, action in enumerate(self.actions):
                    next_position = position + action
                    # Verify if the next position is a valid position.
                    valid_position = self.verify_position(next_position, index)
                    if valid_position:
                        node_edges.append(next_position)
                    else:
                        node_edges.append(None)
            graph_edges.append(node_edges)
        return graph_edges
            
    def create_nodes(self):
        """
        Purpose:
            Create the GraphNode objects for each position in the 1D board representation.
        Args:
            self - the class instance.
        Returns:
            A list of GraphNode objects.
        """
        node_list = []
        for index, edge in enumerate(self.graph_edges):
            if edge == []:      # Is a wall node.
                node = None
            else:
                if index == 0:  # Remove pellet from pacmans starting position.
                    node = GraphNode(index)
                    node.pellet = False
                else:
                    node = GraphNode(index)
            node_list.append(node)
        return node_list
    
    def create_graph(self):
        """
        Purpose:
            Creates the graph by adding pointers to each node that can be visited.
        Args:
            self - the class instance.
        Returns:
            A list of nodes
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
        return node_list

class GraphNode:

    def __init__(self, position):
        self.position = position
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.pellet = True
    
    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.position == other.position
        return False
