import csv
from package import Package
from graph import Vertex


def load_package_data(filename, hashtable):
    """Load CSV package data into hashtable"""

    with open(filename) as packages:
        package_data = csv.reader(packages, delimiter=',')

        next(package_data)  # Skip header
        for package_id, package in enumerate(package_data, 1):
            m_package_id = package_id
            m_address = package[1]
            m_city = package[2]
            m_state = package[3]
            m_postal_code = package[4]
            m_deadline = package[5]
            m_weight = package[6]
            m_status = "at the hub"
            m_notes = package[7]

            #  Package object
            package = Package(
                m_package_id,
                m_address,
                m_city,
                m_state,
                m_postal_code,
                m_deadline,
                m_weight,
                m_status,
                m_notes
            )

            # Insert package object into hash table
            hashtable.insert(m_package_id, package)


def load_distance_data(filename, graph):
    """Load CSV distance data into graph"""

    with open(filename) as distances:
        distance_data = csv.reader(distances, delimiter=',')

        next(distance_data)  # Skip header
        for distance in distance_data:
            vertex_address = distance[1] + '|' + distance[2]
            vertex = Vertex(vertex_address)

            graph.add_vertex(vertex)

            for i, neighboring_node in enumerate(graph.vertices.keys()):
                weight = distance[i + 3]
                graph.add_undirected_edge(vertex, neighboring_node, float(weight))
