# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import front_end.layout as Layout
from front_end.graphics import graphicsDisplay
from front_end.game_files.classic_rules import ClassicGameRules
from front_end.agents.ghost_agents import RandomGhost, DirectionalGhost

#############################
# FRAMEWORK TO START A GAME #
#############################


def loadGhost(ghostType):
    """
    Returns a ghost agent class of the requested type.
    """
    if ghostType == 'RandomGhost':
        return RandomGhost
    elif ghostType == 'DirectionalGhost':
        return DirectionalGhost

def loadPacman():
    """
    Returns a pacman agent object
    """
    from front_end.agents.pacman_agents import PacmanAgent
    return PacmanAgent()

def runGames(layout, pacman, ghosts, display, method, timeout=30):

    rules = ClassicGameRules(timeout) 
    game = rules.newGame(layout, pacman, ghosts, display, method)
    games = game.run()
    
    scores = [game.state.getScore() for game in games]
    wins = [game.state.isWin() for game in games]

    if float(len(wins)) == 0.0:
        winRate = wins.count(True)
    else:
        winRate = wins.count(True)/ float(len(wins))
    if float(len(scores)) == 0.0:
        avgScore = sum(scores)
    else:
        avgScore = sum(scores) / float(len(scores))
    print('Average Score:', avgScore)
    print('Scores:       ', ', '.join([str(score) for score in scores]))
    print('Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate))
    print('Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins]))

    return games

def main(layout=None, num_ghosts=1, frame_time=0.1, agent='PacmanAgent', method='QLearning'):

    if layout == None:
        raise Exception('No layout specified!')

    layout = Layout.getLayout(layout)
    ghosts = [loadGhost('DirectionalGhost')( i+1 ) for i in range(num_ghosts)]
    pacman = loadPacman()
    display = graphicsDisplay.PacmanGraphics(frameTime = frame_time)

    runGames(layout, pacman, ghosts, display, method)