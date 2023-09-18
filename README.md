## LLM Support Bot

## Overview

The backend contains the Python code for ingesting data from Github
Discussions and Issues, writing that data to a vector database, and
providing an API for responding to questions via an LLM and context
from the database.

The frontend is a simple web interface for asking questions and
getting answers from the API.

## Codespaces

You can use Codespaces/Devcontainers to run this application. Start
the remote dev container. From there, you can run `make dev-api` in a terminal
to start the backend, and then open a new termianl and run `make dev-web` t
to start the front-end.


## Installation

If you choose to do manually installation, create a virutal environment and
install dependencies for both python and node.

```
pyenv virtualenv 3.10 llm-support-bot
pyenv local llm-support-bot
make install
```

## Usage

You will need some API tokens in order to run the bot.

```
# Only required to fetch new issues/disccusions to seed Vector Database
GITHUB_API_TOKEN:  Github API token with read:discussion permission scope

# Required for answering questions by the LLM
OPENAI_API_KEY:

# Name of the model to use, e.g gpt4 or gpt-3.5-16k
OPENAI_MODEL

# API Key to query Pinecone for embeddings
PINECONE_API_KEY
```


Start the backend:

```
make dev-api
```


Start the frontend

```
make dev-web
```
