
import os
import sys
from front_end import pacman
from optparse import OptionParser

def start_game(args):
    """
    Calls pacman.py with the given arguments.

    Args:
        args: A dictionary containing the arguments.
    
    Returns:
        Nothing
    """

    pacman.main(layout=args['layout'],
                num_ghosts=args['ghosts'], 
                frame_time=args['frametime'],
                episodes=args['episodes'],  
                method=args['method'], 
                verbose=args['verbose'], 
                multithreaded=args['multithreaded'])

def do_parse(argv):
    """
    Parse the command line input.

    Args:
        argv: The command line arguments.

    Returns:
        A dictionary containing the parsed arguments.
    """

    parser = OptionParser()

    parser.add_option('-l', '--layout', type='string', dest='layout')
    parser.add_option('-e', '--episodes', type='int', dest='episodes')
    parser.add_option('-g', '--ghosts', type='int', dest='ghosts')
    parser.add_option('-f', '--frametime', type='float', dest='frametime')
    parser.add_option('-m', '--method', type='string', dest='method')
    parser.add_option('-v', '--verbose', type='string', dest='verbose')
    parser.add_option('-t', '--multithreaded', type='string', dest='multithreaded')    
    
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    if options.verbose == 'False': # do we run the game without gui?
        verbose = False
    else:
        verbose = True
    if options.multithreaded == 'False': # are we running multithreaded?
        multithreaded = False
    else:
        multithreaded = True

    args['layout'] = options.layout
    args['episodes'] = options.episodes
    args['ghosts'] = options.ghosts
    args['frametime'] = options.frametime
    args['method'] = options.method
    args['verbose'] = verbose
    args['multithreaded'] = multithreaded

    return args

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    args = do_parse(sys.argv[1:]) # capture the command line inputs
    start_game(args) # start a game using the command line inputs
