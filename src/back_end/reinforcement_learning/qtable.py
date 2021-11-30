import numpy
import json
import os

class State:
    """
    Individual State object.
    """
    
    def __init__(self, north, east, south, west, closest_food_dir, closest_ghost_dir, ghost_in_prox):
        """
        Initializes the state.

        :param north: The north direction.
        :param east: The east direction.
        :param south: The south direction.
        :param west: The west direction.
        :param closest_food_dir: The direction to the closest pellet.
        :param closest_ghost_dir: The direction to the closest ghost.
        """

        if north not in list(range(2)):
            raise ValueError(f"Invalid north direction {north}.")
        if east not in list(range(2)):
            raise ValueError(f"Invalid east direction {east}.")
        if south not in list(range(2)):
            raise ValueError(f"Invalid south direction {south}.")
        if west not in list(range(2)):
            raise ValueError(f"Invalid west direction {west}.")
        if closest_food_dir not in list(range(5)):
            raise ValueError(f"Invalid closest pellet direction {closest_food_dir}.")
        if closest_ghost_dir not in list(range(5)):
            raise ValueError(f"Invalid closest ghost direction {closest_ghost_dir}.")
        if ghost_in_prox not in list(range(2)):
            raise ValueError(f"Invalid proximity bit {ghost_in_prox}.")

        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.closest_food_dir = closest_food_dir
        self.closest_ghost_dir = closest_ghost_dir
        self.ghost_in_prox = ghost_in_prox
        

    def as_tuple(self):
        """
        Function returns a tuple representation of the state.
        :return: A tuple representation of the state.
        """
        return (self.north, self.east, self.south, self.west, self.closest_food_dir, self.closest_ghost_dir, self.ghost_in_prox)

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
        and self.ghost_in_prox == other.ghost_in_prox \

    def __repr__(self):
        """
        Function returns a string representation of the state.
        :return: A string representation of the state.
        """
        return str((self.north, self.east, self.south, self.west, self.closest_food_dir, self.closest_ghost_dir, self.ghost_in_prox))

    def __hash__(self):
        """
        Function returns a hash of the state.
        :return: A hash of the state.
        """
        return hash((self.north, self.east, self.south, self.west, self.closest_food_dir, self.closest_ghost_dir, self.ghost_in_prox))

class QTable:

    def __init__(self):
        self.table = {}
        self.actions = ['North', 'East', 'South', 'West']
        self.num_actions = len(self.get_actions)
        

    def init_table(self):
        """
        Generates all possible states.
        :return: None.
        """
        for n in range(2): # can go north: 1, cant go north: 0
            for e in range(2): # can go south: 1, cant go south: 0
                for s in range(2): # can go east: 1, cant go east: 0
                    for w in range(2): # can go west: 1, cant go west: 0
                        for p_dir in range(5): # player direction: 0 = north, 1 = east, 2 = south, 3 = west
                            for g_dir in range(5): # ghost direction: 0 = north, 1 = east, 2 = south, 3 = west
                                for prox in range(2):   # ghost proximity: 0 = not in proximity, 1 = in proximity
                                    state = State(n, e, s, w, p_dir, g_dir, prox)
                                    self.table[hash(state)] = [0] * self.num_actions  # create an entry in the Q-table for the state

    def get_table(self):
        """
        Gets the whole Q-table.
        :return: Q-table dictionary
        """
        return self.table

    def get_actions(self):
        """
        Get all actions.
        :return: list of all actions
        """
        return self.actions

    def get_action_value(self, state: State, action):
        """
        Gets Q-value of a specific state given an action
        """
        idx = self.get_actions().index(action)
        return self.table[hash(state)][idx]

    def get_state_values(self, state: State):
        """
        Get Q-values for the given state object.
        :param state: current state (instance of State class)
        :return: Q-values for the current state
        """
        return self.table[hash(state)]

    def update_state(self, state: State, action, value):
        """
        Updates the state action pair to the given value.
        """
        idx = self.get_actions().index(action)
        self.table[hash(state)][idx] = value

    def save(self, filename='q_table'):
        """
        Saves the Q-Table to a file.
        :param filename: name of the file
        """
        
        file = os.getcwd() + "/back_end/q_tables/" + filename + ".json"
        with open(file, 'w') as f:
            json.dump(self.table, f, indent=4)

    def load(self, filename='q_table'):
        """
        Loads the Q-Table from a file.
        :param filename: name of the file
        """
        file = os.getcwd() + "/back_end/q_tables/" + filename + ".json"
        if os.path.isfile(file):
            with open(file, 'r') as f:
                raw_table = json.load(f)
                tmp = {}
                for key in raw_table:
                    tmp[int(key)] = raw_table[key] # make sure key is an integer
                self.table = tmp
        else:
            self.init_table()
            self.save()

    def __str__(self):
        string = ""
        for key in self.table.keys():
            string += str(key) + " : " + str(self.table[key]) + "\n"
        return string
        