import random
from antsystem import AntColonySystem
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
import numpy as np
from matplotlib.animation import FuncAnimation


# def main():
#     n = 10
#     c = [(10*random(), 10*random()) for i in range(n)]
#
#     a = AntColonySystem(n, c)
#     solution = a.findSolution()
#     graph = []
#     for i in range(len(a.cityLocations)):
#         for j in range(i+1, len(a.cityLocations)):
#             graph.append((i, j, a.distance(i, j)))


n = 4
G = nx.complete_graph(n)
pos = nx.spring_layout(G)
nodes = nx.draw_networkx_nodes(G, pos)
edges = nx.draw_networkx_edges(G, pos)
fig = plt.figure()
node_colors = np.random.randint(0, 100, size=(10, 4))


def animation(i):
    colors = [random.choice(['r', 'b', 'g', 'y']) for i in range(4)]
    nodes.set_array(node_colors[i])
    return nodes,


anim = FuncAnimation(fig, animation, frames=4, interval=50, blit=True)