import networkx as nx
from pyvis.network import Network
from helper import *


# ##################################################
# 1) Load workpiece graph and feature graph data from json file
# ##################################################

# Note: Available files are: workpiece_graph.json, feature_graph.json

# Load and create graphs
feature_graph_data = load_json("./feature_graph.json")
workpiece_graph_data = load_json("./workpiece_graph.json")

# ##################################################
# 2) Create graphs from loaded data
# ##################################################

# Hint: The library networkx helps you to create a graph. You can use the nx.Graph() class to create a graph.
# Note: Other appraoches are also possible.

feature_graph = create_graph(feature_graph_data)
workpiece_graph = create_graph(workpiece_graph_data)

# Note: Optional task - Visualize the graph
# Example code:
# from pyvis.network import Network
# nt = Network()
# nt.from_nx(workpiece_graph)
# nt.show("graph.html", notebook=False)

# Visualize Graphs
visualize_graph(feature_graph, "feature_graph.html")
visualize_graph_3d(feature_graph, "feature_graph_3d.html")
visualize_graph(workpiece_graph, "workpiece_graph.html")
visualize_graph_3d(workpiece_graph, "workpiece_graph_3d.html")

# ##################################################
# 3) Check if the feature graph is a subgraph of the workpiece workpiece and find any other matching subgraphs
# ##################################################

# 1️ Check if the feature graph is a subgraph of the workpiece graph (Strict Matching)
# Checking if both the type and the cavity status are the same.
GM_strict = nx.algorithms.isomorphism.GraphMatcher(
    workpiece_graph, feature_graph,
    node_match=strict_node_match,
    edge_match=edge_match
)

is_strict_subgraph = GM_strict.subgraph_is_isomorphic()

# Get list of strict matches
matching_subgraphs_strict = list(GM_strict.subgraph_isomorphisms_iter())

# 2️ Check if the feature graph is a subgraph of the workpiece graph (Relaxed Matching)
# Checking if the type is the same.
GM_relaxed = nx.algorithms.isomorphism.GraphMatcher(
    workpiece_graph, feature_graph,
    node_match=relaxed_node_match,
    edge_match=edge_match
)

# Check if relaxed subgraph exists
is_relaxed_subgraph = GM_relaxed.subgraph_is_isomorphic()

# Get list of relaxed matches
matching_subgraphs_relaxed = list(GM_relaxed.subgraph_isomorphisms_iter())

# ##################################################
# 4) Results
# ##################################################

# Print results if matches are found. Return the number of matches and the node ids.
print(f"Strict Subgraph Match: {is_strict_subgraph}")
print(f"Relaxed Subgraph Match: {is_relaxed_subgraph}")

print(f"Number of Relaxed Subgraph Matches: {len(matching_subgraphs_relaxed)}")

print("Relaxed Subgraph Matches:")
for match in matching_subgraphs_relaxed:
    print(f"Match: {match}")
