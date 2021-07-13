"""Runner for the statement pipeline"""

import consumers
import pipelines
import producers

if __name__ == '__main__':
    bank1 = producers.CSVStatementProducer(producers.bank1_transform_line,
                                           "data/bank1.csv")
    bank2 = producers.CSVStatementProducer(producers.bank2_transform_line,
                                           "data/bank2.csv")
    bank3 = producers.CSVStatementProducer(producers.bank3_transform_line,
                                           "data/bank3.csv")
    main_consumer = consumers.CSVStatementConsumer("output1.csv",
                                                   consumers.OUTPUT_FIELD_LIST)
    pipeline = pipelines.StatementPipeline([bank1, bank2, bank3], main_consumer)
    pipeline.run()
