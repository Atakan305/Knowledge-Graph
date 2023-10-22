import os
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import requests

def create_directories_safely(path):
    #Safely create directories without raising errors
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        if e.errno == 36:  #Create the condition that the file path is long
            #Shorten the file name
            short_path = path[:50]  #Limit it to 50 characters
            os.makedirs(short_path, exist_ok=True)
        else:
            raise e

def clone_repository(repo_owner, repo_name, local_path, token):
    #Fetch data from a repository using the GitHub REST API v3
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        clone_url = repo_data['clone_url']

        #Create the Git clone command
        clone_command = ['git', 'clone', clone_url, local_path]

        try:
            subprocess.run(clone_command, check=True)
            print(f"Repository '{repo_name}' successfully cloned to '{local_path}'.")
        except subprocess.CalledProcessError as e:
            print(f"Repository cloning failed. Error: {e}")
    else:
        print(f"Repository information couldn't be retrieved. Status code: {response.status_code}")

def build_folder_structure(root_folder):
    #Build a dictionary representing the folder structure
    folder_structure = {}

    for root, dirs, files in os.walk(root_folder):
        folder_structure[root] = {
            "dirs": dirs,
            "files": files
        }

    return folder_structure

def build_knowledge_graph(folder_structure):
    #Build a knowledge graph based on the folder structure
    G = nx.Graph()

    for folder, content in folder_structure.items():
        G.add_node(folder, type="folder")

        for subfolder in content["dirs"]:
            G.add_edge(folder, os.path.join(folder, subfolder), type="contains")

        for file in content["files"]:
            #Make the file name unique to distinguish files with the same name
            file_name = file
            counter = 1
            while G.has_node(os.path.join(folder, file_name)):
                file_name = f"{os.path.splitext(file)[0]}_{counter}{os.path.splitext(file)[1]}"
                counter += 1

            G.add_node(os.path.join(folder, file_name), type="file")
            G.add_edge(folder, os.path.join(folder, file_name), type="contains")

    return G

def visualize_graph(graph, figsize=(12, 12), node_size=50, font_size=8):
    #Visualize the knowledge graph using Matplotlib
    plt.figure(figsize=figsize)
    
    pos = nx.spring_layout(graph, seed=42)  # Use spring_layout for a better layout

    #Specify node colors
    node_colors = ["lightblue" if "type" not in graph.nodes[node] else "lightcoral" if graph.nodes[node]["type"] == "file" else "lightgreen" for node in graph.nodes]

    #Make edges thinner and draw edges in different colors
    edge_colors = "gray"
    width = 0.5

    #Specify node labels
    node_labels = {}
    for node in graph.nodes:
        node_labels[node] = os.path.basename(node)

    #Specify edge labels
    edge_labels = {}
    for u, v in graph.edges():
        edge_labels[(u, v)] = graph[u][v]['type']

    #Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color=node_colors, alpha=0.8)

    #Draw edges
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=width)

    #Add node labels
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=font_size, font_color="black")

    #Add edge labels
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=font_size, font_color="black")

    #Add a title to the graph
    plt.title("Knowledge Graph", fontsize=16)

    #plt.axis('off') #If you don't want to label all graph you can use this...
    plt.show()

def main():
    # Configuration
    repo_owner = 'akdenizz'
    repo_name = 'yolov5_object_detection' 
    local_path = 'example'
    token = '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'  # GitHub Personal Access Token

    #Safely create local directories
    create_directories_safely(local_path)

    #Clone the GitHub repository
    clone_repository(repo_owner, repo_name, local_path, token)

    #Build the folder structure
    root_folder = local_path
    folder_structure = build_folder_structure(root_folder)

    #Build the knowledge graph
    knowledge_graph = build_knowledge_graph(folder_structure)

    #Print the folder structure
    print("Folder Structure:")
    for folder, content in folder_structure.items():
        print(f"{folder}/")
        for subfolder in content["dirs"]:
            print(f"  - {subfolder}/")
        for file in content["files"]:
            print(f"  - {file}")

    #Visualize the knowledge graph
    visualize_graph(knowledge_graph)

if __name__ == "__main__":
    main()
