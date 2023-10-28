# Creating a Knowledge Graph with Analysed Code Files from any Github Repository
Creating a knowledge graph from any Github repo's software sources.

A multidisciplinary working system was followed in the process of creating the Knowledge Graph. According to this, the project aims to create knowledge graphs by pulling data from a specific GitHub repository using GitHub REST API v3 and Matplotlib libraries. The Knowledge Graph creation project includes the following main steps:
-	Pulling data from repository using Github REST API v3 and Personal Access Token
-	Analyzing the code files
-	Processing their various modules
-	Visualizing with Matplotlib&NetworkX library
-	Creating a knowledge graph based on analyzed and extracted information

## Main Steps
The primary objectives of this project were as follows:
1. Analyze code files written in Python and MATLAB to extract relationships between entities.
2. Create a knowledge graph representing these relationships.
3. Import the knowledge graph into a Neo4j database for querying and visualization.

The code analysis component involves parsing source code files written in Python and MATLAB to extract relationships between entities. The relationships include function calls, object creations, variable assignments, class definitions, module imports, dataflow, database connections, and API calls. The extracted relationships are categorized based on their type.
-

![knowledge_graph](https://github.com/Atakan305/Knowledge-Graph/assets/76012121/699e38ff-bcef-4248-b03b-cb010347f641)

This knowledge graph is created with running the main.py file. By running the same file, the graphic can be displayed in a larger area, the quality of its appearance can be increased, and it can be customized according to personal needs.

In addition, for a further step, this project may also added to Neo4j server and it's possible to analyze the created knowledge graph. On this knowledge graph, queries can be written in the Neo4j DBMS and eventually the fetched data can be further interpreted. 
