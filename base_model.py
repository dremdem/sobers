"""
Describes abstract models for producers and consumers

Import as:
import base_model
"""
import abc
import collections


class AbstractStatementProducer:
    """
    Abstract statement producer as base class
    for further implementations like CSV, RestAPI, DB.
    Have to be use as iterator where every iteration is a line of data.
    """

    @abc.abstractmethod
    def __iter__(self):
        """Method for initializing an iterator"""
        pass

    @abc.abstractmethod
    def __next__(self):
        """Method for returning a line from an iterator"""
        pass


class AbstractStatementConsumer(abc.ABC):
    """
    Abstract consumer for put a data to outside destination
    like CSV, RestAPI and so on.
    """

    @abc.abstractmethod
    def write_line(self, line: collections.OrderedDict):
        """Method for writing next piece of data to a destination"""
        pass

    def write_header(self):
        """Stub for method writing a header line to a CSV file"""
        pass

    def finish(self):
        """Stub for method finishing writing to a CSV file"""
