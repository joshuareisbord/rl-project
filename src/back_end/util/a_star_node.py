
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