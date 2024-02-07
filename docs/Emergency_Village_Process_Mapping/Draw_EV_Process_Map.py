import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from(['999',
                  '111',
                  'GP',
                  'Own accord',
                  'Ambulance',
                  'Walk-in',
                  'Direct referral'])

# Add edges with attributes
edges_with_acuity = [('999', 'Ambulance', '1-2'),
                     ('999', 'Ambulance', '3'),
                     ('111', 'Ambulance', '1-2'),
                     ('111', 'Ambulance', '3'),
                     ('111', 'Walk-in', '4-5'),
                     ('111', 'Direct referral', '4-5'),
                     ('GP', 'Walk-in', '3'),
                     ('GP', 'Direct referral', '3'),
                     ('GP', 'Walk-in', '4-5'),
                     ('GP', 'Direct referral', '4-5'),
                     ('Own accord', 'Walk-in', '1-2'),
                     ('Own accord', 'Walk-in', '3'),
                     ('Own accord', 'Walk-in', '4-5')]

# Filter edges based on acuity
#edges_with_acuity_filtered = [(source, target, acuity) for source, target, acuity in edges_with_acuity if acuity == '4-5']
edges_with_acuity_filtered = [(source, target, acuity) for source, target, acuity in edges_with_acuity]

# Merge edges with the same source and target nodes
merged_edges = {}
for source, target, acuity in edges_with_acuity_filtered:
    if (source, target) in merged_edges:
        merged_edges[(source, target)].append(acuity)
    else:
        merged_edges[(source, target)] = [acuity]

# Add merged edges to the graph with acuity information preserved
for (source, target), acuities in merged_edges.items():
    G.add_edge(source, target, acuities=acuities)

# Draw the graph
pos = nx.circular_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, font_weight='bold', arrows=True)

# Label edges with different colors based on acuity
edge_labels = {(u, v): ", ".join(attr['acuities']) for u, v, attr in G.edges(data=True)}
edge_colors = []
for edge in G.edges():
    u, v = edge
    acuities = edge_labels.get((u, v), '').split(', ')
    # Choose a color based on the highest acuity level among merged edges
    max_acuity = max(acuities)
    if max_acuity == '1-2':
        edge_colors.append('red')
    elif max_acuity == '3':
        edge_colors.append('green')
    elif max_acuity == '4-5':
        edge_colors.append('blue')

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
nx.draw_networkx_edges(G, pos, edge_color=edge_colors)

# Show the plot
plt.show()