import datetime
import os
import re


class Package:
    """The package object includes package ID and shipping address data and delivery metadata"""

    def __init__(
        self,
        package_id,
        address,
        city,
        state,
        postal_code,
        deadline,
        weight,
        status,
        notes,
        delivery_time=None,
        departure_time=None,
        truck_id=None
    ):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.notes = notes
        self.delivery_time = delivery_time
        self.departure_time = departure_time
        self.truck_id = truck_id

    # Overwrite print(Package) or else it will print the object reference
    def __str__(self):
        """Return a formatted string of package data"""

        return(
            "\33[1m\33[34mID:\33[0m %s\t\33[1m\33[34m\33[1m\33[34m\33[1m\33[34mWeight:\33[0m %s\t\33[1m\33[34m\33["
            "1m\33[34mOn Truck\33[0m %s\t\33[1m\33[34mStatus:\33[0m %s\t\33[1m\33[34mDeparture:\33[0m %s  \33[1m\33["
            "34mDeadline:\33[0m %s  \33[1m\33[34mETA/Delivery Time:\33[0m %s\t\t\33[1m\33[34mNotes:\33[0m %s\t\33["
            "1m\33[34mAddress:\33[0m %s, %s, %s, %s "
            % (
                self.package_id,
                self.weight,
                self.truck_id,
                self.status,
                self.formatted_time(self.departure_time),
                self.deadline.ljust(10),
                self.formatted_time(self.delivery_time),
                self.formatted_notes(),
                self.address,
                self.city,
                self.state,
                self.postal_code
            )
        )

    # Format datetime object to human-readable string (static method)
    @staticmethod
    def formatted_time(timestamp):
        if timestamp is None:
            return "unassigned"
        else:
            return datetime.datetime.strftime(timestamp, "%H:%M %p")

    # Make notes more easily visible on details list
    def formatted_notes(self):
        """Display N/A if package has no notes"""

        if self.notes == "":
            return "\33[0m" + "N/A"
        else:
            return "\33[31m" + self.notes

    # Determine whether package has arrived at hub and ready to ship or delayed
    def is_ready_to_ship(self, truck_departure):
        """Returns boolean value used to evaluate package readiness"""

        time_delay = None
        wrong_address_flag = re.search(r"Wrong address listed", self.notes)
        time_delay_flag = re.search(r"\d{1,2}:\d{2}", self.notes)

        if wrong_address_flag:
            time_delay = datetime.datetime.strptime("10:20", "%H:%M").time()
        elif time_delay_flag:
            time_delay = datetime.datetime.strptime(time_delay_flag.group(), "%H:%M").time()
        elif time_delay is None:
            return True

        # Returns True if truck departure is after hub arrival time
        return truck_departure.time() >= time_delay

    # Combined address and postal code to use for matching with shipping route
    def label_address(self):
        """Returns address and postal code in the format address|postal code"""

        return "%s|%s" % (self.address, self.postal_code)

    # Given a time string ("HH:MM" format), update delivery status of all packages
    def update_delivery_status(self, status_time):
        """Update package status property with delivery progress"""

        # Statuses:
        # "at the hub" -> package is at the hub (not out for delivery yet)
        # "en route" -> truck has departed with package, but not yet delivered
        # "delivered" -> package has been delivered to route destination

        # Convert selected status input to datetime for delta comparison
        status_date = datetime.datetime.today()
        status_time = datetime.datetime.strptime(status_time, "%H:%M")
        status_datetime = datetime.datetime.combine(status_date, status_time.time())

        # Calculate departure datetime delta
        delivered_delta = status_datetime - self.delivery_time

        # Calculate departure time delta
        departed_delta = status_datetime - self.departure_time

        # Calculate status based on time differential
        delivered = delivered_delta / datetime.timedelta(minutes=1) > 0
        en_route = departed_delta / datetime.timedelta(minutes=1) > 0
        at_the_hub = delivered_delta / datetime.timedelta(minutes=1) < 0

        if delivered:
            self.status = 'delivered'
        elif en_route:
            self.status = 'en route'
        elif at_the_hub:
            self.status = 'at the hub'


# Print details of all packages
def print_all_packages(package_hash):
    """Iterate packages to display details with redefined __str__ function"""

    # Windows command to enable ANSI colour output
    os.system("")

    print("Listing all packages")
    print("--------------------")

    for package in package_hash.all():
        print(str(package))


# Print details of package with provided ID
def print_package(package_hash, package_id):
    """Display details of a single package using redefined __str__ function"""

    # Windows command to enable ANSI colour output
    os.system("")

    package = package_hash.find(package_id)

    if package:
        print("Results for package ID", package_id)
        print("--------------------")
        print(str(package))
    else:
        print("No results for package ID", package_id)
        print("--------------------")


# Print details of all packages at a given time
def print_all_packages_with_time(package_hash, selected_time):
    """Display all package details at a given time (HH:MM)"""

    # Windows command to enable ANSI colour output
    os.system("")

    print("Listing all packages as of ", selected_time)
    print("--------------------")

    for package in package_hash.all():
        package.update_delivery_status(selected_time)
        print(str(package))


# Assign delivery times to packages based on truck route ETA
def update_package_delivery_details(package_hash, package_delivery_data, truck_id):
    """Assign package delivery times based on scheduled truck route details"""

    packages = package_hash.all()
    truck_packages = [p for p in packages if p.truck_id == truck_id]

    for package in truck_packages:
        # match package address with node label in delivery data tuple
        package_label_address = package.label_address()
        departure_time = package_delivery_data[package_label_address]["departure_time"]
        delivery_time = package_delivery_data[package_label_address]["delivery_time"]

        # Assign departure and delivery times to package
        package.departure_time = departure_time
        package.delivery_time = delivery_time
