"""
Describes abstract models for the fields and banks(files)

Import as:
import base_model
"""
import abc
import collections
import csv
from typing import Any, Dict, List


class AbstractField:
    """Define an abstract class for a field"""

    def __init__(self, field_name: str, field_type: Any):
        self.field_name = field_name
        self.field_type = field_type

    def validate(self, value: Any) -> bool:
        try:
            self.field_type(value)
            return True
        except Exception:
            return False


class AbstractSchema:

    def __init__(self, schema_name: str, fields: Dict[str, AbstractField]):
        self.schema_name = schema_name
        self.fields = fields

    def validate(self, values: dict) -> bool:
        return all([field.validate(values[name])
                    for name, field in self.fields.items()])

    @abc.abstractmethod
    def output(self, values: dict) -> collections.OrderedDict:
        pass


class Bank1Schema(AbstractSchema):

    def output(self, values):
        return collections.OrderedDict([
            ("name", )
        ])


class AbstractStatementConsumer:
    def __init__(self, consumer_name: str, schema: AbstractSchema):
        self.consumer_name = consumer_name
        self.schema = schema

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass


class CSVStatementConsumer(AbstractStatementConsumer):

    def __init__(self, file_path: str,
                 delimiter: str = ',',
                 *args, **kwargs):
        self.file_path = file_path
        self.delimiter = delimiter
        super().__init__(*args, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            for line in reader:
                self.schema.validate(line)
                return line
        raise StopIteration


class AbstractStatementProducer:
    def __init__(self, producer_name: str):
        self.producer_name = producer_name


class StatementPipeline:
    def __init__(self,
                 consumers: List[AbstractStatementConsumer],
                 producers: List[AbstractStatementProducer]):
        self.consumers = consumers
        self.producers = producers

    def run(self):
        for consumer in self.consumers:
            for line in consumer:
                pass
