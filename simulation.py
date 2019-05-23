import random
import matplotlib.pyplot as plot
import matplotlib.animation as animation

dx = [1, 1, 1, 0, -1, -1, -1, 0]
dy = [-1, 0, 1, 1, 1, 0, -1, -1]

random.seed()


def satisfied(grid, x, y, types, rules):
    def exists(n, x, y):
        return x >= 0 and y >= 0 and x < n and y < n

    t = grid[x][y] - 1
    neighbours = [0] * types
    for i in range(types):
        neighbours[i] = sum([1 for k in range(len(dx)) if
                             exists(len(grid), x + dx[k], y + dy[k]) and grid[x + dx[k]][y + dy[k]] == i + 1])
    total = sum(neighbours)
    if total > 0:
        neighbours = list(map(lambda r: r / total * 100.0, neighbours))
    for i in range(types):
        if neighbours[i] > rules[t][i]:
            return False
    return True


def find_positions(grid, x, y, types, rules):
    n = len(grid)
    t = grid[x][y]
    grid[x][y] = 0
    available = []
    for i in range(n):
        for j in range(n):
            if (i != x or j != y) and grid[i][j] == 0:
                grid[i][j] = t
                if satisfied(grid, i, j, types, rules):
                    available.append((i, j))
                grid[i][j] = 0
    grid[x][y] = t
    return available


def make_step(frame, image, types, grid, rules):
    def no_choice(list):
        for x, y in list:
            available = find_positions(grid, x, y, types, rules)
            if len(available) > 0:
                return False
        return True

    n = len(grid)
    unhappy = [(i, j) for i in range(n) for j in range(n)
               if grid[i][j] > 0 and not satisfied(grid, i, j, types, rules)]
    if no_choice(unhappy):
        print('Nowhere to go!')
        return None

    if len(unhappy) > 0:
        x, y = random.choice(unhappy)
        available = find_positions(grid, x, y, types, rules)
        while len(available) == 0:
            x, y = random.choice(unhappy)
            available = find_positions(grid, x, y, types, rules)
        newx, newy = random.choice(available)
        grid[newx][newy] = grid[x][y]
        grid[x][y] = 0

    image.set_data(grid)
    return image


def make_step_simultaneously(frame, image, types, grid, rules):
    def no_choice(list):
        for x, y in list:
            available = find_positions(grid, x, y, types, rules)
            if len(available) > 0:
                return False
        return True

    n = len(grid)
    unhappy = [(i, j) for i in range(n) for j in range(n)
               if grid[i][j] > 0 and not satisfied(grid, i, j, types, rules)]
    if no_choice(unhappy):
        print('Nowhere to go!')
        return None

    grid_next = grid.copy()
    for x, y, in unhappy:
        available = find_positions(grid, x, y, types, rules)
        if len(available) > 0:
            newx, newy = random.choice(available)
            grid_next[newx][newy] = grid[x][y]
            grid_next[x][y] = 0
    grid[:] = grid_next[:]

    image.set_data(grid)
    return image


def random_grid(n, a, rules):
    grid = [[0 for i in range(n)] for j in range(n)]
    coords = [(i, j) for i in range(n) for j in range(n)]
    types = len(a)
    for t in range(types):
        for i in range(a[t]):
            x, y = random.choice(coords)
            coords.remove((x, y))
            grid[x][y] = t + 1
    return types, grid, rules


def run(n, sizes, rules, video_file=None):
    types, grid, rules = random_grid(n, sizes, rules)

    fig, ax = plot.subplots()
    plot.axis('off')

    image = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, make_step, frames=1000,
                                  fargs=(image, types, grid, rules), interval=10)

    if video_file:
        ani.save(mov_file, writer=animation.FFMpegWriter(fps=60))
    plot.show()
