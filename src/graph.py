import os
import json
from matplotlib import pyplot as plt

def graph():
    """
    Graphs the data collected from a run.
    """
    x_label = ""
    y_label = ""

    print("1. Episode")
    print("2. Total Timesetps")
    print("3. Episode Timesteps")
    print("4. Total Reward")
    print("5. Episode Reward")

    x_idx = int(input("X Axis: "))
    y_idx = int(input("Y Axis: "))

    if x_idx == 1:
        x_label = "Episode"
    elif x_idx == 2:
        x_label = "Total Timesteps"
    elif x_idx == 3:
        x_label = "Episode Timesteps"
    elif x_idx == 4:
        x_label = "Total Reward"
    elif x_idx == 5:
        x_label = "Episode Reward"

    if y_idx == 1:
        y_label = "Episode"
    elif y_idx == 2:
        y_label = "Total Timesteps"
    elif y_idx == 3:
        y_label = "Episode Timesteps"
    elif y_idx == 4:
        y_label = "Total Reward"
    elif y_idx == 5:
        y_label = "Episode Reward"
        

    graphData(x_idx, y_idx, x_label, y_label)

def graphData(x_idx, y_idx, x_label, y_label):
    """
    Graphs a list of x and y values with labels
    """

    q_learning = averageDirectory('q_learning', x_idx, y_idx)
    sarsa = averageDirectory('sarsa', x_idx, y_idx)

    # plt.plot(q_learning[0], q_learning[1], label='Q Learning')
    plt.plot(sarsa[0], sarsa[1], label='SARSA')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()

def averageDirectory(method, x_idx, y_idx):
    """
    Averages all the files in a directory for a given x and y index
    """

    directory = f"{str(os.getcwd())}/run_stats/{method}/"

    min_episodes = float('inf')
    x = []
    y = []
    files = 0
    for file in os.listdir(directory):
        f = os.path.join(directory, file)

        if os.path.isfile(f):
            files += 1
            with open(f, 'r') as f:
                lst = json.load(f)
                if len(lst[1]) < min_episodes:
                    min_episodes = len(lst[1])
                x.append(lst[x_idx])
                y.append(lst[y_idx])

    print(min_episodes)

    x_avg = []
    y_avg = []
    
    for i in range(min_episodes): # for each element up too the length of the shortest list
        tmp_x = 0
        tmp_y = 0
        for j in range(files): # in each file
            tmp_x += x[j][i]
            tmp_y += y[j][i]
        tmp_x /= files
        tmp_y /= files
        x_avg.append(round(tmp_x, 2))
        y_avg.append(round(tmp_y, 2))
    
    return x_avg, y_avg

if __name__ == "__main__":
    graph()