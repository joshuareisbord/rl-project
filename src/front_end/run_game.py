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
        self.games = []
        self.run()

    def run(self):
        if self.game.method == 'SARSA':
            self.run_sarsa()
        if self.game.method == 'QLearning':
            self.run_qlearning()

    def run_sarsa(self, episodes=300, alpha=0.5, gamma=0.9, epsilon=0.01, filename='q_t'):
        """
        Main control loop for game play.
        """
        q_table = QTable()
        print("Running SARSA")
        start_game = [copy.deepcopy(self.game) for _ in range(episodes)]
        
        for episode in range(episodes):
            self.game = copy.deepcopy(start_game[episode])
            self.game.display.initialize(self.game.state.data)
            pacman_agent = self.game.agents[0]
            ghost_agents = self.game.agents[1:]
            
            q_table.load(filename)
            
            self.game.numMoves = 0

            state = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)
            
            legal_actions = self.game.state.getLegalPacmanActions()
            # Hash state
            action = epsilonGreedy(q_table, state, legal_actions, epsilon)

            # Get an action
            # choose action, from S using qtable

            while not self.game.gameOver:
                if self.game.gameOver:
                    continue
                # Take action, observe R, S'
                self.game.moveHistory.append( (0, action) )
                self.game.state = self.game.state.generateSuccessor( 0, action )
                state_prime = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)
                reward = pacman_agent.get_reward(self.game.state.data)
                
                # choose action' from S'
                legal_actions = self.game.state.getLegalPacmanActions()
                action_prime = epsilonGreedy(q_table, state_prime, legal_actions, epsilon)

                # Get an action
                new_q_s_a = q_table.get_action_value(state, action) + alpha * (reward + gamma * q_table.get_action_value(state_prime, action_prime) - q_table.get_action_value(state, action))
                
                # update qtable
                q_table.update_state(state, action, new_q_s_a)
                
                
                # Change the display
                self.game.state.data.agentMoved = 0
                self.game.display.update( self.game.state.data )
                
                # Allow for game specific conditions (winning, losing, etc.)
                self.game.rules.process(self.game.state, self.game)
                self.game.numMoves += 1

                if self.game.gameOver:
                    continue

                self.run_ghost(ghost_agents)
                
                state = state_prime
                action = action_prime

            self.games.append(self.game)
            q_table.save(filename)   
            
        self.game.display.finish()

    def run_qlearning(self, episodes=50, alpha=0.5, gamma=0.9, epsilon=0.05, filename='q_t'):
        """
        Main control loop for game play.
        """
        print("Running QLearning")
        q_table = QTable()
        start_game = [copy.deepcopy(self.game) for _ in range(episodes)]
        for episode in range(episodes):
            self.game = copy.deepcopy(start_game[episode])
            self.game.display.initialize(self.game.state.data)
            pacman_agent = self.game.agents[0]
            ghost_agents = self.game.agents[1:]
            
            q_table.load(filename)
            
            self.game.numMoves = 0

            state = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)

            while not self.game.gameOver:
                if self.game.gameOver:
                    continue
                legal_actions = self.game.state.getLegalPacmanActions()
                # Hash state
                action = epsilonGreedy(q_table, state, legal_actions, epsilon)
                # Take action, observe R, S'
                self.game.moveHistory.append( (0, action) )
                self.game.state = self.game.state.generateSuccessor( 0, action )
                state_prime = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)
                reward = pacman_agent.get_reward(self.game.state.data)
                
                # Get an action
                new_q_s_a = q_table.get_action_value(state, action) + alpha * (reward + gamma * max(q_table.get_state_values(state_prime)) - q_table.get_action_value(state, action))
                
                # update qtable
                q_table.update_state(state, action, new_q_s_a)
                
                
                # Change the display
                self.game.state.data.agentMoved = 0
                self.game.display.update( self.game.state.data )
                
                # Allow for game specific conditions (winning, losing, etc.)
                self.game.rules.process(self.game.state, self.game)
                self.game.numMoves += 1

                if self.game.gameOver:
                    continue

                self.run_ghost(ghost_agents)
                
                state = state_prime
                
            self.games.append(self.game)
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
            self.game.state.data.agentMoved = 1
            self.game.display.update( self.game.state.data )
            
            # Allow for game specific conditions (winning, losing, etc.)
            self.game.rules.process(self.game.state, self.game)

            self.game.numMoves += 1
            agent_index += 1