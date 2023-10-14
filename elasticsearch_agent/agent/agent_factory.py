from langchain.agents.initialize import initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.prompts.chat import SystemMessage
from elasticsearch_agent.config import cfg
from elasticsearch_agent.tools.list_indices_tool import ListIndicesTool
from elasticsearch_agent.tools.index_data_tool import IndexShowDataTool
from elasticsearch_agent.tools.index_details_tool import IndexDetailsTool
from elasticsearch_agent.tools.index_search_tool import create_search_tool

tools = [
    ListIndicesTool(),
    IndexShowDataTool(),
    IndexDetailsTool(),
    create_search_tool(),
]

def agent_factory() -> AgentExecutor:
    from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent

    tags_ = []
    agent = AgentType.OPENAI_FUNCTIONS
    tags_.append(agent.value if isinstance(agent, AgentType) else agent)
    agent_obj = OpenAIFunctionsAgent.from_llm_and_tools(
        cfg.llm, tools,
        system_message=SystemMessage(content="You are a helpful AI ElasticSearch Expert Assistant")
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent_obj, tools=tools, tags=tags_, verbose=cfg.langchain_verbose
    )


if __name__ == "__main__":
    agent_executor = agent_factory()
    prompt = agent_executor.agent.prompt
    print(prompt)
    print(type(agent_executor.agent.prompt))
