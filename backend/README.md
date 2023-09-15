## LLM Support Bot

The general flow for this LLM Support bot is as follows:

### Initialize the vector index

- Fetch data from Github's GraphQL API for Issues and Disccussions and
  save as a JSON
- Parse the JSON files to create Documents and Nodes
- Write documents to a VectorDB such as Pinecone or Chroma

### Answer Questions

- The question.py script has a function that takes a question and returns
  an answer. It uses a custom prompt and generates additional context to the prompt.
- `main.py` contains a simple `/ask` endpoint which takes a `question` in the
  request body and returns an answer.

