
class States:
    """
    Generates all possible states possible for the representation.
    """
    def __init__(self):
        """
        Initializes the states.

        :return: None.
        """
        self.__states = {}
        self.__generate_states()

    def states(self):
        """
        Returns all the states.

        :return: A list of all the states.
        """
        return list(self.__states.values())

    def keys(self):
        """
        Returns the keys of the states.

        :return: A list of the keys of the states.
        """
        return self.__states.keys()

    def get_state(self, state_hash):
        """
        Gets a state from the list of states.

        :param state_hash: The hash of the state to get.

        :return: The state.
        """
        return self.__states[state_hash]

    def add_state(self, state):
        """
        Adds a state to the list of states.

        :param state: The state to add.

        :return: True if the state was added, False otherwise.
        """
        self.__states[hash(state)] = state

    def remove_state(self, state):
        """
        Removes a state from the list of states.

        :param state: The state to remove.

        :return: True if the state was removed, False otherwise.
        """
        try:
            del self.__states[hash(state)]
            return True

        except KeyError:
            return False

    def __str__(self):
        """
        Returns a string representation of the states.

        :return: A string representation of the states.
        """
        return str(self.__states.values())

    def __generate_states(self):
        """
        Generates all possible states.

        :return: None.
        """
        for n in range(2): # can go north: 1, cant go north: 0
            for s in range(2): # can go south: 1, cant go south: 0
                for e in range(2): # can go east: 1, cant go east: 0
                    for w in range(2): # can go west: 1, cant go west: 0
                        for p_dir in range(4): # player direction: 0 = north, 1 = east, 2 = south, 3 = west
                            for g_dir in range(4): # ghost direction: 0 = north, 1 = east, 2 = south, 3 = west
                                state = State(n, s, e, w, p_dir, g_dir)
                                self.__states[hash(state)] = state # hash value which is key for the state
                                self.add_state(State(n, e, s, w, p_dir, g_dir))
        return


class State:
    """
    Individual State object.
    """
    
    def __init__(self, north, east, south, west, closest_food_dir, closest_ghost_dir):
        """
        Initializes the state.

        :param north: The north direction.
        :param east: The east direction.
        :param south: The south direction.
        :param west: The west direction.
        :param closest_food_dir: The direction to the closest pellet.
        :param closest_ghost_dir: The direction to the closest ghost.
        """
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.closest_food_dir = closest_food_dir
        self.closest_ghost_dir = closest_ghost_dir

    def __eq__(self, other):
        """
        Function returns True if the states are equal.

        :param other: The other state.

        :return: True if the states are equal.
        """
        return \
        isinstance(other, State) \
        and self.north == other.north \
        and self.east == other.east \
        and self.south == other.south \
        and self.west == other.west \
        and self.closest_food_dir == other.closest_food_dir \
        and self.closest_ghost_dir == other.closest_ghost_dir \

    def __repr__(self):
        """
        Function returns a string representation of the state.

        :return: A string representation of the state.
        """
        return str((self.north, self.east, self.south, self.west, self.closest_food_dir, self.closest_ghost_dir))

    def __hash__(self):
        """
        Function returns a hash of the state.

        :return: A hash of the state.
        """
        return hash((self.north, self.east, self.south, self.west, self.closest_food_dir, self.closest_ghost_dir))
