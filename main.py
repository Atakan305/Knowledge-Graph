import os
import networkx as nx
import matplotlib.pyplot as plt
import re

#Create a new DiGraph (Directed Graph)
G = nx.DiGraph()

#Define the directory where your code files are stored
code_directory = "your/path/code/directory"

#Define the supported programming languages and their corresponding file extensions
languages = {
    "python": [".py"],
    "matlab": [".m"],
}

#Function to extract relationships from code
def extract_relationships(code, language):
    relationships = []
    if language == "python":
        #Extract object creation, variable assignments, class definitions, module imports, dataflow, database connections, and API calls
        object_creations = re.findall(r'(\w+)\s*=\s*(\w+)\(.+\)', code)
        variable_assignments = re.findall(r'(\w+)\s*=\s*.+', code)
        class_definitions = re.findall(r'classdef\s+(\w+)', code)
        module_imports = re.findall(r'py.importlib.import_module\(\"(\w+)\"\)', code)  # Assuming this pattern for Python module imports
        dataflow = re.findall(r'(\w+)\s*=\s*(\w+)\(.+\)', code)  # Extract source and target from dataflow
        database_connections = re.findall(r'\w+\(.+\)', code)  # Assuming this pattern for database connections
        api_calls = re.findall(r'(\w+)\(.+\)', code)  # Extract only function names as API calls
        #Add a custom "type" based on your criteria, for example, function names
        relationships.extend((source, target, "function") for source, target in object_creations)
        relationships.extend((source, target, "variable") for source in variable_assignments)
        relationships.extend((source, target, "class") for source, target in class_definitions)
        relationships.extend((source, target, "module") for source in module_imports)
        relationships.extend((source, target, "function") for source, target in dataflow)
        relationships.extend((source, target, "database") for source in database_connections)
        relationships.extend((source, function_name, "api") for function_name in api_calls)
    elif language == "matlab":
        #Extract relationships from MATLAB code
        class_definitions = re.findall(r'classdef\s+(\w+)', code)
        function_modules = re.findall(r'function\s+(\w+)', code)
        relationships.extend((source, target, "class") for source in class_definitions for target in function_modules)
    return relationships

#Parse code files in the specified directory
for root, dirs, files in os.walk(code_directory):
    for file in files:
        file_path = os.path.join(root, file)
        language = None
        for lang, extensions in languages.items():
            if any(file.endswith(ext) for ext in extensions):
                language = lang
                break
        if language is None:
            continue  # Skip unsupported file types

        with open(file_path, "r") as f:
            code = f.read()

        relationships = extract_relationships(code, language)

        #Add nodes and edges to the graph
        for source, target, rel_type in relationships:
            G.add_node(source)
            G.add_node(target)
            G.add_edge(source, target, type=rel_type)

#Draw the knowledge graph using the "spring layout" algorithm
pos = nx.spring_layout(G, seed=42)

#Define edge colors
edge_colors = {
    "uses": "blue",
    "calls": "red",
    "reads": "green",
    "class": "black",
    "module": "black",
    "variable": "black",
    "function": "black",
    "database": "black",
    "api": "black",
}

#Draw the graph with node colors
nodes = nx.draw_networkx_nodes(G, pos, node_color="lightgray")

#Draw the edges with edge colors
edges = nx.draw_networkx_edges(G, pos, edge_color=[edge_colors.get(data.get("type", "black")) for _, _, data in G.edges(data=True)])

#Add labels to the nodes
nx.draw_networkx_labels(G, pos, labels={node: node for node in G.nodes()})

#Add labels to the edges
edge_labels = {(source, target): rel_type for source, target, rel_type in G.edges(data="type")}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

#Display the graph with the title and without axis
plt.title("Knowledge Graph")
plt.axis("off")
plt.show()
