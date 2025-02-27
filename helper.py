import json
import networkx as nx
from pyvis.network import Network

# ----------------------------------------------
# Load JSON Data with Error Handling
# ----------------------------------------------
def load_json(filepath):
    """
    Loads JSON data from a given file path and handles file errors.

    Args:
        filepath (str): Path to the JSON file

    Returns:
        dict: Loaded JSON data or None if error occurs
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' is not a valid JSON file.")
        return None
    

# ----------------------------------------------
# Create a Graph from JSON Data
# ----------------------------------------------
def create_graph(data):
    """
    Creates a NetworkX graph from JSON data.

    Args:
        data (dict): Dictionary containing 'nodes' and 'edges' lists
            nodes format: [(node_id, {attributes}), ...]
            edges format: [(node1, node2, {attributes}), ...]

    Returns:
        nx.Graph: NetworkX graph object or None if data is invalid
    """
    if data is None:
        return None

    G = nx.Graph()

    # Add nodes with attributes (node_id and associated attribute dictionary)
    for node_id, node_attr in data["nodes"]:
        G.add_node(node_id, **node_attr)

    # Add edges with attributes (source node, target node, and attribute dictionary)
    for edge in data["edges"]:
        node1, node2, edge_attr = edge
        G.add_edge(node1, node2, **edge_attr)

    return G


# ----------------------------------------------
# 2D Graph Visualization using PyVis
# ----------------------------------------------
def visualize_graph(graph, filename):
    """
    Creates an interactive 2D graph visualization using PyVis.

    Args:
        graph (nx.Graph): NetworkX graph object
        filename (str): File name to save the visualization (HTML file)
    """
    if graph is None:
        return

    # Initialize PyVis Network
    nt = Network(notebook=False, height="750px", width="100%")
    
    # Add nodes with labels
    for node, data in graph.nodes(data=True):
        node_label = f"{node} ({data.get('type', 'Unknown')})"
        nt.add_node(node, label=node_label, color="lightblue" if data.get("cavity", False) else "lightgreen")

    # Add edges with labels
    for edge in graph.edges(data=True):
        edge_label = edge[2].get("angular_type", "")
        nt.add_edge(edge[0], edge[1], title=edge_label)

    # Save and open graph visualization
    nt.show(filename, notebook=False)


# ----------------------------------------------
#3D Graph Visualization using PyVis
# ----------------------------------------------
def visualize_graph_3d(graph, filename):
    """
    Creates an interactive 3D graph visualization using PyVis.

    Args:
        graph (nx.Graph): NetworkX graph object
        filename (str): File name to save the visualization (HTML file)
    """
    if graph is None:
        return

    # Initialize PyVis Network with Dark Mode
    nt = Network(notebook=False, height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Enable physics for 3D floating effect
    nt.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.05)

    # Define different shapes & colors for node types
    node_styles = {
        "plane": {"shape": "circle", "color": "#4CAF50"},  # Green
        "cylinder": {"shape": "box", "color": "#FFA500"},  # Orange
        "cone": {"shape": "triangle", "color": "#FF5733"},  # Red
        "torus": {"shape": "diamond", "color": "#33C3FF"},  # Blue
        "default": {"shape": "ellipse", "color": "#FFFFFF"}  # White
    }

    # Add nodes with labels and custom styling
    for node, data in graph.nodes(data=True):
        node_type = data.get("type", "default")  # Get node type
        node_shape = node_styles.get(node_type, node_styles["default"])  # Get styling

        node_label = f"{node} ({node_type})"
        node_color = "lightblue" if data.get("cavity", False) else node_shape["color"]

        nt.add_node(node, label=node_label, color=node_color, shape=node_shape["shape"], size=20)

    # Add edges with labels and better thickness
    for edge in graph.edges(data=True):
        edge_label = edge[2].get("angular_type", "")
        nt.add_edge(edge[0], edge[1], title=edge_label, width=2)

    # Save and open graph visualization
    nt.show(filename, notebook=False)


# ----------------------------------------------
# Graph Matching Functions for Subgraph Isomorphism
# ----------------------------------------------
def strict_node_match(n1, n2):
    """
    Matches nodes strictly based on type and cavity status.

    Args:
        n1 (dict): Attributes of the first node
        n2 (dict): Attributes of the second node

    Returns:
        bool: True if the nodes match strictly, False otherwise
    """
    return n1.get("type") == n2.get("type") and n1.get("cavity") == n2.get("cavity")


def relaxed_node_match(n1, n2):
    """
    Matches nodes based only on type (ignores cavity status).

    Args:
        n1 (dict): Attributes of the first node
        n2 (dict): Attributes of the second node

    Returns:
        bool: True if the node types match, False otherwise
    """
    return n1.get("type") == n2.get("type")


def edge_match(e1, e2):
    """
    Matches edges based on angular type.

    Args:
        e1 (dict): Attributes of the first edge
        e2 (dict): Attributes of the second edge

    Returns:
        bool: True if the angular types match, False otherwise
    """
    return e1.get("angular_type") == e2.get("angular_type")