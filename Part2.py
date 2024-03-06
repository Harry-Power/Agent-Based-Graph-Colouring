import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

GRAPH_SIZE = 40
ITERATIONS = 100
NUM_RUNS = 20
NUM_COLOURS = 6
EDGE_PROBABILITY = 0.1


# Function to count the number of conflicts
def count_conflicts(g):
    _conflicts = 0
    for edge in g.edges:
        if g.nodes[edge[0]]['color'] == g.nodes[edge[1]]['color']:
            _conflicts += 1
    return _conflicts


# Define the list of colours using NUM_COLOURS
colours = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'white', 'grey', 'cyan',
           'magenta', 'lime', 'olive', 'maroon', 'navy', 'teal', 'silver', 'gold', 'indigo', 'violet', 'tan',
           'turquoise', 'salmon', 'plum', 'orchid', 'peru', 'khaki', 'lavender', 'ivory', 'honeydew', 'fuchsia',
           'coral', 'chartreuse', 'azure', 'aquamarine', 'bisque', 'beige', 'aliceblue', 'antiquewhite', 'aqua',
           'aquamarine', 'azure', 'blanchedalmond', 'blueviolet']
colours = colours[:NUM_COLOURS]
conflicts_over_time = [[] for _ in range(NUM_RUNS)]
for i in range(NUM_RUNS):

    # Generate a random graph
    G = nx.erdos_renyi_graph(GRAPH_SIZE, EDGE_PROBABILITY)
    # G = nx.random_regular_graph(3, GRAPH_SIZE)
    # Small world graph
    # G = nx.newman_watts_strogatz_graph(GRAPH_SIZE, 5, 0.5)

    # Randomly assign colors to the nodes
    for node in G.nodes:
        G.nodes[node]['color'] = np.random.choice(colours)

    lowest_conflicts = (GRAPH_SIZE * (GRAPH_SIZE - 1)) / 2  # initially worst case scenario number
    best_coloring = []  # best coloured graph

    for node in G.nodes:
        G.nodes[node]['color'] = np.random.choice(colours)

    for _ in range(ITERATIONS):
        buffer = list(G.nodes[node]['color'] for node in G.nodes)
        for (node, j) in enumerate(G.nodes):

            # Get the colors of the neighboring nodes
            neighboursColours = [G.nodes[neighbour]['color'] for neighbour in G.neighbors(node)]

            # If the color of the current node is in the colors of the neighboring nodes
            if G.nodes[node]['color'] in neighboursColours:
                # Get the colors of the neighbors of the neighbors of the current node
                # Exclude the current node and its direct neighbors
                coloursNeighboursWontUse = \
                    [G.nodes[neighboursNeighbour]['color']
                     for neighbour in G.neighbors(node)
                     if G.nodes[neighbour]['color'] != G.nodes[node]['color']
                     for neighboursNeighbour in G.neighbors(neighbour)
                     if neighboursNeighbour != node and neighboursNeighbour != neighbour]

                # Get the colors the neighbours won't use that aren't used by the neighbours
                coloursNeighboursWontAndDontUse = \
                    set(coloursNeighboursWontUse) - set(neighboursColours)
                # If there are any such colors, randomly choose one and assign it to the current node
                if coloursNeighboursWontAndDontUse:
                    buffer[j] = np.random.choice(list(coloursNeighboursWontAndDontUse))
                else:
                    # If there are any such colors, randomly choose one not used by the neighbors
                    availableColours = set(colours) - set(neighboursColours)
                    if availableColours:
                        buffer[j] = np.random.choice(list(availableColours))

        # # Recolor the nodes where there are conflicts
        # for (node, j) in enumerate(G.nodes):
        #     G.nodes[j]['color'] = buffer[j]
        for (node, j) in enumerate(G.nodes):
            neighborColours = [G.nodes[neighbor]['color'] for neighbor in G.neighbors(node)]
            if G.nodes[node]['color'] in neighborColours:
                availableColours = [colour for colour in colours if colour not in neighborColours]
                if len(availableColours) > 0:
                    buffer[j] = np.random.choice(availableColours)

        # Recolor the nodes where there are conflicts
        for (node, j) in enumerate(G.nodes):
            G.nodes[j]['color'] = buffer[j]

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

plt.figure(figsize=(10, 10))
# plot the best graph
for node in G.nodes:
    G.nodes[node]['color'] = best_coloring[node]
nx.draw(G, with_labels=True, node_color=[G.nodes[i]['color'] for i in G.nodes])
plt.show()
