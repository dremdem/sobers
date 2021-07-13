"""
Describes abstract models for the fields and banks(files)

Import as:
import base_model
"""
import abc
import collections
import csv
import datetime as dt
from typing import List

OUTPUT_FIELD_LIST = [
    "date",
    "type",
    "amount",
    "from",
    "to"
]


def bank1_transform_line(values: dict) -> collections.OrderedDict:
    return collections.OrderedDict([
        ("date", dt.datetime.strptime(values["timestamp"], "%b %d %Y")),
        ("type", values["type"]),
        ("amount", float(values["amount"])),
        ("from", int(values["from"])),
        ("to", int(values["to"]))
    ])


def bank2_transform_line(values: dict) -> collections.OrderedDict:
    return collections.OrderedDict([
        ("date", dt.datetime.strptime(values["date"], "%d-%m-%Y")),
        ("type", values["transaction"]),
        ("amount", float(values["amounts"])),
        ("from", int(values["from"])),
        ("to", int(values["to"]))
    ])


def bank3_transform_line(values: dict) -> collections.OrderedDict:
    return collections.OrderedDict([
        (
            "date",
            dt.datetime.strptime(values["date_readable"], "%d %b %Y")),
        ("type", values["type"]),
        ("amount", float(values["euro"]) + (float(values['cents']) / 10)),
        ("from", int(values["from"])),
        ("to", int(values["to"]))
    ])


class AbstractStatementProducer:
    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass


class CSVStatementProducer(AbstractStatementProducer):
    def __init__(self,
                 transform_func,
                 file_path: str,
                 delimiter: str = ',',
                 ):
        self.file_path = file_path
        self.delimiter = delimiter
        self.transform_func = transform_func

    def __iter__(self):
        csvfile = open(self.file_path)
        self.reader = csv.DictReader(csvfile, delimiter=self.delimiter)
        return self

    def __next__(self):
        return self.transform_func(next(self.reader))


class AbstractStatementConsumer(abc.ABC):

    @abc.abstractmethod
    def write_line(self, line: collections.OrderedDict):
        pass

    def write_header(self):
        pass


class CSVStatementConsumer(AbstractStatementConsumer):

    def __init__(self, file_path: str,
                 fieldnames: List[str],
                 delimiter: str = ','):
        self.writer = csv.DictWriter(open(file_path, 'w'),
                                     fieldnames=fieldnames,
                                     delimiter=delimiter)

    def write_header(self):
        self.writer.writeheader()

    def write_line(self, line):
        self.writer.writerow(line)


class StatementPipeline:
    def __init__(self,
                 producers: List[AbstractStatementProducer],
                 consumer: AbstractStatementConsumer):
        self.producers = producers
        self.consumer = consumer

    def run(self):
        self.consumer.write_header()
        for producer in self.producers:
            for line in producer:
                self.consumer.write_line(line)


if __name__ == '__main__':

    bank1 = CSVStatementProducer(bank1_transform_line,
                                 "data/bank1.csv")
    bank2 = CSVStatementProducer(bank2_transform_line,
                                 "data/bank2.csv")
    bank3 = CSVStatementProducer(bank3_transform_line,
                                 "data/bank3.csv")
    main_consumer = CSVStatementConsumer("output1.csv", OUTPUT_FIELD_LIST)
    pipeline = StatementPipeline([bank1, bank2, bank3], main_consumer)
    pipeline.run()
