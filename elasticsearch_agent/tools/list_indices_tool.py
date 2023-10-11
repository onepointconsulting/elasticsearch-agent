from typing import Type, Optional, List

from pydantic import BaseModel, Field
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun
)

from elasticsearch_agent.config import cfg


class ListIndicesInput(BaseModel):
    """Input for the list indices tool."""

    separator: str = Field(..., description="separator for the list of indices")


class ListIndicesTool(BaseTool):
    """Tool for getting all ElasticSearch indices"""

    name = "elastic_list_indices"
    description = "Input is a delimiter like comma or new line, output is a comma separated list of views in the database. Always use this tool to get to know the indices in the ElasticSearch cluster."

    def _run(
        self,
        separator: str
    ) -> str:
        """Get all indices in the elastic search server ususally separated by a line break"""
        indices: List[str] = cfg.es.cat.indices(h="index", s="index").split()
        return separator.join(
            [index for index in indices if not index.startswith(".")]
        )

    async def _arun(
        self,
        separator: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("ListIndicesTool does not support async")

    args_schema: Optional[Type[BaseModel]] = ListIndicesInput


if __name__ == "__main__":
    from elasticsearch_agent.log_init import logger

    indices_tool = ListIndicesTool()
    logger.info(indices_tool(","))
