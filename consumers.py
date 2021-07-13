"""
Consumers for writing data to destinations.

Import as:
import consumers
"""

import csv
from typing import List

import base_model

# Template list of fields
OUTPUT_FIELD_LIST = [
    "date",
    "type",
    "amount",
    "from",
    "to"
]


class CSVStatementConsumer(base_model.AbstractStatementConsumer):
    """CSV realization of statement consumer"""

    def __init__(self, file_path: str,
                 fieldnames: List[str],
                 delimiter: str = ','):
        """
        Constructor of the class.

        :param file_path: Path to a CSV-file.
        :param fieldnames: List of field names for a destination.
        :param delimiter: Delimiter for a CSV-file.
        """
        self.writer = csv.DictWriter(open(file_path, 'w'),
                                     fieldnames=fieldnames,
                                     delimiter=delimiter)

    def write_header(self):
        """Header writer for a CSV-file"""
        self.writer.writeheader()

    def write_line(self, line):
        """Line writer for a CSV-file"""
        self.writer.writerow(line)
