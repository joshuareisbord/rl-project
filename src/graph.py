from matplotlib import pyplot as plt
import os
import json


def average_directory(directory, x_idx, y_idx):
    """
    Averages all the files in a directory
    """
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

def graph(x, y, labels):
    """
    Graphs a list of x and y values with labels
    """
    plt.plot(x, y)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.show()

if __name__ == "__main__":

    dir = str(os.getcwd()) + "/run_stats/"

    labels = ["x", "y"]

    print("1. Episode")
    print("2. Total Timesetps")
    print("3. Episode Timesteps")
    print("4. Total Reward")
    print("5. Episode Reward")
    print("X Axis: ", end="")
    x_idx = int(input(""))
    if x_idx == 1:
        labels[0] = "Episode"
    elif x_idx == 2:
        labels[0] = "Total Timesteps"
    elif x_idx == 3:
        labels[0] = "Episode Timesteps"
    elif x_idx == 4:
        labels[0] = "Total Reward"
    elif x_idx == 5:
        labels[0] = "Episode Reward"

    print("1. Episode")
    print("2. Total Timesetps")
    print("3. Episode Timesteps")
    print("4. Total Reward")
    print("5. Episode Reward")
    print("Y Axis: ", end="")
    y_idx = int(input(""))
    if y_idx == 1:
        labels[1] = "Episode"
    elif y_idx == 2:
        labels[1] = "Total Timesteps"
    elif y_idx == 3:
        labels[1] = "Episode Timesteps"
    elif y_idx == 4:
        labels[1] = "Total Reward"
    elif y_idx == 5:
        labels[1] = "Episode Reward"


    stats = average_directory(dir, x_idx, y_idx)
    graph(stats[0], stats[1], labels)