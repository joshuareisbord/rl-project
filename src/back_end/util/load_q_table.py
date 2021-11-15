from back_end.reinforcement_learning.qtable import QTable

def load_q_table(file_name = None):
    """
    Loads an Q-Table from a file within src/back_end/training.

    :param file_name: The name of the file to load.
    :return: The Q-Table object.
    """

    if file_name is None:
        return QTable()
    return QTable(file_name)
