# Elasticsearch Langchain Agent

This project uses ElasticSearch together with LangChain and ChatGPT 4 to build an agent with which you can ask intelligent questions on
top of an ElasticSearch cluster.

## Setup

We suggest to use [Conda](https://docs.conda.io/en/latest/) to manage the virtual environment and then install poetry.

```
conda activate base
conda remove -n elastic_search_playground --all
conda create -n elastic_search_playground python=3.11
conda activate elastic_search_playground
pip install poetry
``````

## Installation

```
poetry install
```