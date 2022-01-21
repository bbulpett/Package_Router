# Barnabas Bulpett
# Package Routing Program"

import re
from packages import Packages
from graph import Graph
from package import print_all_packages, print_package, print_all_packages_with_time
from importer import load_package_data, load_distance_data
from dispatcher import load_trucks
from scheduler import schedule_trucks
from truck import print_distance_totals


class Main:
    """The main class executed when the program first runs"""
    package_hash = Packages()  # Create Chaining Hash table instance
    distance_graph = Graph()  # Create new undirected graph

    # Load packages from CSV into hash table
    load_package_data('Package-File.csv', package_hash)
    # Load distances from CSV into graph
    load_distance_data('Distance-Table.csv', distance_graph)

    # Determine starting node location ("hub location")
    vertices_list = list(distance_graph.vertices.keys())
    start_node = vertices_list[0]

    # Sort packages onto appropriate trucks
    truck_list = load_trucks(vertices_list, package_hash)

    # Schedule deliveries
    schedule_trucks(distance_graph, package_hash, start_node, truck_list)

    # Display user interface menu
    print("\Package Routing Program")
    print("--------------------")

    entry = True

    while entry:
        print("\nMenu:")
        print("""
            1 = Search by package ID
            2 = Show all packages
            3 = All packages at a given time
            4 = Total truck distances
            5 = End Program
            """)
        entry = input("Enter selection: ")

        if entry == "1":
            package_id = None
            while package_id is None:
                input_value = input("Enter package ID... ")

                try:
                    # Validate that the ID value entered is a positive integer
                    if int(input_value) <= 0:
                        print("Package ID must a positive integer")
                    else:
                        package_id = int(input_value)
                except ValueError:
                    print("Package ID must be a positive integer")

            print_package(package_hash, package_id)
            entry = "0"
        elif entry == "2":
            # Print all package data along with cumulative truck mileage
            print_all_packages(package_hash)
            print_distance_totals(truck_list)
        elif entry == "3":
            # Use a regular expression to match time format HH:MM
            # Ex:
            regexp = '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
            time_input = None
            while time_input is None:
                input_value = input("Enter time in 24-hour format HH:MM... ")

                if not re.match(regexp, input_value):
                    print("Time input must be in the format HH:MM")
                else:
                    time_input = input_value

            print_all_packages_with_time(package_hash, time_input)
            entry = "0"
        elif entry == '4':
            print_distance_totals(truck_list)
            entry = "0"
        elif entry == "5":
            print("\nGoodbye")
            entry = None
        elif entry != "":
            print("\nPlease enter a valid selection")
