# Creating a Knowledge Graph with Analysed Code Files from any Github Repository
Creating a knowledge graph from any Github repo's software sources.

A multidisciplinary working system was followed in the process of creating the Knowledge Graph. According to this, the project aims to create knowledge graphs by pulling data from a specific GitHub repository using GitHub REST API v3 and Matplotlib libraries. The Knowledge Graph creation project includes the following main steps:
-	Pulling data from repository using Github REST API v3 and Personal Access Token
-	Analyzing the code files
-	Processing their various modules
-	Visualizing with Matplotlib&NetworkX library
-	Creating a knowledge graph based on analyzed and extracted information

## Main Steps
1.	Getting GitHub Repository Information: At project startup, the GitHub API is used to pull basic information from the user-specified GitHub repository:
- Files
- Folders
- Services
- Backbone
2.	Data Analysis and Processing: The captured data is analyzed and processed in Python. In particular, certain data may need to be selected and processed.
3.	Creating a Knowledge Graph with Matplotlib: The processed data was represented as a graph using Matplotlib.
4.	Commissioning of Access Tools: In order to run the main functions mentioned above, this last step aims to enter personal access tokens and other information and ensure successful data flow.

![knowledge_graph](https://github.com/Atakan305/Knowledge-Graph/assets/76012121/699e38ff-bcef-4248-b03b-cb010347f641)

This knowledge graph is created with running the main.py file. By running the same file, the graphic can be displayed in a larger area, the quality of its appearance can be increased, and it can be customized according to personal needs.

In addition, for a further step, this project may also added to Neo4j server and it's possible to analyze the created knowledge graph. On this knowledge graph, queries can be written in the Neo4j DBMS and eventually the fetched data can be further interpreted. 
