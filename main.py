import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

R_ON = 255
W_ON = 100
OFF = 0
vals = [R_ON, OFF, W_ON]
W_birth_rate = 0.02
R_birth_rate = 0.2
empty_rate = 1.0 - W_birth_rate - R_birth_rate
W_birth_chance = 90
W_die_chance = 6
R_birth_chance = 10


def random_grid(n):
    return np.random.choice(vals, n*n, p=[R_birth_rate, empty_rate, W_birth_rate]).reshape(n, n)


def update(frameNum, img, grid, n):
    newGrid = grid.copy()
    for i in range(n):
        for j in range(n):
            #If I'm a rabbit
            if grid[i, j] == R_ON:
                empty_spaces = [(x, y) for x in [(i-1) % n, i, (i+1) % n] for y in [(j-1) % n, j, (j+1) % n] if grid[x, y] == OFF]
                wolves_spaces = [(x, y) for x in [(i-1) % n, i, (i+1) % n] for y in [(j-1) % n, j, (j+1) % n] if grid[x, y] == W_ON]
                if wolves_spaces:
                    newGrid[i, j] == W_ON
                elif len(empty_spaces) > 0:
                    random_move = random.randint(0, len(empty_spaces) - 1) if len(empty_spaces) > 1 else 0
                    newGrid[empty_spaces[random_move]] = R_ON
                    newGrid[i, j] = OFF
                    if random.randint(0, 100) > 100 - R_birth_chance:
                        newGrid[i, j] = R_ON
            #If I'm a wolf
            if grid[i, j] == W_ON:
                rabbits_spaces = [(x, y) for x in [(i-1) % n, i, (i+1) % n] for y in [(j-1) % n, j, (j+1) % n] if grid[x, y] == R_ON]
                if not rabbits_spaces:
                    if random.randint(0, 100) > 100 - W_die_chance:
                        newGrid[i, j] = OFF
                    else:
                        newGrid[i, j] = OFF
                        newGrid[(i + random.randint(-1, 1)) % n, (j + random.randint(-1, 1)) % n] = W_ON
                else:
                    random_move = random.randint(0, len(rabbits_spaces) - 1) if len(rabbits_spaces) > 1 else 0
                    newGrid[rabbits_spaces[random_move]] = W_ON
            elif grid[i, j] == OFF:
                pass
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


def main():
    n = 100
    update_interval = 70
    grid = random_grid(n)

    fig, ax = plt.subplots()    #A few decent looking color themes already applied in matplotlib: summer, hot, afmhot, gist_heat
    img = ax.imshow(grid, interpolation='nearest', cmap='hot')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, n, ),
                                  frames=10, interval=update_interval, save_count=50)

    plt.show()


if __name__ == '__main__':
    main()
