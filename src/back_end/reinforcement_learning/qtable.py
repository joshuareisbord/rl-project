
import json
import os
from state import States

class QTable:
    """
    This is the Q-Table for the PacMan game.
    """
    def __init__(self, filename="q_table.json"):
        """
        Initializes the Q-Table.

        :param filename: The filename of the Q-Table.
        """
        self.__table = {}
        self.__load_q_table()
        self.__filename = filename

    def __load_q_table(self):
        """
        Loads the Q-Table from file. If the file does not exist, Q-Table is created.

        :param filename: The filename of the Q-Table.
        """
        try:
            file_dir = f"{os.getcwd()}/{'PacMan/training/'}{self.__filename}"
            with open(file_dir, "r") as file:
                self.__table = json.load(file)
        except FileNotFoundError:
            print(f"Q-Table file at {file_dir} not found! Generating new Q-Table")
            states = States()
            for state in states.keys():
                self.__table[state] = [0, 0, 0, 0] # [ north, east, south, west ] #q-values which will be updated

    def get_state_q_values(self, state):
        """
        Returns the Q-Values of a state.

        :param state: The state.

        :return: The Q-Values of the state.
        """
        try:
            return self.__table[hash(state)]
        except KeyError:
            raise KeyError("The state does not exist in the Q-Table!")

    def get_q_value(self, state, action):
        """
        Gets the Q-Value of a state and action.

        :param state: The state.
        :param action: The action: north, south, east or west.

        :return: The Q-Value of the state and action.
        """

        actions = self.get_state_q_values(state)

        if action.lower() in ["north", "east", "south", "west"]:
            if action == "north":
                return actions[0]
            elif action == "east":
                return actions[1]
            elif action == "south":
                return actions[2]
            elif action == "west":
                return actions[3]
        else:
            raise ValueError("The action is not valid!")

    def set_q_value(self, state, action, value):
        """
        Sets the Q-Value of a state and action.

        :param state: The state.
        :param action: The action.

        :return: True if the Q-Value was set, False otherwise.
        """
        try:
            self.__table[hash(state)][action] = value
            return True
        except KeyError:
            raise KeyError("The state does not exist in the Q-Table!")

    def save(self):
        """
        Save the Q-Table to a file.

        :param filename: The filename of the Q-Table.

        :return: True if the Q-Table was saved

        :raises FileNotFoundError: If the file does not exist.
        """
        try:
            file_dir = f"{os.getcwd()}/{'PacMan/training/'}{self.__filename}"
            print(f"Saving Q-Table to {file_dir}")
            with open(file_dir, "w") as file:
                json.dump(self.__table, file, indent=4)
        except FileNotFoundError:
            exception = FileNotFoundError("The file could not be found.")
            raise exception

    def __str__(self):
        """
        String representation of the Q-Table.

        :return: A string representation of the Q-Table.
        """
        string = ""
        for state in self.__table.keys():
            string += f"{str(state)}: {str(self.__table[state])}\n"
        return string

    def __len__(self):
        """
        Total number of states in the Q-Table.

        :return: The total number of states in the Q-Table.
        """
        return len(self.__table)