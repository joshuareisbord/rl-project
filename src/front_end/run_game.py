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

    def run(self, episodes=100, alpha=0.5, gamma=9, epsilon=0.1, filename='q_table'):
        """
        Main control loop for game play.
        """
        q_table = QTable()
        start_game = copy.deepcopy(self.game)
        for episode in range(episodes):
            self.game = copy.deepcopy(start_game)
            self.game.display.initialize(self.game.state.data)
            pacman_agent = self.game.agents[0]
            ghost_agents = self.game.agents[1:]
            
            q_table.load(filename)
            
            self.game.numMoves = 0

            state = pacman_agent.get_state_representation(self.game.state.deepCopy())
            
            legal_actions = self.game.state.getLegalPacmanActions()
            # Hash state
            action = epsilonGreedy(q_table, state, legal_actions, epsilon)
            # choose action, from S using qtable

            
            while not self.game.gameOver:
                if self.game.gameOver:
                    continue
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

                if self.game.gameOver:
                    continue

                self.run_ghost(ghost_agents)
                
                state = state_prime
                action = action_prime

            q_table.save(filename)   
            
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