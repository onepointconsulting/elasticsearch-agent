from typing import Type, Optional

from pydantic import BaseModel, Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from elasticsearch_agent.config import cfg
from langchain.tools.base import BaseTool
from elasticsearch_agent.log_init import logger



class IndexDetailsInput(BaseModel):
    """Input for the list index details tool."""

    index_name: str = Field(..., description="The name of the index for which the details are to be retrieved")


class IndexDetailsTool(BaseTool):
    """Tool for getting information about a single ElasticSearch index"""

    name = "elastic_index_show_details"
    description = "Input is an index name, output is a JSON based string with the aliases, mappings containing the field names and settings of an index"

    def _run(
        self,
        index_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get all indices in the elastic search server ususally separated by a line break"""
        try:
            alias = cfg.es.indices.get_alias(index=index_name)
            field_mappings = cfg.es.indices.get_field_mapping(
                index=index_name, fields="*"
            )
            field_settings = cfg.es.indices.get_settings(index=index_name)
            return str(
                {
                    "alias": alias[index_name],
                    "field_mappings": field_mappings[index_name],
                    "settings": field_settings[index_name],
                }
            )
        except:
            logger.exception(f"Could not fetch index information for {index_name}")
            return ""

    async def _arun(
        self,
        index_name: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("IndexDetailsTool does not support async")

    args_schema: Optional[Type[BaseModel]] = IndexDetailsInput

if __name__ == "__main__":
    index_name = "socio_economic_indicators"
    tool = IndexDetailsTool()
    result = tool(index_name)
    logger.info("result: %s", result)
