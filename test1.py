import networkx as nx
import matplotlib.pyplot as mpl

g = nx.Graph()
g.add_edge(1, 2, weight=80)
g.add_node(3)

nx.draw_spring(g, with_labels=True)
mpl.show()