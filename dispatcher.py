from truck import Truck
import datetime
import re


# Load sorted packages onto appropriate trucks
# Time complexity: O(n^2)
def load_trucks(vertices_list, package_hash):
    """Determine packages to load onto individual trucks"""
    # Instantiate delivery trucks:
    # Truck 1: Unrestricted packages only. Excludes packages only deliverable on truck 2
    # Truck 1 departs at 8:00 AM
    unrestricted_truck = Truck("Unrestricted", 1, (8, 0, 0))

    # Truck 2: Can include any package, including restricted packages
    # and is loaded to maximum capacity (16 packages).
    # Truck 2 departs at 9:05 AM
    restricted_truck = Truck("Restricted", 2, (9, 5, 0))

    # Truck 3: leaves hub later (wrong address or delayed flight). Cannot include restricted
    # packages and is loaded to maximum capacity (16 packages)
    # Truck 3 departs at 10:30 AM
    delayed_truck = Truck("Delayed", 3, (10, 30, 0))

    # Sort packages based on contingencies/restrictions
    all_packages = package_hash.all().copy()
    sorted_packages = sort_packages(all_packages)

    """Load unrestricted truck"""
    # List of unrestricted truck packages includes priority (not EOD) packages
    # and packages that are noted to be grouped with others
    unrestricted_truck_packages = []
    ordered_grouped_packages = order_by_deadline(sorted_packages["grouped_packages"])

    for package in ordered_grouped_packages[:]:
        unrestricted_truck_packages.append(package)

    for package in sorted_packages["priority_packages"][:]:
        if(
            package.is_ready_to_ship(unrestricted_truck.departure_time) and
            len(unrestricted_truck_packages) < 12
        ):
            unrestricted_truck_packages.append(package)
            sorted_packages["priority_packages"].remove(package)

    ordered_unrestricted_packages = order_by_deadline(unrestricted_truck_packages)

    load_truck(unrestricted_truck, ordered_unrestricted_packages, vertices_list)

    """Load delayed truck"""
    # List of delayed truck packages starts with delayed packages if available at departure time,
    # followed by non-priority unrestricted packages until truck capacity is reached
    delayed_truck_packages = []

    for package in sorted_packages["delayed_packages"][:]:
        if package.is_ready_to_ship(delayed_truck.departure_time) and package.deadline == 'EOD':
            delayed_truck_packages.append(package)
            sorted_packages["delayed_packages"].remove(package)

    for package in sorted_packages["unrestricted_packages"][:]:
        if len(delayed_truck_packages) < delayed_truck.capacity:
            delayed_truck_packages.append(package)
            sorted_packages["unrestricted_packages"].remove(package)
        else:
            break

    load_truck(delayed_truck, delayed_truck_packages, vertices_list)

    """Load restricted truck"""
    # List of restricted truck packages starts with delayed packages if available at departure time,
    # followed by all restricted packages,
    # followed by non-priority unrestricted packages until truck capacity is reached
    restricted_truck_packages = []

    for package in sorted_packages["priority_packages"][:]:
        if package.is_ready_to_ship(restricted_truck.departure_time):
            restricted_truck_packages.append(package)
            sorted_packages["priority_packages"].remove(package)

    while(
        len(restricted_truck_packages) < restricted_truck.capacity and
        len(sorted_packages["delayed_packages"]) > 0
    ):
        for package in sorted_packages["delayed_packages"][:]:
            if package.is_ready_to_ship(restricted_truck.departure_time):
                restricted_truck_packages.append(package)
                sorted_packages["delayed_packages"].remove(package)

    while(
        len(restricted_truck_packages) < restricted_truck.capacity and
        len(sorted_packages["restricted_packages"]) > 0
    ):
        for package in sorted_packages["restricted_packages"][:]:
            restricted_truck_packages.append(package)
            sorted_packages["restricted_packages"].remove(package)

    for package in sorted_packages["unrestricted_packages"][:]:
        restricted_truck_packages.append(package)

    ordered_restricted_packages = order_by_deadline(restricted_truck_packages)

    load_truck(restricted_truck, ordered_restricted_packages, vertices_list)

    return [unrestricted_truck, restricted_truck, delayed_truck]


# Load designated list of packages onto each truck
# Time complexity: O(n^2)
def load_truck(truck, packages, vertices_list):
    loaded_status = "* at the hub"

    # Load packages onto each truck until reaching their capacity
    for package in packages:
        if package.status != loaded_status:
            package_address = "%s|%s" % (package.address, package.postal_code)
            address_match = [v for v in vertices_list if v.label == package_address]

            # Do not duplicate truck stop entries
            if address_match[0] not in truck.stops:
                truck.stops.append(address_match[0])

            package.truck_id = truck.truck_id
            package.status = loaded_status


# Returns a dictionary of categorized packages
# Time complexity: O(n^2), because grouped_packages() function O(n^2) is invoked
def sort_packages(packages):
    restriction_flag = "Can only be on truck 2"
    contingency_flags = [
        "Delayed on flight---will not arrive to depot until 9:05 am",
        "Wrong address listed"
    ]

    delayed_packages = []
    priority_packages = []
    restricted_packages = []
    unrestricted_packages = []

    # Retrieve any packages to be grouped with the specific package
    grouped_packages_list = grouped_packages(packages)

    # Remove any grouped packages so that they will not be iterated with others
    for package in grouped_packages_list:
        packages.remove(package)

    for package in packages:
        # Filter package lists for restricted and delayed packages
        if package.notes == restriction_flag:
            restricted_packages.append(package)
            continue
        elif package.notes in contingency_flags:
            delayed_packages.append(package)
            continue
        elif package.deadline != "EOD":
            priority_packages.append(package)
            continue
        else:
            unrestricted_packages.append(package)

    # Evaluate unrestricted package addresses to determine if any can be grouped for efficiency.
    grouped_addresses = ["%s|%s" % (p.address, p.postal_code) for p in grouped_packages_list]
    priority_addresses = ["%s|%s" % (p.address, p.postal_code) for p in priority_packages]
    restricted_addresses = ["%s|%s" % (p.address, p.postal_code) for p in restricted_packages]

    for package in unrestricted_packages:
        address_string = "%s|%s" % (package.address, package.postal_code)

        if address_string in grouped_addresses:
            grouped_packages_list.append(package)
            unrestricted_packages.remove(package)
            continue
        elif address_string in priority_addresses:
            priority_packages.append(package)
            unrestricted_packages.remove(package)
            continue
        elif address_string in restricted_addresses:
            restricted_packages.append(package)
            unrestricted_packages.remove(package)
            continue

    # Evaluate delayed package addresses to determine if any can be loaded on restricted truck for efficiency.
    for package in delayed_packages:
        address_string = "%s|%s" % (package.address, package.postal_code)
        date = datetime.date.today()
        time = datetime.time(9, 5, 0)
        restricted_truck_departure = datetime.datetime.combine(date, time)

        if address_string in priority_addresses and package not in restricted_packages:
            if package.is_ready_to_ship(restricted_truck_departure):
                restricted_packages.append(package)
                delayed_packages.remove(package)
                continue

    sorted_packages = {
        "delayed_packages": delayed_packages,
        "grouped_packages": grouped_packages_list,
        "priority_packages": priority_packages,
        "restricted_packages": restricted_packages,
        "unrestricted_packages": unrestricted_packages
    }

    # Return a dictionary of sorted packages
    return sorted_packages


# Return a list of packages that must be loaded with a particular package
# Time complexity: O(n^2)
def grouped_packages(packages_list):
    """
    Find packages to group with given package, based on annotated constraint
    or matching physical address
    """
    # List of package ID integers for packages to be grouped with package
    companion_ids = []
    companion_addresses = []
    delivery_constraint_pattern = "Must be delivered with"

    # Collect ID of all packages either marked to be grouped with others or
    # marked by others to be grouped with them.
    for package in packages_list:
        address_string = "%s|%s" % (package.address, package.postal_code)
        # If package is annotated to be grouped or if its address is present in the companions list,
        # add its ID to the list along with items to be grouped.
        if re.match(delivery_constraint_pattern, package.notes) or address_string in companion_addresses:
            companion_ids.append(package.package_id)
            companion_addresses.append(address_string)
            id_strings = re.findall(r'\d+', package.notes)
            companion_ids += list(map(int, id_strings))

    # Deduped set of companion IDs
    companion_set = set(companion_ids)
    # Prepare list of packages to be grouped
    companions = [p for p in packages_list if p.package_id in companion_set]

    # return subset of packages to group with package
    return companions


# Time Complexity: O(n)
def order_by_deadline(packages):
    # Extract "EOD" packages to be added to the sorted priority (timed deadline) list
    eod_packages = [p for p in packages if p.deadline == 'EOD']
    priority_packages = [p for p in packages if p.deadline != 'EOD']
    priority_sorted = sorted(priority_packages, key=lambda p: datetime.datetime.strptime(p.deadline, '%H:%M %p'))

    return priority_sorted + eod_packages
