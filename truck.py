import datetime


class Truck:
    """
    The truck object provides capacity specifications and includes identifying nomenclature and containers for route
    locations
    """

    def __init__(self, name, truck_id, departure):
        date = datetime.date.today()
        time = datetime.time(departure[0], departure[1], departure[2])

        self.capacity = 16
        self.departure_time = datetime.datetime.combine(date, time)
        self.name = name
        self.route = []
        self.route_distance = 0.0
        self.speed = 18
        self.stops = []
        self.truck_id = truck_id

    # Time complexity: O(n log n)
    def update_route_eta(self, graph):
        """Assign calculated time of arrival to each node in the truck's route"""

        route_progress = self.departure_time
        # Initial origin node is the "hub location", first node in route list
        self.route[0] = (self.route[0], self.departure_time)
        origin_node = self.route[0]

        # Calculate the delivery time of each location (node) in route
        for i, node in enumerate(self.route):
            # Skip starting node ("hub location")
            if i == 0:
                continue
            # Skip already-updated nodes
            if type(node) == tuple:
                continue

            # Determine if route node has already been updated and assign timestamp
            updated_route_elements = [n for n in self.route if type(n) == tuple]
            updated_nodes = [n[0] for n in updated_route_elements]

            if node in updated_nodes:
                node_eta = [n[1] for n in updated_route_elements if n[0] == node]
                self.route[i] = (self.route[i], node_eta[0])

                continue

            delta_miles = graph.edges[origin_node[0], node]
            delta_minutes = (60/self.speed) * delta_miles
            delta = datetime.timedelta(minutes=delta_minutes)
            route_progress += delta

            # Convert route element to a tuple of node and formatted ETA time
            self.route[i] = (self.route[i], route_progress)

            # Reassign origin to current node for next iteration
            origin_node = self.route[i]


# Time complexity: O(N)
def print_distance_totals(truck_list):
    """Print cumulative sum of distances for all destinations of each truck's assigned route"""

    cumulative_mileage = 0.0

    print("\nTruck distance totals:")
    print("--------------------")

    for truck in truck_list:
        distance = round(truck.route_distance, 1)

        print("Truck", truck.truck_id, "mileage:", distance)

        cumulative_mileage += truck.route_distance

    print("Total distance for all", len(truck_list), "trucks:", round(cumulative_mileage, 1))
