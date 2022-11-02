""" Export data from an ArchivesSpace resource record (collection/finding aid)
    to a spreadsheet for use in digitization workflows.

    Spreadsheet is in CSV format and has the fields "Box", "Folder/Item", and "Title",
    with one row per folder/item.

    Currently this script only supports exporting data from a full collection,
    not a specific series or subseries within a collection.

    Requires ArchivesSnake client library: https://github.com/archivesspace-labs/ArchivesSnake
    and .archivessnake.yml config file with valid ArchivesSpace API URL, username and password
"""

import csv
from asnake.client import ASnakeClient


def main():

    client = ASnakeClient()

    # update these variables for the collection you're working on
    repo = 3  # ASpace repository ID
    resource = 388  # ASpace resource ID for collection
    filename = "ms353_digi_tracking.csv"  # filename for output CSV file

    components = client.get(
        f"repositories/{repo}/resources/{resource}/ordered_records").json(
        )["uris"]

    with open(filename, "w", encoding="utf8") as outfile:
        writer = csv.DictWriter(outfile,
                                fieldnames=["Box", "Folder/Item", "Title"])
        writer.writeheader()
        for component in components:
            if component["level"] in ["file", "item"]:
                for row in make_rows(client, component["ref"]):
                    writer.writerow(row)


def make_rows(client, uri):
    """ takes authenticated ASnake client and ASpace resource URI
        yields one dict per folder/item number associated with that resource

        * this may be more than one dict per instance,
          if instance folder/item number is range or multiple
          * for example, the folder number "7-9" will yield three dicts,
            one each for folders 7, 8, & 9
            "7 & 9" will yield two, one each for folders 7 and 9

        dict fields: Box, Folder/Item, Title
        these dicts form the spreadsheet rows
    """
    archival_object = client.get(uri).json()
    for instance in archival_object["instances"]:
        # box number
        box_ref = instance["sub_container"]["top_container"]["ref"]
        box_number = client.get(box_ref).json().get("indicator")
        # indicator_2 values (folder/item number) may be:
        # null, number, ("7"), or range of numbers separated by dash ("7-9"),
        folder_number = instance["sub_container"].get("indicator_2")
        if folder_number:
            # number range
            if "-" in folder_number:
                bounds = [int(i.strip()) for i in folder_number.split("-")]
                for i in range(bounds[0], bounds[1] + 1):
                    yield {
                        "Box": box_number,
                        "Folder/Item": i,
                        "Title": archival_object["title"]
                    }
            # multiple numbers with ampersand
            elif "&" in folder_number:
                numbers = [int(i.strip()) for i in folder_number.split("&")]
                for i in numbers:
                    yield {
                        "Box": box_number,
                        "Folder/Item": i,
                        "Title": archival_object["title"]
                    }
            # single number
            else:
                yield {
                    "Box": box_number,
                    "Folder/Item": folder_number,
                    "Title": archival_object["title"]
                }
        # null folder/item number
        else:
            yield {
                    "Box": box_number,
                    "Folder/Item": None,
                    "Title": archival_object["title"]
                }



if __name__ == '__main__':
    main()
