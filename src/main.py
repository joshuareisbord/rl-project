import multiprocessing
import traceback
import os
from front_end import pacman
from multiprocessing import Process
import multiprocessing as mp

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Verbose = False will display the GUI. Frame_time lets you control how fast the display is updated.
# Note some small states will cause the game to studder as it is taking longer to calculate A* for that state.
# Verbose = True will just have std output of each game.

if __name__ == "__main__":

                   # [layout, episodes, frame_time, method, verbose]
    default_params = ['smallClassicTest2', 2, 1, 0.001, 'QLearning', False, False]
    core_count = 1

    selection = input("Change any paramaters? (y/n): ")

    if selection == "y":
        
        while(True):
            print("1. Layout")
            print("2. Episodes")
            print("3. Ghosts")
            print("4. Frame Time")
            print("5. TD Method")
            print("6. Use GUI")
            print("7. Finish (any other key)")
            to_change = input("Selection:")

            if to_change == "1":
                default_params[0] = input("Enter layout: ")
            elif to_change == "2":
                choice = int(input("Enter episodes: "))
                try:
                    default_params[1] = int(choice)
                except:
                    print("Invalid input! Must be an integer!")
            elif to_change == "3":
                choice = int(input("Enter ghosts: "))
                try:
                    default_params[2] = int(choice)
                except:
                    print("Invalid input! Must be an integer!")
            elif to_change == "4":
                choice = float(input("Enter frame time: "))
                try:
                    choice = float(choice)
                    if choice > 0.0009 and choice < 1:
                        default_params[2] = choice
                except:
                    print("Invalid input! Must be a float between 0.001 and 1!")
            elif to_change == "5":
                choice = input("Enter TD method (SARSA or QLearning): ")
                if choice == "SARSA" or choice == "sarsa":
                    default_params[3] = "SARSA"
                elif choice == "QLearning" or choice == "qlearning":
                    default_params[3] = "QLearning"
                else:
                    print("Invalid input! Must be 'SARSA' or 'QLearning'!")
            elif to_change == "6":
                choice = input("Use GUI? (y/n): ")
                if choice == "y":
                    default_params[4] = True
                elif choice == "n":
                    default_params[4] = False
                else:
                    print("Invalid input. Must be 'y' or 'n'!")
            else:
                break

    selection = input("Run multiple instances? (y/n): ")
    if selection == "y":
            choice = int(input("Enter number of instances: (-1 for max): "))
            try:
                choice = int(choice)
                if choice > os.cpu_count():
                    print("Invalid input! Must be less than or equal to the number of cores on your machine!")
                elif choice == -1:
                    core_count = os.cpu_count()
                elif choice == 0:
                    print("Invalid input! Must be greater than 0!")
                else:
                    core_count = choice
                default_params[5] = True # we are using multi-threading
            except:
                print("Invalid input! Must be an integer between 0 and the cores on your machine! (-1 for max)")

    elif selection == "n":
        default_params[5] = False
    else:
        print("Invalid input. Must be 'y' or 'n'!")

    arg_string = f"--layout={default_params[0]} \
                   --episodes={default_params[1]} \
                   --ghosts={default_params[2]} \
                   --frametime={default_params[3]} \
                   --method={default_params[3]} \
                   --verbose={default_params[4]} \
                   --multithreaded={default_params[5]}"

    for i in range(core_count):
            p = Process(target=os.system, args=(f"python threaded_executer.py {arg_string}",))
            p.start()

    # pacman.main(layout='smallClassicTest2', episodes=2, frame_time=0.001, method='QLearning', verbose=True)


