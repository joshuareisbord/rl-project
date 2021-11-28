import numpy as np
from simulator import Environment
from simulator import Graph
from state import State


def get_current_state(environment):

    """ 
    Purpose:
        Function takes in an environemnt and translates it into
        the appropriate state vector reperesntation
    Args:
        envionrment - The environment object which holds game data
    Returns: 
        The direction
    """
    #available_positions = []
    pac_man = environment.pacman
    position = environment.nodes[pac_man]
    n = (int(position.north is not None))
    e = (int(position.east is not None))
    s = (int(position.south is not None))
    w = (int(position.west is not None))

    pellet_dir = get_closest_pellet_direction(environment)
    ghost_dir = get_ghost_direction(environment)

    return State(n, e, s, w, pellet_dir, ghost_dir)

def get_closest_pellet_direction(environment):
    """
    Purpose:
        Function gets the closest pellet to pac_man and 
        calculates its relative direction to pac_man
    Args:
        pac_man_position - the index of pac_man's position in the graph 
    Returns: 
        The direction of the pellet (0-3)
    """

    closest = [None, None, np.inf]
    for end in range(len(environment.length)):
        node = environment.nodes[end]
        if node is not None:
            #a_star
            path = environment.a_star.a_star(environment.pac_man, end)
            if (len(path < closest[1])):
                direction = environment.a_star.get_direction_of_a_star(path)
                closest = [node, direction, len(path)]
    return direction

def get_ghost_direction(environment):
    ghost_path = environment.a_star.a_star(environment.pac_man, environment.ghost)
    ghost_dir = environment.a_star.get_direction_of_a_star(ghost_path)

    return ghost_dir

def get_reward(position, action):
    """
    Purpose:
        Function gets the reward after taking an action.
    Args:
        position - the index 
    Action is an index
    """
    node = self.nodes[position]
    valid_action = self.verify_position(position, action)
    if valid_action:
        next_position = position + self.actions[action]
        next_node = self.nodes[next_position]
        if next_node.ghost:
            return -10
        else:
            if next_node.pellet:
                return 1
            else:
                return -0.5
    return -0.5



