from elasticsearch_agent.agent.agent_factory import agent_factory2
from elasticsearch_agent.log_init import logger

agent_executor = agent_factory2()


def test_list_indices():
    res = agent_executor.run("Can you please list all indices?")
    logger.info("Indices: ")
    logger.info(res)


def test_list_count():
    res = agent_executor.run(
        "How many records are there in the socio_economic_indicators index?"
    )
    logger.info("Record count: ")
    logger.info(res)


def test_list_counts():
    res = agent_executor.run(
        "Can you please list all indices with its corresponding record count?"
    )
    logger.info("Record count in all indices: ")
    logger.info(res)


def test_fields():
    res = agent_executor.run(
        "Which are the fields of the socio_economic_indicators index?"
    )
    logger.info("Fields of socio_economic_indicators index:")
    logger.info(res)


def test_query_austria():
    res = agent_executor.run(
        "Which is the CO2 production value for Austria in 2019 and 2020?"
    )
    logger.info("Fields of socio_economic_indicators index:")
    logger.info(res)


def test_query_germany():
    res = agent_executor.run(
        "Which is the CO2 production value for Germany from 2018 to 2020?"
    )
    logger.info("Fields of socio_economic_indicators index:")
    logger.info(res)


def test_query_germany_vs_autria():
    execution_template(
        "Can you compare the CO2 production of Austria and Germany from 2015 to 2020?"
    )


def test_query_germany_vs_autria_vs_india():
    execution_template("Can you compare the CO2 production of Austria and Germany and India from 2015 to 2020 in terms of trends?")


def execution_template(question: str):
    res = agent_executor.run(question)
    logger.info(question)
    logger.info(res)


if __name__ == "__main__":
    test_query_germany_vs_autria()
    # test_fields()
