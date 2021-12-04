import os
from multiprocessing import Process

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Verbose = False will display the GUI. Frame_time lets you control how fast the display is updated.
# Note some small states will cause the game to studder as it is taking longer to calculate A* for that state.
# Verbose = True will just have std output of each game.

def error(message):
    print("\n")
    print("Error: " + message)
    print("\n")

if __name__ == "__main__":

                   # [layout, episodes, ghosts, frame_time, method, verbose, multithreaded]
    # default_params = ['smallClassicTest2', 10, 1, 0.001, 'QLearning', True, False]
    default_params = ['smallClassicTest2', 5, 1, 0.1, 'FollowQ', False, False]

    core_count = 1 # default core ocunt

    print("\nParamaters Set:")
    print(f"Layout: {default_params[0]}")
    print(f"Episodes: {default_params[1]}")
    print(f"Ghosts: {default_params[2]}")
    print(f"Frame Time: {default_params[3]}")
    print(f"Method: {default_params[4]}")
    print(f"No GUI: {default_params[5]}")
    print(f"Multi-Threaded: {default_params[6]}")
    print("\n")

    selection = input("Change any paramaters? (y/n): ")

    if selection == "y": # if user wants to change any parameters
        
        while(True):
            print("\n")
            print("1. Layout")
            print("2. Episodes")
            print("3. Ghosts")
            print("4. Frame Time")
            print("5. TD Method")
            print("6. Use GUI")
            print("7. Finish (any other key)")
            print("\n")
            to_change = input("Selection: ")

            # layout (this is the board we are using)
            if to_change == "1":
                default_params[0] = input("Enter layout: ")
            
            # number of episodes to train on
            elif to_change == "2":
                choice = int(input("Enter episodes: "))
                try:
                    default_params[1] = int(choice)
                except:
                    error("Invalid input! Must be an integer!")
            
            # numbrt of ghosts
            elif to_change == "3":
                choice = int(input("Enter ghosts: "))
                try:
                    default_params[2] = int(choice)
                except:
                    error("Invalid input! Must be an integer!")
            
            # change frame time (how fast game runs)
            elif to_change == "4":
                choice = float(input("Enter frame time: "))
                try:
                    choice = float(choice)
                    if choice > 0.0009 and choice < 1:
                        default_params[3] = choice
                except:
                    error("Invalid input! Must be a float between 0.001 and 1!")
            
            # change td method
            elif to_change == "5":
                choice = input("Enter TD method (SARSA, QLearning, or FollowQ (just follow QTable)): ")
                if choice == "SARSA" or choice == "sarsa":
                    default_params[4] = "SARSA"
                elif choice == "QLearning" or choice == "qlearning":
                    default_params[4] = "QLearning"
                elif choice == "FollowQ" or choice == "followq":
                    default_params[4] = "FollowQ"
                else:
                    error("Invalid input! Must be 'SARSA', 'QLearning', or FollowQ!")
            
            # verbose mode
            elif to_change == "6":
                choice = input("Use GUI? (y/n): ")
                if choice == "y":
                    default_params[5] = False
                elif choice == "n":
                    default_params[5] = True
                else:
                    error("Invalid input. Must be 'y' or 'n'!")
            
            # exit
            else:
                break

    selection = input("Run multiple instances? (y/n): ")
    if selection == "y":
            choice = int(input("Enter number of instances: (-1 for max): "))
            try:
                choice = int(choice)
                if choice > os.cpu_count():
                    print("Warning: You have entered a number greater than the number of cores on your machine! Are you sure you want to continue?")
                    print("If you choose not to continue cores will be set to max avaliable on machine! (y/n) ", end="")
                    confirm = input("")
                    if confirm == "y":
                        core_count = choice
                    else:
                        choice = os.cpu_count()
                elif choice == -1:
                    core_count = os.cpu_count()
                elif choice == 0:
                    error("Invalid input! Must be greater than 0!")
                else:
                    core_count = choice
            except:
                error("Invalid input! Must be an integer between 0 and the cores on your machine! (-1 for max)")

    elif selection == "n":
        default_params[6] = False
    else:
        print("Invalid input. Must be 'y' or 'n'!")
    
    default_params[6] = core_count > 1 or core_count== -1 # set to true if we are running multiple instances

    arg_string = f"--layout={default_params[0]} \
                   --episodes={default_params[1]} \
                   --ghosts={default_params[2]} \
                   --frametime={default_params[3]} \
                   --method={default_params[4]} \
                   --verbose={default_params[5]} \
                   --multithreaded={default_params[6]}"

    for i in range(core_count):
            p = Process(target=os.system, args=(f"python threaded_executer.py {arg_string}",))
            p.start()

    # pacman.main(layout='smallClassicTest2', episodes=2, frame_time=0.001, method='QLearning', verbose=True)


