from neo4j import GraphDatabase
import os
import subprocess
import requests
import networkx as nx

# Define your GitHub token here
github_token = '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'

class GitHubRepoLoader:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self._driver.close()

    def clone_repository(self, tx, repo_owner, repo_name, local_path):
        # Fetching the data from a repository with GitHub API
        api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
        headers = {
            'Authorization': f'token {github_token}'
        }
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            repo_data = response.json()
            clone_url = repo_data['clone_url']

            # Construct the git clone command
            clone_command = ['git', 'clone', clone_url, local_path]

            try:
                subprocess.run(clone_command, check=True)
                print(f"Repository '{repo_name}' cloned successfully to '{local_path}' folder.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to clone repository. Error: {e}")
        else:
            print(f"Failed to fetch repository information. Status code: {response.status_code}")

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
            file_name = file
            counter = 1
            while G.has_node(os.path.join(folder, file_name)):
                file_name = f"{os.path.splitext(file)[0]}_{counter}{os.path.splitext(file)[1]}"
                counter += 1

            G.add_node(os.path.join(folder, file_name), type="file")
            G.add_edge(folder, os.path.join(folder, file_name), type="contains")

    return G

def main():
    repo_owner = 'Atakan305'
    repo_name = 'UAV-UCAV-Projects' 
    local_path = 'with_neo4j'

    loader = GitHubRepoLoader("neo4j://localhost:7687", "neo4j", "Atiba2030!")  #Neo4j Connection Details

    with loader._driver.session() as session:
        session.write_transaction(loader.clone_repository, repo_owner, repo_name, local_path)

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

if __name__ == "__main__":
    main()
