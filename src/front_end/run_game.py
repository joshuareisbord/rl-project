import copy
from back_end.reinforcement_learning.qtable import QTable, State
from back_end.reinforcement_learning.rand_argmax import rand_argmax
from back_end.reinforcement_learning.epsilon_greedy import epsilonGreedy
NORTH = 'North'
SOUTH = 'South'
EAST = 'East'
WEST = 'West'
STOP = 'Stop'

class RunGame:
    def __init__(self, game):
        self.game = game
        self.run()

    def run(self, episodes=2, alpha=0.5, gamma=0.9, epsilon=0.1, filename='q_table'):
        """
        Main control loop for game play.
        """
        # clean_game = copy.deepcopy(self.game)

        # for _ in range(episodes):
        #     self.game = copy.deepcopy(clean_game)
        #     self.game.display.initialize(self.game.state.data)
        #     self.game.numMoves = 0

        #     agentIndex = self.game.startingIndex
        #     numAgents = len( self.game.agents )
        
        #     while not self.game.gameOver:
        #         # Fetch the next agent
        #         agent = self.game.agents[agentIndex]
        #         move_time = 0
        #         skip_action = False
        #         observation = self.game.state.deepCopy()

        #         # Solicit an action
        #         action = None
        #         # self.game.mute(agentIndex)
        #         action = agent.getAction(observation)
        #         # self.game.unmute()

        #         # Execute the action
        #         self.game.moveHistory.append( (agentIndex, action) )
        #         self.game.state = self.game.state.generateSuccessor( agentIndex, action )

        #         # Change the display
        #         self.game.display.update( self.game.state.data )
        #         ###idx = agentIndex - agentIndex % 2 + 1
        #         ###self.game.display.update( self.game.state.makeObservation(idx).data )

        #         # Allow for game specific conditions (winning, losing, etc.)
        #         self.game.rules.process(self.game.state, self.game)
        #         # Track progress
        #         if agentIndex == numAgents + 1: self.game.numMoves += 1
        #         # Next agent
        #         agentIndex = ( agentIndex + 1 ) % numAgents
    
        
        
        
        
        start_game = copy.deepcopy(self.game)
        for episode in range(episodes):
            self.game = copy.deepcopy(start_game)
            pacman_agent = self.game.agents[0]
            ghost_agents = self.game.agents[1:]
            q_table = QTable()
            q_table.load(filename)
            self.game.display.initialize(self.game.state.data)
            self.game.numMoves = 0
            
            state = pacman_agent.get_state_representation(self.game.state.deepCopy())

            legal_actions = self.game.state.getLegalPacmanActions()
            # Hash state
            action = epsilonGreedy(q_table, state, legal_actions, epsilon)
            # choose action, from S using qtable

            try:
                while not self.game.gameOver:

                    # Take action, observe R, S'
                    self.game.moveHistory.append( (0, action) )
                    self.game.state = self.game.state.generateSuccessor( 0, action )
                    reward = pacman_agent.get_reward(self.game.state.data)
                    state_prime = pacman_agent.get_state_representation(self.game.state.deepCopy())
                    # choose action' from S'
                    legal_actions = self.game.state.getLegalPacmanActions()
                    action_prime = epsilonGreedy(q_table, state_prime, legal_actions, epsilon)
                    
                    new_q_s_a = q_table.get_action_value(state, action) + alpha * (reward + gamma * q_table.get_action_value(state_prime, action_prime) - q_table.get_action_value(state, action))
                    
                    # update qtable
                    q_table.update_state(state, action, new_q_s_a)
                    
                    
                    # Change the display
                    self.game.display.update( self.game.state.data )
                    
                    # Allow for game specific conditions (winning, losing, etc.)
                    self.game.rules.process(self.game.state, self.game)
                    self.game.numMoves += 1

                    self.run_ghost(ghost_agents)
                    
                    state = state_prime
                    action = action_prime

                q_table.save(filename)   
            except Exception as e:
                print(e)
                continue 
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