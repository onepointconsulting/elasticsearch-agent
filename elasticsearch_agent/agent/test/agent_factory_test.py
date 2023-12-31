from elasticsearch_agent.agent.agent_factory import agent_factory
from elasticsearch_agent.log_init import logger

agent_executor = agent_factory()


def test_list_indices():
    execution_template("Can you please list all indices?")


def test_list_count():
    execution_template(
        "How many records are there in the co2 production index?"
    )


def test_list_counts():
    execution_template(
        "Can you please list all indices with its corresponding record count?"
    )


def test_fields():
    execution_template("Which are the fields of the gross national income index?")


def test_query_austria():
    execution_template(
        "Which is the CO2 production value for Austria in 2019 and 2020?"
    )


def test_query_germany():
    execution_template(
        "Which is the CO2 production value for Germany from 2018 to 2020?"
    )


def test_query_germany_vs_autria():
    execution_template(
        "Can you compare the CO2 production of Austria and Germany from 2015 to 2020?"
    )


def test_query_germany_vs_autria_vs_india():
    execution_template(
        "Can you compare the CO2 production of Austria and Germany and India from 2015 to 2020 in terms of trends?"
    )


def test_query_average_european_countries():
    execution_template(
        "Can you give me the average of CO2 production for all European countries based on the co2 production index for the year of 2019?"
    )


def test_list_regions():
    execution_template("Can you list all regions in the co2 production index?")


def test_list_all_european_countries():
    execution_template(
        "Can you list all European countries in the in the co2 production index?"
    )


def test_list_all_european_countries_specific():
    execution_template(
        "Can you list all countries in the ECA region in the co2 production index?"
    )


def test_CO2_for_regions():
    execution_template("Can you list the CO2 emissions for 2020 for all regions?")


def test_gni_for_Germany():
    execution_template("Can you tell me the gross national income of Germany in 2015 and 2016?")


def test_regionswith_gni():
    execution_template("Which are the regions mentioned for which you have gross national income per capita data?")

def test_highest_co2():
    execution_template("Which is the country with the highest Co2 production in 2021?")

import sys

report_file = None

if len(sys.argv) > 1:
    report_file = sys.argv[1] if sys.argv[1] != '.' else None 


def execution_template(question: str) -> str:
    res = agent_executor.run(f"""
Make sure that you query first the indices in the ElasticSearch database.
Make sure that after querying the indices you query the field names.

                             
Then answer this question:
{question}
""")
    logger.info(question)
    logger.info(res)
    if report_file is not None:
        with open(report_file, "a") as f:
            f.write(
                f"""
{question}
{res}

"""
            )
    return res


if __name__ == "__main__":
    # To test and pipe the result into a file, use:
    # python.exe .\elasticsearch_agent\agent\test\agent_factory_test.py test_output.txt
    test_list_indices()
    test_list_count()
    test_list_counts()
    test_fields()
    test_query_austria()
    test_query_germany()
    test_query_germany_vs_autria()
    test_query_germany_vs_autria_vs_india()
    test_query_average_european_countries()
    test_list_regions()
    test_list_all_european_countries()
    test_list_all_european_countries_specific()
    test_CO2_for_regions()
    test_gni_for_Germany()
    test_regionswith_gni()
    test_highest_co2()
