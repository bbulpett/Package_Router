import sys


class Vertex:
    """Vertex object represents a physical delivery location and is an individual node in the graph"""

    def __init__(self, label):
        self.label = label  # Label of each vertex is the location address string in the format "Address|PostalCode"
        self.distance = sys.maxsize  # Initialize with largest size Python can handle (virtual infinity)
        self.parent = None


class Graph:
    """
    Graph object represents the adjacency list of vertices (delivery locations) imported from CSV data file.
    Instantiated at the start of the application, the single "distance graph" is referenced at every step of package
    delivery route calculation.
    """

    def __init__(self):
        self.vertices = {}  # Dictionary of vertices
        self.edges = {}  # Dictionary of distances between destinations

    def add_vertex(self, vertex):
        self.vertices[vertex] = []

    def add_directed_edge(self, origin, destination, distance=1.0):
        self.edges[(origin, destination)] = distance
        self.vertices[origin].append(destination)

    def add_undirected_edge(self, origin, destination, distance=1.0):
        self.add_directed_edge(origin, destination, distance)
        self.add_directed_edge(destination, origin, distance)
