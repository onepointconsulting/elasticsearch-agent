from langchain.agents.initialize import initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.prompts.chat import AIMessage, SystemMessage

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
    return initialize_agent(
        tools, cfg.llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=cfg.langchain_verbose
    )


def agent_factory2() -> AgentExecutor:
    from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent

    tags_ = []
    agent = AgentType.OPENAI_FUNCTIONS
    tags_.append(agent.value if isinstance(agent, AgentType) else agent)
    extra_prompt_messages = [
        AIMessage(
            content="I should look at the indices in the ElasticSearch cluster to see what I can query. Then I should query the fields of the most relevant ElasticSearch Indices."
        )
    ]
    agent_obj = OpenAIFunctionsAgent.from_llm_and_tools(
        cfg.llm, tools, extra_prompt_messages=extra_prompt_messages, system_message=SystemMessage(content="You are a helpful AI ElasticSearch Expert Assistant")
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent_obj, tools=tools, tags=tags_, verbose=cfg.langchain_verbose
    )


if __name__ == "__main__":
    agent_executor = agent_factory()
    prompt = agent_executor.agent.prompt
    print(prompt)
    print(type(agent_executor.agent.prompt))
