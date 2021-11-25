import numpy
import json
import os
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

        if north not in list(range(2)):
            raise ValueError(f"Invalid north direction {north}.")
        if east not in list(range(2)):
            raise ValueError(f"Invalid east direction {east}.")
        if south not in list(range(2)):
            raise ValueError(f"Invalid south direction {south}.")
        if west not in list(range(2)):
            raise ValueError(f"Invalid west direction {west}.")
        if closest_food_dir not in list(range(4)):
            raise ValueError(f"Invalid closest pellet direction {closest_food_dir}.")
        if closest_ghost_dir not in list(range(4)):
            raise ValueError(f"Invalid closest ghost direction {closest_ghost_dir}.")

        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.closest_food_dir = closest_food_dir
        self.closest_ghost_dir = closest_ghost_dir

    def as_tuple(self):
        """
        Function returns a tuple representation of the state.
        :return: A tuple representation of the state.
        """
        return (self.north, self.east, self.south, self.west, self.closest_food_dir, self.closest_ghost_dir)

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

class QTable:

    def __init__(self): # TODO: take actions from Directions class as list as an argument
        self.table = {}
        self.actions = ['North', 'East', 'South', 'West'] # TODO: change to a list of actions from Directions class!
        self.init_table()
        self.save()

    def init_table(self):
        """
        Generates all possible states.
        :return: None.
        """
        for n in range(2): # can go north: 1, cant go north: 0
            for e in range(2): # can go south: 1, cant go south: 0
                for s in range(2): # can go east: 1, cant go east: 0
                    for w in range(2): # can go west: 1, cant go west: 0
                        for p_dir in range(4): # player direction: 0 = north, 1 = east, 2 = south, 3 = west
                            for g_dir in range(4): # ghost direction: 0 = north, 1 = east, 2 = south, 3 = west
                                state = State(n, e, s, w, p_dir, g_dir)
                                self.table[hash(state)] = [0]*len(self.get_actions()) # create an entry in the Q-table for the state

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
        print(state, hash(state))
        return self.table[hash(state)]

    def update_state(self, state: State, action, value):
        """
        Updates the state action pair to the given value.
        """
        print(state, action, value)
        idx = self.get_actions().index(action)
        self.table[hash(state)][idx] = value

    def save(self, filename='q_table'):
        """
        Saves the Q-Table to a file.
        :param filename: name of the file
        """
        
        dir = "src/back_end/training/" + filename + ".json"
        with open(dir, 'w') as f:
            json.dump(self.table, f, indent=4)

    def load(self, filename='q_table'):
        """
        Loads the Q-Table from a file.
        :param filename: name of the file
        """
        dir = "src/back_end/training/" + filename + ".json" 
        with open(dir, 'r') as f:
            raw_table = json.load(f)
            tmp = {}
            for key in raw_table:
                tmp[int(key)] = raw_table[key] # make sure key is an integer
            self.table = tmp

    def __str__(self):
        string = ""
        for key in self.table.keys():
            string += str(key) + " : " + str(self.table[key]) + "\n"
        return string
        
if __name__ == "__main__":
    q = QTable()
    print(q)