from collections import deque

class JsonBuilder:
    """Single purpose JSON file builder for dynamically streaming output data
    
    Attributes:
        out: Output JSON file being built
        stack: Deque for storing order of closing brackets and curly brackets
    """
    def __init__(self, outpath):
        self.out = open(outpath, 'w', newline='')
        self.stack = deque()

    def format_ids(self, set, start, end, count):
        """
        Populates the initial lines of a JSON file to prepare for dynamic
        storage of a list of zbMATH identifiers with given filters.

        Args:
            set: String MSC set code to filter ID's by
            start: String start date of filtering range (format 1970-01-01T00:00:00Z)
            end: String end date of filtering range (format 1970-01-01T00:00:00Z)
            count: String number of records which match the given filters 
        """
        self.out.write('{')
        self.stack.append('}')
        self.out.write(f'"set":"{set}", ')
        self.out.write(f'"start":"{start}", ')
        self.out.write(f'"end":"{end}", ')
        self.out.write(f'"count":{count}, ')
        self.out.write('"identifiers":[')
        self.stack.append(']')

    def add_ID_page(self, id_list):
        """
        Write ID's from a list. Intended for use with page wise list of ID's.
        Appends a comma to the end of the page, so add_ID should be used
        for the final ID in the list.

        Args:
            id_list: List of string ID's
        """
        for id in id_list:
            self.out.write(f"{id},")

    def add_ID(self, id):
        """Write an individual ID to the JSON output list. (No commas)

        Args:
            id: String ID to be added to the JSON list
        """
        self.out.write(id)

    def __enter__(self):
        return self
    
    def __exit__(self, e_type, e_value, e_trace):
        if not self.out.closed:
            self.close()
    
    def close(self):
        """Manually closes the output file"""
        if not self.out.closed:
            # Close any remaining braces
            while len(self.stack) != 0:
                self.out.write(self.stack.pop())
            self.out.close()
