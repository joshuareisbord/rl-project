

from environment import Environment
from graph import Graph
from simulator import Simulator

def run(length, width, board, actions, bounds):
    graph = Graph(length, width, board, actions, bounds)
    environment = Environment(graph)


if __name__ == '__main__':
    length = 5
    width = 4
    board = [ 1, 1, 1, 1,
              1, 0, 0, 1,
              1, 0, 1, 1,
              1, 0, 0, 1,
              1, 1, 1, 1 ]
    
    actions = [-4, 1, 4, -1] # [ north, east, south, west] (index modifiers for the board)
    bounds = [0, [4, 8, 12, 16, 20], 20, [-1, 3, 7, 11, 15]] # [ north, [east], south, [west] ]


