from typing import Type, Optional

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)

from pydantic import BaseModel, Field

from langchain.tools.base import BaseTool

from elasticsearch_agent.log_init import logger
from elasticsearch_agent.config import cfg


class IndexShowDataInput(BaseModel):
    """Input for the index show data tool."""

    index_name: str = Field(..., description="The name of the index for which the data is to be retrieved")


class IndexShowDataTool(BaseTool):
    """Tool for getting a list of entries from an ElasticSearch index, helpful to figure out what data is available."""

    name = "elastic_index_show_data"
    description = "Input is an index name, output is a JSON based string with and extract of the data of the index"

    def _run(
        self,
        index_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get all indices in the elastic search server ususally separated by a line break"""
        try:
            res = cfg.es.search(
                index=index_name,
                from_=cfg.elastic_index_data_from,
                size=cfg.elastic_index_data_size,
                query={"match_all": {}},
            )
            return str(res["hits"])
        except:
            logger.exception(f"Could not fetch index data for {index_name}")
            return ""

    args_schema: Optional[Type[BaseModel]] = IndexShowDataInput


if __name__ == "__main__":
    index_name = "socio_economic_indicators"
    res = IndexShowDataTool().run(index_name)
    logger.info(res)
