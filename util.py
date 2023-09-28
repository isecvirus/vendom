"""
* Author = virus
* Version = 1.0.0

* Organizations unique identifier
"""

import json

class DATA(dict):
    def get_name(self):
        return self.get("org", None)

    def get_address(self):
        return self.get("address", None)

class Vendom:
    def __init__(self, file:str="data.json"):
        self.file = file
        self.data = {}

        self.load(file)

    def __len__(self):
        """
        Number of ids in the self.data

        vendom = Vendom()
        count = len(vendom)
        """
        return len(self.data)

    @staticmethod
    def read(file:str) -> dict:
        try:
            with open(file, "r") as o:
                return json.loads(o.read())
        except FileNotFoundError:
            raise FileNotFoundError("The data file isn't exist")

    def load(self, file):
        """
        Load the data file.

        * will be auto called on init a new instance *
        # and when updating the file using update_file:
        ```
        vendom.update_file( ... )
        ```
        """
        self.data = self.read(file)


    def update_file(self, new_file):
        """
        Updates the data file

        :param new_file: existing full data file path
        """
        self.file = new_file
        self.load(new_file) # to load the new data

    def merge_file(self, file):
        """
        Merge two data files in a buffer to read from.

        :param file: json data file
        :return: new merged dict.
        """
        file_data = self.read(file)

        self.data = {**self.data, **{i:file_data[i] for i in sorted(file_data)}}

        return self.data

    def export(self, *id:str, file:str):
        """
        Exports a specified number of ids to a file

        :param id: args of ids
            ```
            vendom = Vendom()
            vendom.export("000000", "000001", ..., "output.json")
            ```
        :param file: the output file
        :return: dict data
            ```
            {id: org: value, address: vlaue, ...}
            ```
        """
        with open(file, "w") as export_file:
            data = self.get(*id)
            export_file.write(json.dumps(data, indent=4))

        return data

    def get_ids(self) -> list:
        """
        Get all data's ids as a list
        ```
        [000000, 000001, ...]
        ```

        :return:
        """
        return sorted(self.data)

    def get_index(self, index:int) -> DATA:
        """

        :param index: the human index of the wanted id
        :return: a data object
        ```
        vendom = Vendom()
        print(vendom.get_index(100))

        >> {"xxxxxx": {"org": "...", "address": "..."}}
        ```
        """

        length = self.__len__()
        index = min(max(1, index - 1), length)

        if index <= (length - 1):
            return DATA(self.data.get(sorted(self.data)[index], None))

    def get(self, *id:str) -> dict:
        """

        :param id: ids of queried organizations
        ```
        vendom = Vendom()
        vendom.get("000000", "000001", ...)

        >> {"xxxxxx": {"org": "...", "address": "..."}, ...}
        ```
        :return:
        """
        return {i: (self.data.get(i, None)) for i in id}

    def search(self, string:str, by:str="org", case_sensitive:bool=False) -> dict:
        """

        :param string: the target string
        :param by: search by "org" or "address"
        :param case_sensitive: make the search sensitive to char case or not
        :return: dict

        ```
        vendom = Vendom()
        print(vendom.search("ieee", case_sensitive=False))

        >> {"xxxxxx": {"org": "...", "address": "..."}}
        ```
        """
        if not by in ["org", "address"]:
            by = "org"

        result = {}
        for id in self.data:
            org_name = self.data[id][by]
            org_name = (str(org_name).lower() if not case_sensitive else org_name)

            string = (str(string).lower() if not case_sensitive else string)

            if string in org_name:
                result[id] = self.data[id]

        return result