# Creating a Knowledge Graph with Analysing Code Files from any Github Repository
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

![knowledge_graph](https://github.com/Atakan305/Knowledge-Graph/assets/76012121/699e38ff-bcef-4248-b03b-cb010347f641)

This knowledge graph is created with running the main.py file. By running the same file, the graphic can be displayed in a larger area, the quality of its appearance can be increased, and it can be customized according to personal needs.

```
python main.py
```
for customizing the relationships between code files you can change this block in main.py file:
```
def extract_relationships(code, language):
    relationships = []
    if language == "python":
        # Extract object creation, variable assignments, class definitions, module imports, dataflow, database connections, and API calls
        object_creations = re.findall(r'(\w+)\s*=\s*(\w+)\(.+\)', code)
        variable_assignments = re.findall(r'(\w+)\s*=\s*.+', code)
        class_definitions = re.findall(r'classdef\s+(\w+)', code)
        module_imports = re.findall(r'py.importlib.import_module\(\"(\w+)\"\)', code)  # Assuming this pattern for Python module imports
        dataflow = re.findall(r'(\w+)\s*=\s*(\w+)\(.+\)', code)  # Extract source and target from dataflow
        database_connections = re.findall(r'\w+\(.+\)', code)  # Assuming this pattern for database connections
        api_calls = re.findall(r'(\w+)\(.+\)', code)  # Extract only function names as API calls
        # Add a custom "type" based on your criteria, for example, function names
        relationships.extend((source, target, "function") for source, target in object_creations)
        relationships.extend((source, target, "variable") for source in variable_assignments)
        relationships.extend((source, target, "class") for source, target in class_definitions)
        relationships.extend((source, target, "module") for source in module_imports)
        relationships.extend((source, target, "function") for source, target in dataflow)
        relationships.extend((source, target, "database") for source in database_connections)
        relationships.extend((source, function_name, "api") for function_name in api_calls)
    elif language == "matlab":
        # Extract relationships from MATLAB code (customize for your specific MATLAB code structure)
        class_definitions = re.findall(r'classdef\s+(\w+)', code)
        function_modules = re.findall(r'function\s+(\w+)', code)
        relationships.extend((source, target, "class") for source in class_definitions for target in function_modules)
    return relationships
```


In addition, for a further step, this project may also added to Neo4j server and it's possible to analyze the created knowledge graph. On this knowledge graph, queries can be written in the Neo4j DBMS and eventually the fetched data can be further interpreted. 
you can run the file and connect to the Neo4j browser with this command:
```
python src/neo4j_kg_upload.py
```
and you can customize the queries according to your files and relationships via changing this code block:
```
    def import_knowledge_graph(self, tx, graph_file):
        # Open the knowledge graph file and read its content
        with open(graph_file, 'r') as f:
            knowledge_graph_data = f.read()

        lines = knowledge_graph_data.split('\n')

        for line in lines:
            parts = line.split(',')
            if len(parts) == 3:
                source_node, target_node, relationship_type = parts[0], parts[1], parts[2]

                # Customize the import logic to match your knowledge graph data structure
                # For example, create nodes and relationships in Neo4j based on the parsed data
                # You may need to use Cypher queries for this task
                # For example, create a query with using Cypher. 
                cypher_query = (
                    f"MERGE (source:Node {{name: $source_node}})"
                    f"MERGE (target:Node {{name: $target_node}})"
                    f"MERGE (source)-[:{relationship_type}]->(target)"
                )

                tx.run(cypher_query, source_node=source_node, target_node=target_node)
```

In conclusion, this project aims to extracting relationships from source code files, constructing a knowledge graph, and importing it into a Neo4j database. The resulting knowledge graph can be used for various applications, including code analysis, visualization, and querying. 
