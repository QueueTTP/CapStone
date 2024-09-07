from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment="StarMeter Data Lineage")

# Add nodes (represent key components in your data pipeline)
dot.node("A", "Kafka (Event Source)")
dot.node("B", "Spark Streaming (Data Processing)")
dot.node("C", "MySQL (Database Storage)")
dot.node("D", "Dashboard (Real-time Visualization)")

# Add edges (show data flow between components)
dot.edge("A", "B", label="Real-time event data")
dot.edge("B", "C", label="Processed data insertion")
dot.edge("C", "D", label="Query for visualization")

# Render the graph to a file and display it
dot.render("data_lineage_diagram", format="png")
dot.view()
