"""
Producer classes for gathering information from sources.

Import as:
import producers
"""

import csv
import collections
import datetime as dt

import base_model


def bank1_transform_line(values: dict) -> collections.OrderedDict:
    """
    Transform data from the line to destination bank1 format.

    :param values: Dictionary with values where keys are field names.
    :return: Result of transformation.
    """
    return collections.OrderedDict([
        ("date", dt.datetime.strptime(values["timestamp"], "%b %d %Y")),
        ("type", values["type"]),
        ("amount", float(values["amount"])),
        ("from", int(values["from"])),
        ("to", int(values["to"]))
    ])


def bank2_transform_line(values: dict) -> collections.OrderedDict:
    """
    Transform data from the line to destination bank2 format.

    :param values: Dictionary with values where keys are field names.
    :return: Result of transformation.
    """
    return collections.OrderedDict([
        ("date", dt.datetime.strptime(values["date"], "%d-%m-%Y")),
        ("type", values["transaction"]),
        ("amount", float(values["amounts"])),
        ("from", int(values["from"])),
        ("to", int(values["to"]))
    ])


def bank3_transform_line(values: dict) -> collections.OrderedDict:
    """
    Transform data from the line to destination bank3 format.

    :param values: Dictionary with values where keys are field names.
    :return: Result of transformation.
    """
    return collections.OrderedDict([
        ("date",
         dt.datetime.strptime(values["date_readable"], "%d %b %Y")),
        ("type", values["type"]),
        ("amount", float(values["euro"]) + (float(values['cents']) / 10)),
        ("from", int(values["from"])),
        ("to", int(values["to"]))
    ])


class CSVStatementProducer(base_model.AbstractStatementProducer):
    """CSV realization of the statement producer"""

    def __init__(self,
                 transform_func,
                 file_path: str,
                 delimiter: str = ',',
                 ):
        """
        Constructor for a class.

        :param transform_func: Link to a function for a data transformation.
        :param file_path: Path to a source CSV file.
        :param delimiter: Delimiter symbol for a CSV file.
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.transform_func = transform_func

    def __iter__(self):
        """CSV iterator initialization"""
        csvfile = open(self.file_path)
        self.reader = csv.DictReader(csvfile, delimiter=self.delimiter)
        return self

    def __next__(self):
        """Get next line from CSV-file and transform to a needed format"""
        return self.transform_func(next(self.reader))
