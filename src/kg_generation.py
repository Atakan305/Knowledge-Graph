import networkx as nx
import matplotlib.pyplot as plt

# Create a new Graph
G = nx.DiGraph()

# Variables, classes, functions, and modules
variables = [
    ("dataset_raw", {"type": "variable"}),
    ("LICENCE", {"type": "variable"}),
    ("test.png", {"type": "variable"}),
    ("mnist_net.mat", {"type": "variable"}),
]

classes = [
    ("preprocess", {"type": "class"}),
]

functions = [
    ("extract_labels", {"type": "function"}),
    ("extract_images", {"type": "function"}),
    ("unzipgz", {"type": "function"}),
    ("load_labels", {"type": "function"}),
    ("create_inputs", {"type": "function"}),
]

modules = [
    ("numpy", {"type": "module"}),
    ("cv2", {"type": "module"}),
    ("struct", {"type": "module"}),
    ("extract_mnist", {"type": "module"}),
    ("train.m", {"type": "module"}),
    ("prediction.m", {"type": "module"}),
]

# Add variables, classes, functions, and modules to the graph
G.add_nodes_from(variables)
G.add_nodes_from(classes)
G.add_nodes_from(functions)
G.add_nodes_from(modules)

# Define relationships within the code
relationships = [
    ("extract_mnist", "numpy", {"type": "uses", "description": "uses numpy"}),
    ("extract_mnist", "cv2", {"type": "uses", "description": "uses cv2"}),
    ("extract_mnist", "struct", {"type": "uses", "description": "uses struct"}),
    ("extract_mnist", "extract_labels", {"type": "calls", "description": "calls extract_labels"}),
    ("extract_mnist", "extract_images", {"type": "calls", "description": "calls extract_images"}),
    ("extract_labels", "struct", {"type": "uses", "description": "uses struct"}),
    ("extract_images", "numpy", {"type": "uses", "description": "uses numpy"}),
    ("extract_images", "cv2", {"type": "uses", "description": "uses cv2"}),
    ("preprocess", "unzipgz", {"type": "calls", "description": "calls unzipgz"}),
    ("preprocess", "load_labels", {"type": "calls", "description": "calls load_labels"}),
    ("preprocess", "create_inputs", {"type": "calls", "description": "calls create_inputs"}),
    ("train.m", "preprocess", {"type": "calls", "description": "calls preprocess"}),
    ("train.m", "mnist_net.mat", {"type": "uses", "description": "uses mnist_net.mat"}),
    ("prediction.m", "mnist_net.mat", {"type": "uses", "description": "uses mnist_net.mat"}),
    ("preprocess", "dataset_raw", {"type": "reads", "description": "reads data from dataset_raw"}),
    ("extract_mnist", "dataset_raw", {"type": "reads", "description": "reads data from dataset_raw"}),
]

G.add_edges_from(relationships)

# Draw the graph
pos = nx.spring_layout(G, seed=42)

# Make nodes and edges more detailed
node_colors = {
    "variable": "lightblue",
    "class": "lightgreen",
    "function": "lightcoral",
    "module": "lightgray",
}

edge_colors = {
    "uses": "blue",
    "calls": "red",
    "reads": "green",
}

node_labels = {node: node for node, data in G.nodes(data=True)}
edge_labels = {(source, target): data["description"] for source, target, data in G.edges(data=True)}

nodes = nx.draw_networkx_nodes(G, pos, node_color=[node_colors[data["type"]] for node, data in G.nodes(data=True)])
edges = nx.draw_networkx_edges(G, pos, edge_color=[edge_colors[data["type"]] for source, target, data in G.edges(data=True)])
labels = nx.draw_networkx_labels(G, pos, labels=node_labels)
edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Improve the readability of the graph
plt.legend(node_colors.values(), node_colors.keys(), title="Node Types")
plt.legend(edge_colors.values(), edge_colors.keys(), title="Edge Types")
plt.title("Detailed Information Graph")
plt.axis("off")
plt.show()
