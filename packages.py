class Packages:
    """Store imported CSV package data in hash table"""

    # Create buckets with empty list and default initial capacity of 10
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Fetch collection of all packages in hash table
    def all(self):
        # Reduce 2D array into sorted list of values
        return [item[1] for item in sorted(sum(self.table, []))]

    # Fetch a specific package in the hash table
    def find(self, key):
        # Locate the bucket list
        bucket_list = hash(key) % len(self.table)
        package_list = self.table[bucket_list]

        # Find key in bucket list
        for item in package_list:
            if item[0] == key:
                return item[1]

        # If no item is found, return None
        return None

    # Add a package to the chained hash table
    # Function behaves as an "upsert" action, performing both
    # an insert action and an update action.
    def insert(self, key, item):  # does both insert and update
        # Locate the bucket list
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # If package is already present, update it with new value
        for key_value_pair in bucket_list:
            if key_value_pair[0] == key:
                key_value_pair[1] = item

                return True

        # If package not already in list, append it to the end of list
        bucket_list.append([key, item])

        return True

    # Remove an item from the hash table
    def remove(self, key):
        # Locate the bucket list
        bucket_list = hash(key) % len(self.table)
        package_list = self.table[bucket_list]

        # Check for presence of element in list and remove if present
        for item in package_list:
            if item[0] == key:
                package_list.remove([item[0], item[1]])
