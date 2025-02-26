# Test for Applicats for Development Position Backend/CAD

## Basic Information

This repository provides data for the graph of a workpiece (containing nodes and edges) as well as the graph of a specific feature.
Hint: Look at overview workpiece.png for better understanding.

Nodes describe the surfaces of the workpiece using different types like cylinder, conde or plane.

Edges describe the connection between the surfaces. The edges contain information like the angular_type (e.g. convex, concave) to describe how the surfaces are connected.

## Objectives

### 1. Create an own repository using the content of this repository


### 2. Read the graph data from the json-files and create graph objects in python

- 	You are free to use any library you want. In case you don't know any networkx helps you to create a graph object.


### 3. Check if the feature graph is a subgraph of the workpiece workpiece and find any other matching subgraphs 

-   Check if the given feature graph is actually a subgraph of the workpiece graph.
-	Search for all possible matching subgraphs, that are simmilar to the given feature graph.
-	Hint: To get simmilar subgraphs it's not all attributes of a node have to match.


### 4. Return the results

-   Print the results
-   Commit your changes to your repository
-	Send us the link to your repository with the results