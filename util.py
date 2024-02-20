"""
* Author = virus
* Version = 1.1.0

* Organizations unique identifier
"""

import json


class Vendom:
    def __init__(self, database:str= "organizations.json"):
        self.database = database
        self.data = {}

        self.load(database)

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
            raise FileNotFoundError("Couldn't find the OUI database.")

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
        self.database = new_file
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

    def get_oui(self, mac:str, sep:str=":"):
        """

        :param mac: mac address parser
        :return:
        """

        if mac.count(sep) == 5:
            portions = mac.split(sep)
            oui = portions[:3]

            return "".join(oui).lower()
        return mac

    def get(self, *id:str, sep:str=":") -> dict|str:
        """

        :param id: ids of queried organizations
        ```
        vendom = Vendom()
        vendom.get("000000", "01:00:00:00:00:00", ...)

        >> {"xxxxxx": "<org>", ...}
        ```
        :return:
        """

        vendor = "<unknown>"
        ouis = {}
        for oui in id:
            vendor = self.data.get(oui, vendor)

            ouis[oui] = vendor

        return ouis if len(id) > 1 else vendor