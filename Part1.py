import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

GRAPH_SIZE = 20

# Define the list of colors
colors = ['red', 'green', 'blue', 'yellow', 'purple']

G = nx.erdos_renyi_graph(GRAPH_SIZE, 0.1)

# Randomly assign colors to the nodes
for node in G.nodes:
    G.nodes[node]['color'] = np.random.choice(colors)

# Function to count the number of conflicts
def count_conflicts(G):
    conflicts = 0
    for edge in G.edges:
        if G.nodes[edge[0]]['color'] == G.nodes[edge[1]]['color']:
            conflicts += 1
    return conflicts


lowest_conflicts = (GRAPH_SIZE * (GRAPH_SIZE - 1)) / 2
best_coloring = []

iterations = 100
conflicts_over_time = []
for _ in range(iterations):
    # Randomly assign colors to the nodes
    for node in G.nodes:
        G.nodes[node]['color'] = np.random.choice(colors)
    # Count the number of conflicts
    conflicts = count_conflicts(G)
    if conflicts < lowest_conflicts:
        lowest_conflicts = conflicts
        best_coloring = [G.nodes[i]['color'] for i in G.nodes]
    conflicts_over_time.append(conflicts)

plt.figure(figsize=(8, 8))
# plot the best graph
for node in G.nodes:
    G.nodes[node]['color'] = best_coloring[node]
nx.draw(G, with_labels=True, node_color=[G.nodes[i]['color'] for i in G.nodes])
plt.show()

# Plot the number of conflicts over time
plt.plot(conflicts_over_time)
plt.xlabel('Experiment')
plt.ylabel('Number of conflicts')
plt.title('Number of conflicts over time')
plt.show()





