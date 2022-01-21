# Time complexity: O(n^2)
def dijkstra_shortest_path(graph, start_node):
    """Run Dijkstra's Algorithm to determine the shortest path from each node in graph to all other nodes"""

    # Container to hold unvisited nodes while iterating
    unvisited_nodes = []

    # Execute until all nodes in graph are visited
    for current_node in graph.vertices:
        unvisited_nodes.append(current_node)

        start_node.distance = 0

        # Continue for each unvisited node until depleted
        while unvisited_nodes:
            min_index = 0

            # Evaluate each unvisited node to find that which has the minimum distance
            for i, node in enumerate(unvisited_nodes):
                if node.distance < unvisited_nodes[min_index].distance:
                    min_index = i

            # Set current node to that which has the minimum distance
            current_node = unvisited_nodes.pop(min_index)

            # Calculate distance of current node to neighboring nodes
            for neighboring_node in graph.vertices[current_node]:
                distance = graph.edges[(current_node, neighboring_node)]
                distance_to_current = current_node.distance + distance

                # Evaluate suitability of neighboring node to become new current node
                if distance_to_current < neighboring_node.distance:
                    neighboring_node.distance = distance_to_current
                    neighboring_node.parent = current_node


# Time complexity: O(n)
def get_shortest_path(origin, destination, truck_stops):
    # Collect path segment nodes in a list
    path_nodes = []

    # Start at destination node and work backwards to origin
    current_vertex = destination

    # Conditions to ensure presence of vertex and to prevent assignment
    # of parent nodes not included in itinerary (truck stops)
    while current_vertex is not None and current_vertex is not origin and current_vertex in truck_stops:
        path_nodes.append(current_vertex)
        current_vertex = current_vertex.parent

    return {"nodes": path_nodes, "total_distance": destination.distance}
