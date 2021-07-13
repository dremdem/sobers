"""
Pipelines are collecting producers and consumer together.

Import as:
import pipelines
"""
from typing import List

import base_model


class StatementPipeline:
    """Get the data from producers and write it to consumers."""
    def __init__(self,
                 producers: List[base_model.AbstractStatementProducer],
                 consumer: base_model.AbstractStatementConsumer):
        """
        Constructor for a class.

        :param producers: List of producers.
        :param consumer: Consumer of the data.
        """
        self.producers = producers
        self.consumer = consumer

    def run(self):
        """Pipeline for reading and writing data"""
        self.consumer.write_header()
        for producer in self.producers:
            for line in producer:
                self.consumer.write_line(line)
        self.consumer.finish()
