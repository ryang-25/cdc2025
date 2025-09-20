import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import pickle

from networkx.algorithms import community

G = nx.Graph()
# G = pickle.load(open('viz.pickle', 'rb'))
df = pd.read_csv('Pop_Culture.csv')
num_nodes = 30

for i, row in df.iterrows():
    if i >= 30:
        break
    review_id = row['review_id']
    attrs = row.drop('review_id').to_dict()
    G.add_node(review_id, **attrs)

for node1, attrs1 in G.nodes(data=True):
    for node2, attrs2 in G.nodes(data=True):
        if node1 == node2:
            pass
        shared = sum(1 for e1, e2 in zip(attrs1.values(), attrs2.values()) if e1 == e2)
        if shared > 0:
            G.add_edge(node1, node2, weight=shared)


communities = community.greedy_modularity_communities(G)
color_map = {node: i for i, com in enumerate(communities) for node in com}
colors = [color_map[node] for node in G.nodes()]

# Draw graph
pos = nx.spring_layout(G, seed=42)
weights = [G[u][v]['weight'] for u, v in G.edges()]
nx.draw(G, pos, with_labels=True, node_color=colors, cmap=plt.cm.Set3,
        edge_color=weights, edge_cmap=plt.cm.Blues, width=2.0)
plt.title("Review ID Graph Clustered by Shared Attributes")
plt.show()

plt.savefig("test.png")

print("done")

pickle.dump(G, open('viz.pickle', 'wb'))

# for u, v in combinations()

# comms = nx.community.louvain_communities(G, weight='weight', seed=0)

# kmeans = KMeans(n_clusters=2, random_state=0, n_init)
