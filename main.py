import numpy as np
from scipy.signal import convolve2d
from matplotlib import pyplot as plt
import scipy.ndimage as ndi
from astar import Solution
import pandas as pd

MAP_SIZE = 100


def make_noise_grid(density: int, height: int, width: int):
    noise_grid = np.random.randint(1, 100, size=(height, width))
    return np.where(noise_grid > density, 0, 1)


def apply_celular_automaton(grid, num_iterations: int):

    for i in range(num_iterations):
        grid =convolve2d(grid, np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]), mode="same")
        grid = np.where((grid > 4) | (grid == 0), 1, 0)
    grid_depth = ndi.gaussian_gradient_magnitude(grid*255, (10, 10))
    return grid, grid_depth

map, depth = apply_celular_automaton(make_noise_grid(60, MAP_SIZE, MAP_SIZE), 5)

scaled_map = (depth-np.min(depth))/(np.max(depth) - np.min(depth))

r = np.where((scaled_map > 0.66), 139, 0) 
g = np.where((scaled_map > 0.33) & (scaled_map <= 0.66), 255, 0) + np.where((scaled_map > 0.66), 69, 0)
b = np.where(scaled_map <= 0.33, 255, 0)

rgb = np.zeros(shape=(MAP_SIZE, MAP_SIZE, 3))
rgb[:, :, 0] = r
rgb[:, :, 1] = g
rgb[:, :, 2] = b

plt.imshow(rgb/255)
plt.savefig("testimage.jpg")
plt.show()


# maps = []
# targets = []
# players = []
# goals = []
# dataset = pd.DataFrame()
# for i in range(1_000):
#     map, depth = apply_celular_automaton(make_noise_grid(60, MAP_SIZE, MAP_SIZE), 10)

#     astar = Solution()
#     player = np.random.randint(0, MAP_SIZE, size=2)
#     goal = np.random.randint(0, MAP_SIZE, size=2)

#     while map[player[0]][player[1]] != 1 and map[goal[0]][goal[1]]:
#         player = np.random.randint(0, MAP_SIZE, size=2)
#         goal = np.random.randint(0, MAP_SIZE, size=2)
#     solution = astar.shortestPathBinaryMatrix(map, player[0], player[1], goal[0], goal[1])
#     if solution != -1:
#         dist_player_goal = np.sqrt(np.sum(np.square(player - goal)))
#         target_label = solution - dist_player_goal
#         maps.append(map.reshape(MAP_SIZE*MAP_SIZE))
#         targets.append(target_label)
#         players.append(player)
#         goals.append(goal)

# pd.DataFrame({"Maps": maps, "Player":players, "Goal": goals, "Target": targets}).to_csv("output/MapData.csv")
        
