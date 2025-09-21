import math
import pickle
import random

import pandas as pd
import networkx as nx
# Copied from ChatGPT
import plotly.graph_objects as go

from datasketch import MinHashLSHForest, MinHash
from networkx.algorithms import community

FILE_NAME = 'Pop_Culture.csv'
MIN_SIM = 0.15
NUM_PERM = 128

# The number of edges to include.
TOP_K = 5

MAX_NODES_DRAW = 5_000
MAX_EDGES_DRAW = 100_000
MAX_ROWS = 36927

NEW_GRAPH = True

english_key = {
  'cluster': 'Cluster ID',
  'size': 'Size',
  'fav_heroe': 'Favorite hero',
  'fav_villain': 'Favorite villain',
  'fav_film': 'Favorite film',
  'fav_soundtrack': 'Favorite soundtrack',
  'fav_spaceship': 'Favorite spaceship',
  'fav_planet': 'Favorite planet',
  'fav_robot': 'Favorite robot'
}

random.seed(43)

print('Loading values from file', FILE_NAME)
df = pd.read_csv(FILE_NAME).drop('review_id', axis=1)[:MAX_ROWS] # drop review_id column
rows = len(df)
print('Loaded', rows, 'rows')
column_names = df.columns.tolist()

G = nx.Graph()

if NEW_GRAPH:
  # Build MiniHash and LSH
  print('Building MiniHash and LSH')
  mhs = []
  forest = MinHashLSHForest(num_perm=NUM_PERM)
  for i, row in enumerate(df.itertuples(index=False)):
    G.add_node(i)
    m = MinHash(num_perm=NUM_PERM)
    for atr in row:
      m.update(atr.encode('utf8'))
    forest.add(str(i), m)
    mhs.append(m)

  forest.index()

  print('Building edges')
  for i in range(rows):
    # we don't want to include self-loops
    result = forest.query(mhs[i], TOP_K+1)
    for j in result:
        j = int(j)
        if i == j:
            continue
        weight = mhs[i].jaccard(mhs[j])
        G.add_edge(i, j, weight=weight)
  print('Edges built:', G.number_of_edges())
  pickle.dump(G, open('viz.pickle', 'wb'))

  print('Building communities and metagraph')
  communities = community.louvain_communities(G, weight='weight', resolution=0.3)
  MG = nx.Graph()

  print('Built', len(communities), 'communities')
  # Build a dict associating each node with its community (and summarize the clusters (communities))
  cluster = {}
  summaries = []
  for i, comm in enumerate(communities):
    MG.add_node(i)
    for j in comm:
      cluster[j] = {'cluster': i}

    # Community summary
    summary = { 'cluster': str(i), 'size': str(len(comm)) }
    # Rows associated with community
    df_rows = df.iloc[list(comm)]
    for name, series in df_rows.items():
        vc = series.value_counts(normalize=True)
        v, p = vc.idxmax(), vc.max().item() # value and associated percentage
        summary[name] = f"{v}: {p:.1%}"
    summaries.append(summary)

  print('Setting clusters')

  # Set cluster on each node
  nx.set_node_attributes(G, cluster)
  # pickle.dump(G, open('viz.pickle', 'wb'))

  for u, v, d in G.edges(data=True):
    cu, cv = G.nodes[u]['cluster'], G.nodes[v]['cluster']
    if cu == cv:
      continue
    # Copied from ChatGPT
    if MG.has_edge(cu, cv):
      MG[cu][cv]['weight'] += 1
    else:
      MG.add_edge(cu, cv, weight=1)

  # Central position
  pos_g = {}
  pos_mg = nx.spring_layout(MG, weight='weight')

  # Arrange nodes around central position
  # Copied from ChatGPT
  for m in pos_mg:
    mx, my = pos_mg[m]
    # Small radius
    R = 0.03 * math.sqrt(len(communities[m]))
    for i, n in enumerate(communities[m]):
      t = 2*math.pi * (i / max(1,len(communities[m]))) + random.random()*0.2
      r = R * (0.5 + random.random()*0.5)
      pos_g[n] = [mx + r*math.cos(t), my + r*math.sin(t)]
  p = {
    'G': G,
    'pos_g': pos_g,
    'communities': communities,
    'summaries': summaries
  }
  pickle.dump(p, open('visual.pickle', 'wb'))

else:
  p = pickle.load(open('visual.pickle', 'rb'))
  G = p['G']
  pos_g = p['pos_g']
  communities = p['communities']
  summaries = p['summaries']
  print('Loaded from restore point')

nodes = list(G.nodes())
subgraph_nodes = random.sample(nodes, min(len(nodes), MAX_NODES_DRAW))
H = nx.Graph(G.subgraph(subgraph_nodes))

H.remove_nodes_from(list(nx.isolates(H))) # Prune orphans

# edges = list(H.edges())
# subgraph_edges = random.sample(edges, min(len(edges), MAX_EDGES_DRAW))
# H = H.edge_subgraph(subgraph_edges)

print('Subgraph has', len(H.nodes), 'nodes')
print('Subgraph has', len(H.edges), 'edges')

print('Repositioning nodes')
pos = nx.spring_layout(H, pos=pos_g, weight='weight')

edge_traces = []
for u, v, d in H.edges(data=True):
  x0, y0 = pos[u]
  x1, y1 = pos[v]
  # Copied from ChatGPT
  edge_traces.append(go.Scattergl(x=[x0, x1, None], y=[y0, y1, None], mode='lines',
                          line=dict(width=d['weight']*7.5, color='rgba(0,0,0,0.18)'),
                          hoverinfo='skip', showlegend=False))

# Plotly does not support edges weights :(

palette = ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f',
           '#edc948','#b07aa1','#ff9da7','#9c755f','#bab0ab']

nodes = H.nodes
xs = [pos[n][0] for n in nodes]
ys = [pos[n][1] for n in nodes]
node_colors = [palette[H.nodes[n]['cluster'] % len(palette)] for n in nodes]

print('Formatting summaries')

texts = []
for summary in summaries:
  text = []
  for k, v in summary.items():
    text.append(f'{english_key[k]}: {v}')
  texts.append('<br>'.join(text))

node_trace = go.Scattergl(
    x=xs, y=ys, mode='markers',
    marker=dict(size=10, color=node_colors, line=dict(width=0.3, color='white')),
    hoverinfo='text', text=texts
)

# Copied from ChatGPT
fig = go.Figure(edge_traces +[node_trace])
fig.update_layout(title='A Star Wars Similarity Map',
                  xaxis=dict(visible=False), yaxis=dict(visible=False),
                  plot_bgcolor='white', showlegend=False, height=900,
                  margin=dict(l=10,r=10,t=60,b=10))
fig.write_html("visualize.html", include_plotlyjs='cdn', full_html=True)
