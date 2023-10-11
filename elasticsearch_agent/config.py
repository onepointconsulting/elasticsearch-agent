import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from elasticsearch import Elasticsearch

load_dotenv()


class Config:
    elastic_server = os.getenv("ELASTIC_SERVER")
    elastic_user = os.getenv("ELASTIC_USER")
    elastic_password = os.getenv("ELASTIC_PASSWORD")
    elastic_verify_certificates = os.getenv("ELASTIC_VERIFY_CERTIFICATES") == "true"

    es = Elasticsearch(
        [elastic_server],
        basic_auth=(elastic_user, elastic_password),
        verify_certs=elastic_verify_certificates,
    )

    elastic_index_data_from = int(os.getenv("ELASTIC_INDEX_DATA_FROM"))
    elastic_index_data_size = int(os.getenv("ELASTIC_INDEX_DATA_SIZE"))
    elastic_index_data_max_size = int(os.getenv("ELASTIC_INDEX_DATA_MAX_SIZE"))

    model = os.getenv("OPENAI_MODEL")
    request_timeout = int(os.getenv("REQUEST_TIMEOUT"))
    has_langchain_cache = os.getenv("LANGCHAIN_CACHE") == "true"
    streaming = os.getenv("CHATGPT_STREAMING") == "true"
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model,
        temperature=0,
        request_timeout=request_timeout,
        cache=has_langchain_cache,
        streaming=streaming,
        verbose=os.getenv("LLM_VERBOSE") == "true"
    )

    langchain_verbose = os.getenv("LANGCHAIN_VERBOSE") == "true"
    aggs_limit = int(os.getenv("AGGS_LIMIT"))

cfg = Config()

if __name__ == "__main__":
    from elasticsearch_agent.log_init import logger

    check_fields = [
        cfg.elastic_server,
        cfg.elastic_user,
        cfg.elastic_password,
        cfg.elastic_verify_certificates,
        cfg.elastic_index_data_from,
        cfg.elastic_index_data_size
    ]
    for field in check_fields:
        assert field is not None
        logger.info(field)
