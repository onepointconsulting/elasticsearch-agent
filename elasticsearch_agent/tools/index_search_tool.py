import json

from pydantic.v1 import BaseModel, Field  # <-- Uses v1 namespace

from elasticsearch_playground.log_init import logger
from elasticsearch_playground.config import cfg

from langchain.tools import StructuredTool


class SearchToolInput(BaseModel):
    """Input for the index show data tool."""

    index_name: str = Field(
        ..., description="The name of the index for which the data is to be retrieved"
    )
    query: str = Field(..., description="The ElasticSearch JSON query used to filter all hits")
    from_: int = Field(
        ..., description="The record index from which the query will start"
    )
    size: int = Field(
        ...,
        description="How many records will be retrieved from the ElasticSearch query",
    )


def elastic_search(
    index_name: str,
    query: str,
    from_: int = cfg.elastic_index_data_from,
    size: int = cfg.elastic_index_data_size,
):
    """Executes a specific query on an index in ElasticSearch and returns all hits"""
    try:
        query_dict: dict = json.loads(query)
        if "query" in query_dict:
            query_dict = query_dict["query"]
        logger.info(query)
        res = cfg.es.search(
            index=index_name,
            from_=from_,
            size=size,
            query=query_dict,
        )
        return str(res['hits'])
    except Exception as e:        
        logger.exception("Could not execute query")
        msg = str(e)
        return msg


def create_search_tool():
    return StructuredTool.from_function(elastic_search, name="elastic_index_search_tool", args_schema=SearchToolInput)


if __name__ == "__main__":
    index_name = "socio_economic_indicators"
    tool = create_search_tool()
    res = tool.run(
        {
            "index_name": index_name,
            "query": """{"term": {"region": "SA"}}""",
            "from_": 0,
            "size": 10,
        }
    )
    logger.info(res)
