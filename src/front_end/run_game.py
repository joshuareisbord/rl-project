
class RunGame:
    def __init__(self, game):
        self.game = game
        self.run()

    def run(self):
        """
        Main control loop for game play.
        """
        
        pacman_agent = self.game.agents[0]
        ghost_agents = self.game.agents[1:]
        
        # Get Q table

        self.game.display.initialize(self.game.state.data)
        self.game.numMoves = 0
        pacman_agent.get_state_representation(self.game.state.deepCopy())
        # choose action, from S using qtable
        while not self.game.gameOver:
            # Take action, observe R, S'

            # choose action' from S'
            # update qtable
            # s = s' a = a'
            # Fetch the next agent
            
            
            observation = self.game.state.deepCopy()

            # get an action
            action = pacman_agent.getAction(observation)

            # Take the action
            self.game.moveHistory.append( (0, action) )
            self.game.state = self.game.state.generateSuccessor( 0, action )

            # Change the display
            self.game.display.update( self.game.state.data )
            
            # Allow for game specific conditions (winning, losing, etc.)
            self.game.rules.process(self.game.state, self.game)
            self.game.numMoves += 1

            self.run_ghost(ghost_agents)
            
        self.game.display.finish()

    def run_ghost(self, ghost_agents):
        agent_index = 1
        for agent in ghost_agents:
            observation = self.game.state.deepCopy()

            # Get an action
            action = agent.getAction(observation)

            # Execute the action
            self.game.moveHistory.append( (agent_index, action) )
            self.game.state = self.game.state.generateSuccessor( agent_index, action )

            # Change the display
            self.game.display.update( self.game.state.data )
            
            # Allow for game specific conditions (winning, losing, etc.)
            self.game.rules.process(self.game.state, self.game)

            self.game.numMoves += 1
            agent_index += 1