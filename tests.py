import consumers
import pipelines
import producers


def test_pipeline():
    """
    Checking that amount of lines from all CSV-files equials
    amount of lines in the destination file.
    """
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

    bank1_len = len(open("data/bank1.csv").readlines()) - 1
    bank2_len = len(open("data/bank2.csv").readlines()) - 1
    bank3_len = len(open("data/bank3.csv").readlines()) - 1
    output_len = len(open("output1.csv").readlines()) - 1

    assert output_len == bank1_len + bank2_len + bank3_len
