import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

GRAPH_SIZE = 100
ITERATIONS = 100
NUM_RUNS = 20
NUM_COLOURS = 6
EDGE_PROBABILITY = 0.05

# Function to count the number of conflicts
def count_conflicts(g):
    _conflicts = 0
    for edge in g.edges:
        if g.nodes[edge[0]]['color'] == g.nodes[edge[1]]['color']:
            _conflicts += 1
    return _conflicts


# Define the list of colours using NUM_COLOURS
colours = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'white', 'black', 'grey', 'cyan',
           'magenta', 'lime', 'olive', 'maroon', 'navy', 'teal', 'silver', 'gold', 'indigo', 'violet', 'tan',
           'turquoise', 'salmon', 'plum', 'orchid', 'peru', 'khaki', 'lavender', 'ivory', 'honeydew', 'fuchsia',
           'coral', 'chartreuse', 'azure', 'aquamarine', 'bisque', 'beige', 'aliceblue', 'antiquewhite', 'aqua',
           'aquamarine', 'azure', 'blanchedalmond', 'blueviolet']
colours = colours[:NUM_COLOURS]
conflicts_over_time = [[] for _ in range(NUM_RUNS)]
for i in range(NUM_RUNS):

    G = nx.erdos_renyi_graph(GRAPH_SIZE, EDGE_PROBABILITY)

    # Randomly assign colors to the nodes
    for node in G.nodes:
        G.nodes[node]['color'] = np.random.choice(colours)

    lowest_conflicts = (GRAPH_SIZE * (GRAPH_SIZE - 1)) / 2
    best_coloring = []

    for node in G.nodes:
        G.nodes[node]['color'] = np.random.choice(colours)

    for _ in range(ITERATIONS):
        for node in G.nodes:
            conflict = False
            for neighbor in G.neighbors(node):
                if G.nodes[node]['color'] == G.nodes[neighbor]['color']:
                    conflict = True
                    break
            if conflict:
                G.nodes[node]['color'] = np.random.choice(colours)

        # Count the number of conflicts
        conflicts = count_conflicts(G)
        if conflicts < lowest_conflicts:
            lowest_conflicts = conflicts
            best_coloring = [G.nodes[i]['color'] for i in G.nodes]
        conflicts_over_time[i].append(conflicts)

# Plot the number of conflicts over time
plt.figure(figsize=(8, 8))
for i in range(NUM_RUNS):
    plt.plot(conflicts_over_time[i])

print(conflicts_over_time)
# plot the average number of conflicts
average_conflicts = np.mean(conflicts_over_time, axis=0)
print(average_conflicts)
plt.plot(average_conflicts, 'k--', label='Average number of conflicts')
plt.xlabel('Iteration number')
plt.ylabel('Number of conflicts')
plt.title('Number of conflicts over time')
# Add gridlines
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 8))
# plot the best graph
for node in G.nodes:
    G.nodes[node]['color'] = best_coloring[node]
nx.draw(G, with_labels=True, node_color=[G.nodes[i]['color'] for i in G.nodes])
plt.show()
