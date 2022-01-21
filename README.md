###Introduction
The application determines efficient route and delivery distributions for a list of packages and corresponding location distance data, loaded from CSV files, for a package delivery service. Packages are sorted and distributed among three delivery trucks with the following restrictions:
- The service has 3 available trucks and 2 available truck drivers.
- Each package will have a unique identifier and the maximum capacity for each truck is 16 packages.
- Maximum truck speed is 18 miles per hour, and it is assumed that trucks have unlimited fuel will not need to stop.
- Each truck’s route must have no collisions with other truck routes and may leave the hub location starting at 8:00 AM.
- Trucks may return to the hub location to load additional packages.
- Packages may include one special note, indicating a contingency (delayed arrival at hub), a truck restriction (must be delivered on a specific truck), or a grouping restriction, meaning that the package must be delivered with certain other package(s).
- In addition, a package note may indicate that the wrong delivery address is listed. For packages with this designation, the delivery address will not be known until 10:20 AM and therefore cannot depart the hub facility until that time.
- If a package includes a delivery deadline time, it must arrive at the destination address prior to the stated time.

###Summary of Primary Algorithm
The primary algorithm used in scheduling package deliveries is Dijkstra’s shortest path algorithm. Given a graph of nodes and a starting node, this algorithm determines the shortest path from the starting node to each node in the graph. While doing so, a pointer is maintained to reference previously visited shortest path nodes.
For further clarification, this solution uses all three of the available delivery trucks:
- The first truck delivers only priority (early deadline) and packages annotated to be grouped. Upon completion, the driver of this truck returns to the hub facility so that they can drive the delayed truck (see “truck three” below).
- Truck number two delivers packages it alone can deliver, based on package notes. In addition, packages that are both delayed and have a priority deadline are loaded onto this truck. It departs the hub facility at 9:05 AM, once delayed priority packages have arrived.
- Finally, the “delayed” truck (truck three) departs the facility no earlier than 10:20AM, as it must await delayed packages and those for which an address is not yet known. No priority packages are loaded onto this truck.
