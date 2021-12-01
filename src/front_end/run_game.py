import copy
import os

from back_end.reinforcement_learning.qtable import QTable
from back_end.reinforcement_learning.epsilon_greedy import epsilonGreedy

class RunGame:
    """
    RunGame class.
    """

    def __init__(self, game):
        """
        Default constructor.
        """
        self.game = game
        self.games = []
        self.data = [[],[],[], [], [], []]
        self.run()

    def run(self):
        """
        Purpose:
            Runs the specified reinforcement learning algorithm.
            SARSA or QLearning.
        Args:
            self - class instance.
        """
        if self.game.method == 'SARSA':
            self.run_sarsa(episodes=self.game.episodes)
        elif self.game.method == 'QLearning':
            self.run_qlearning(episodes=self.game.episodes)
        else:
            print("Invalid method {self.game.method}! Method must be 'SARSA' or 'QLearning'.")
            exit(1)

    def collect_data(self, method, episode, total_timesteps, episode_timesteps, total_reward, episode_reward):
        """
        Purpose:
            Collects data for graphing.
        Args:
            episode - the episode number.
            total_timesteps - the total timesteps taken since episode 0
            episode_timesteps - the timesteps taken in this episode.
            total_reward - the total reward since episode 0.
            episode_reward - the total reward in this episode.
        Returns:
            None
        """
        if self.data[0] == []:
            self.data[0].append(method)
        self.data[1].append(episode)
        self.data[2].append(total_timesteps)
        self.data[3].append(episode_timesteps)
        self.data[4].append(total_reward)
        self.data[5].append(episode_reward)
                

    def run_sarsa(self, episodes, alpha=0.5, gamma=0.9, epsilon=0.01, filename='SARSA_QTable'):
        """
        Purpose:
            SARSA Algorithm for controlling Pacman.
        Args:
            self - class instance.
            episodes - the number of episodes to run.
            alpha - the alpha value to use.
            gamma - the gamma value to use.
            epsilon - the epsilon value to use.
            filename - the name of the qtable to load/create.
        Returns:
            None
        """
        if self.game.multithreaded:
            filename = str(os.getpid()) + '_' + filename

        print("Running SARSA.")

        q_table = QTable()
        # List of starting game states. Used to get information about each game once completed.
        start_game = [copy.deepcopy(self.game) for _ in range(episodes)]
        total_timesteps = 0
        total_reward = 0
        for episode in range(episodes):
            episode_timesteps = 0
            episode_reward = 0

            q_table.load(filename)                                                          # Load QTable
            self.game = start_game[episode]                                                 # Get starting game object state

            if not self.game.verbose: self.game.display.initialize(self.game.state.data)    # Initialize the GUI
            
            pacman_agent = self.game.agents[0]                  # Get Pacman Agent object
            ghost_agents = self.game.agents[1:]                 # Get Ghost Agent Objects
            self.game.numMoves = 0                              # Initialize move counter.

            # Gets the state object to query qtable.
            state = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)
            # Get all actions Pacman can take.
            legal_actions = self.game.state.getLegalPacmanActions()
            # Get an action given the current state based on epsilon greedy policy.
            action = epsilonGreedy(q_table, state, legal_actions, epsilon)

            # Loop until the terminal state is reached
            while not self.game.gameOver:
                # Take action, observe R, S'
                self.game.moveHistory.append( (0, action) )
                self.game.state = self.game.state.generateSuccessor( 0, action )
                state_prime = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)
                reward = pacman_agent.get_reward(self.game.state.data)
                
                # Choose action' from S'
                legal_actions = self.game.state.getLegalPacmanActions()
                action_prime = epsilonGreedy(q_table, state_prime, legal_actions, epsilon)

                # Get new state action pair value.
                new_q_s_a = q_table.get_action_value(state, action) + alpha * (reward + gamma * q_table.get_action_value(state_prime, action_prime) - q_table.get_action_value(state, action))
                
                # Update qtable.
                q_table.update_state(state, action, new_q_s_a)
                
                # Change the display
                self.game.state.data.agentMoved = 0
                if not self.game.verbose: self.game.display.update( self.game.state.data )
                
                # Allow for game specific conditions (winning, losing, etc.)
                self.game.rules.process(self.game.state, self.game)
                self.game.numMoves += 1

                # Check if in win/lose state before moving the ghost.
                if self.game.gameOver: continue
                
                # Moves the ghost.
                self.run_ghost(ghost_agents)
                
                # S <- S'
                # A <- A'
                state = state_prime
                action = action_prime

                episode_timesteps += 1
                total_timesteps += 1
                total_reward += 1
                episode_reward += 1

            self.games.append(self.game)
            q_table.save(filename)
            # Update data with results. Used to make graphs.
            self.collect_data(self.game.method, episode, total_timesteps, episode_timesteps, total_reward, episode_reward)

        # close the display when the game terminates.
        if not self.game.verbose: self.game.display.finish()

    def run_qlearning(self, episodes, alpha=0.5, gamma=0.9, epsilon=0.05, filename='Qlearning_QTable'):
        """
        Purpose:
            SARSA Algorithm for controlling Pacman.
        Args:
            self - class instance.
            episodes - the number of episodes to run.
            alpha - the alpha value to use.
            gamma - the gamma value to use.
            epsilon - the epsilon value to use.
            filename - the name of the qtable to load/create.
        Returns:
            None
        """
        if self.game.multithreaded:
            filename = str(os.getpid()) + '_' + filename
        
        print("Running QLearning")
        q_table = QTable()
        # List of starting game states. Used to get information about each game once completed.
        start_game = [copy.deepcopy(self.game) for _ in range(episodes)]
        total_timesteps = 0
        total_reward = 0
        for episode in range(episodes):
            episode_timesteps = 0
            episode_reward = 0
            q_table.load(filename)                                                          # Load QTable
            self.game = start_game[episode]                                                 # Get starting game object state
            if not self.game.verbose: self.game.display.initialize(self.game.state.data)    # Initialize the GUI
            
            pacman_agent = self.game.agents[0]                  # Get Pacman Agent object
            ghost_agents = self.game.agents[1:]                 # Get Ghost Agent Objects
            self.game.numMoves = 0                              # Initialize move counter.

            # Gets the state object to query qtable.
            state = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)

            while not self.game.gameOver:
                # Get an action given the current state based on epsilon greedy policy.
                legal_actions = self.game.state.getLegalPacmanActions()
                action = epsilonGreedy(q_table, state, legal_actions, epsilon)
                # Take action, observe R, S'
                self.game.moveHistory.append( (0, action) )
                self.game.state = self.game.state.generateSuccessor( 0, action )
                state_prime = pacman_agent.get_state_representation(copy.deepcopy(self.game), 6)
                reward = pacman_agent.get_reward(self.game.state.data)
                
                # Get new state action pair value.
                new_q_s_a = q_table.get_action_value(state, action) + alpha * (reward + gamma * max(q_table.get_state_values(state_prime)) - q_table.get_action_value(state, action))
                
                # Update qtable.
                q_table.update_state(state, action, new_q_s_a)
                
                # Change the display
                self.game.state.data.agentMoved = 0
                if not self.game.verbose: self.game.display.update( self.game.state.data )
                
                # Allow for game specific conditions (winning, losing, etc.)
                self.game.rules.process(self.game.state, self.game)
                self.game.numMoves += 1

                # Check if in win/lose state before moving the ghost.
                if self.game.gameOver: continue

                # Move the ghost.
                self.run_ghost(ghost_agents)
                
                # S <- S'
                state = state_prime

                episode_timesteps += 1
                total_timesteps += 1
                total_reward += 1
                episode_reward += 1
            
            self.games.append(self.game)
            q_table.save(filename)
            # Update data with results. Used to make graphs.
            self.collect_data(self.game.method, episode, total_timesteps, episode_timesteps, total_reward, episode_reward)

        # close the display when the game terminates.
        if not self.game.verbose: self.game.display.finish()

    def run_ghost(self, ghost_agents):
        """
        Purpose:
            Updates the ghosts position.
        Args:
            self - class instance.
            ghost_agents - list of ghost agent objects.
        Returns:
            None
        """
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
            if not self.game.verbose: self.game.display.update( self.game.state.data )
            
            # Allow for game specific conditions (winning, losing, etc.)
            self.game.rules.process(self.game.state, self.game)

            self.game.numMoves += 1
            agent_index += 1
        return
