from front_end.game_files.constants import *
from front_end.game_files.agent_logic.agent_directions import Directions
from front_end.game_files.agent_logic.agent_actions import Actions
from front_end.util import nearestPoint, manhattanDistance


class GhostRules:
    """
    These functions dictate how ghosts interact with their environment.
    """
    GHOST_SPEED=1.0
    def getLegalActions( state, ghostIndex ):
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """
        conf = state.getGhostState( ghostIndex ).configuration
        possibleActions = Actions.getPossibleActions( conf, state.data.layout.walls )
        reverse = Actions.reverseDirection( conf.direction )
        if Directions.STOP in possibleActions:
            possibleActions.remove( Directions.STOP )
        if reverse in possibleActions and len( possibleActions ) > 1:
            possibleActions.remove( reverse )
        return possibleActions
    getLegalActions = staticmethod( getLegalActions )

    def applyAction( state, action, ghostIndex):

        legal = GhostRules.getLegalActions( state, ghostIndex )
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0: speed /= 2.0
        vector = Actions.directionToVector( action, speed )
        ghostState.configuration = ghostState.configuration.generateSuccessor( vector )
    applyAction = staticmethod( applyAction )

    def decrementTimer( ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint( ghostState.configuration.pos )
        ghostState.scaredTimer = max( 0, timer - 1 )
    decrementTimer = staticmethod( decrementTimer )

    def checkDeath( state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0: # Pacman just moved; Anyone can kill him
            for index in range( 1, len( state.data.agentStates ) ):
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()
                if GhostRules.canKill( pacmanPosition, ghostPosition ):
                    GhostRules.collide( state, ghostState, index )
        else:
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            if GhostRules.canKill( pacmanPosition, ghostPosition ):
                GhostRules.collide( state, ghostState, agentIndex )
    checkDeath = staticmethod( checkDeath )

    def collide( state, ghostState, agentIndex):
        if ghostState.scaredTimer > 0:
            state.data.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            # Added for first-person
            state.data._eaten[agentIndex] = True
        else:
            if not state.data._win: # this means you lost the game
                state.data.scoreChange -= 500
                state.data._lose = True
    collide = staticmethod( collide )

    def canKill( pacmanPosition, ghostPosition ):
        return manhattanDistance( ghostPosition, pacmanPosition ) <= COLLISION_TOLERANCE
    canKill = staticmethod( canKill )

    def placeGhost(state, ghostState):
        ghostState.configuration = ghostState.start
    placeGhost = staticmethod( placeGhost )