from router import dijkstra_shortest_path, get_shortest_path
from package import update_package_delivery_details


# Time complexity: O(n^2 log n)
def schedule_trucks(distance_graph, package_hash, start_node, trucks):
    """Schedule loaded trucks for delivery form hub to locations"""

    # Using three trucks with two drivers
    # I. "Truck 1" can only deliver "unrestricted" packages - those which are not specified to go on a a particular
    #     truck and are not delayed. This truck leaves at 8:00 AM.
    # II. "Truck 2" can deliver any package not marked as delayed. This truck also leaves at 8:00 AM.
    # III. "Truck 3" can deliver any package. However, it includes packages with the following contingency factors:
    #     a. Packages delayed on flights, not arriving at hub until 9:05 AM
    #     b. Packages with incorrect addresses, which will not be corrected until 10:30 AM
    #
    # Given the above listed criteria, and the limitation of fewer drivers than trucks available, we schedule departure
    # for the loaded trucks as follows:
    #     1. Truck 1 ("unrestricted" truck) departs the hub promptly at 8:00 AM, and is loaded with early priority
    #        packages.
    #     2. Upon completing all of its deliveries, it returns to the hub so that the driver can assume operation of
    #        Truck 3 and deliver the remaining packages (which includes delayed items).

    for truck in trucks:
        # Assign each node to the truck's route list based on least distance to complete Hamiltonian path for all stops
        # Starting initially from hub node (start node), subsequently reassigning the origin until all destinations have
        # been visited.

        # All routes start from the hub location
        truck.route.insert(0, start_node)
        # Set initial origin for shortest path iteration
        origin = start_node
        # Execute Dijkstra's algorithm for the set of nodes in the truck's schedule
        dijkstra_shortest_path(distance_graph, origin)
        # Clone truck stops list to prevent mutation of original
        scheduled_stops = truck.stops.copy()

        for destination in scheduled_stops:
            if destination in truck.route:
                continue

            # Get shortest paths to each node in list
            path = get_shortest_path(origin, destination, scheduled_stops)
            path_nodes = path["nodes"]
            path_total_distance = path["total_distance"]

            if len(path_nodes) > 0:
                # Add path nodes to truck route
                truck.route = truck.route + path_nodes
                # Increment cumulative truck route distance with total distance of path segment
                truck.route_distance += path_total_distance
                # Reset origin to end node of path segment
                origin = path_nodes[-1]

        # Unrestricted truck (which initially departs at 8:00AM)
        # returns to hub so driver can take delayed truck
        if truck.truck_id == 1:
            # Append hub location to route unless already assigned
            if truck.route[-1] != start_node:
                truck.route.append(start_node)

        # Assign arrival times to locations, generated as 2-tuples, and build total route distance
        truck.update_route_eta(distance_graph)
        # Propagate delivery times for truck packages based on location arrival times
        update_package_delivery_details(package_hash, formatted_delivery_data(truck), truck.truck_id)


# Consolidate and format route data to update package details
# Time complexity: O(n)
def formatted_delivery_data(truck):
    formatted_data = {}

    # Prepare a dictionary of labeled data points to simplify package update
    for location in truck.route:
        location_node = location[0]
        location_time = location[1]

        formatted_data[location_node.label] = {
            "departure_time": truck.departure_time,
            "delivery_time": location_time
        }

    return formatted_data
