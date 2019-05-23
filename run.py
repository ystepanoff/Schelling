import simulation


def two_agents(p1, p2):
    n = 30
    a = [440, 440]
    r = {0: [100.0, p1],
         1: [p2, 100.0]}
    return (n, a, r)


def three_agents(p1, p2, p3):
    n = 30
    a = [290, 290, 290]
    r = {0: [100.0, p1, p1],
         1: [p2, 100.0, p2],
         2: [p3, p3, p3]}
    return n, a, r


def run(test, *args):
    n, sizes, rules = test(*args)
    simulation.run(n, sizes, rules)


#run(two_agents, 50.0, 50.0)
#run(two_agents, 60.0, 60.0)
# run(three_agents)

if __name__ == '__main__':
    run(two_agents, 50.0, 50.0)
