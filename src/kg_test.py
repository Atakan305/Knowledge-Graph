import os
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import requests

def safe_makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        if e.errno == 36:  # If the file name is too long
            # Shorten the file name
            short_path = path[:100]  # For example, limit it to 100 characters
            os.makedirs(short_path, exist_ok=True)
        else:
            raise e

def clone_repository(repo_owner, repo_name, local_path, token):
    # Fetch data from a repository using the GitHub API
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        clone_url = repo_data['clone_url']

        # Create the Git clone command
        clone_command = ['git', 'clone', clone_url, local_path]

        try:
            subprocess.run(clone_command, check=True)
            print(f"Repository '{repo_name}' successfully cloned to '{local_path}'.")
        except subprocess.CalledProcessError as e:
            print(f"Repository cloning failed. Error: {e}")
    else:
        print(f"Unable to fetch repository information. Status code: {response.status_code}")

def build_folder_structure(root_folder):
    folder_structure = {}

    for root, dirs, files in os.walk(root_folder):
        folder_structure[root] = {
            "dirs": dirs,
            "files": files
        }

    return folder_structure

def build_knowledge_graph(folder_structure):
    G = nx.Graph()

    for folder, content in folder_structure.items():
        G.add_node(folder, type="folder")

        for subfolder in content["dirs"]:
            G.add_edge(folder, os.path.join(folder, subfolder), type="contains")

        for file in content["files"]:
            # Make the file name unique to distinguish files with the same name
            file_name = file
            counter = 1
            while G.has_node(os.path.join(folder, file_name)):
                file_name = f"{os.path.splitext(file)[0]}_{counter}{os.path.splitext(file)[1]}"
                counter += 1

            G.add_node(os.path.join(folder, file_name), type="file")
            G.add_edge(folder, os.path.join(folder, file_name), type="contains")

    return G

def visualize_graph(graph, figsize=(20, 20), node_size=100, font_size=8):
    pos = nx.circular_layout(graph)
    plt.figure(figsize=figsize)

    node_colors = ["lightblue" if "type" not in graph.nodes[node] else "lightcoral" if graph.nodes[node]["type"] == "file" else "lightgreen" for node in graph.nodes]
    edge_colors = ["gray" for _ in graph.edges]

    # Add an edge attribute to provide information on the edges
    edge_labels = {}
    for u, v, data in graph.edges(data=True):
        edge_labels[(u, v)] = data.get("type", "")

    nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color=node_colors)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
    nx.draw_networkx_labels(graph, pos, font_size=font_size, font_color="black")
    
    # Display edges with labels
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)

    plt.show()

def main():
    repo_owner = 'suhedaras'
    repo_name = 'deepface' 
    local_path = 'test'
    token = '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'  # GitHub Personal Access Token

    safe_makedirs(local_path)
    clone_repository(repo_owner, repo_name, local_path, token)

    root_folder = local_path
    folder_structure = build_folder_structure(root_folder)
    knowledge_graph = build_knowledge_graph(folder_structure)

    print("Folder Structure:")
    for folder, content in folder_structure.items():
        print(f"{folder}/")
        for subfolder in content["dirs"]:
            print(f"  - {subfolder}/")
        for file in content["files"]:
            print(f"  - {file}")

    visualize_graph(knowledge_graph)

if __name__ == "__main__":
    main()
