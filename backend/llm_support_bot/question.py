import datetime
import logging
import os
import sys

import click
from llama_index import ServiceContext, set_global_service_context
from llama_index.prompts import PromptTemplate

from llm_support_bot import storage
from llm_support_bot.types import Event
from llm_support_bot.model import openai_model
from llm_support_bot.db import get_connection, write_event

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
logger = logging.getLogger(__name__)

model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo-16k")


def init_model(model=model):
    logging.info("Initializing model")
    llm = openai_model(model=model)
    embed_model = storage.get_embedding_model()
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    set_global_service_context(service_context)
    index = storage.load_index()

    template = (
        "We have provided Github Issues and Discussions as context"
        " below.---------------------{context_str}---------------------You are a"
        " support bot, searching for relevant information in Github Issues and"
        " Discussions.You will receive a question from the user, and will try to find"
        " relevant information.If you find a relevant result, include the type, name,"
        " and URL of the document, as well as a possible solution to their problem.An"
        " Example Answer:Summary: (summarize the question)Relevant Issues: (link to the"
        " issues or discussions)(Your Answer below)Given this information, please"
        " answer the question: {query_str}\n"
    )
    qa_template = PromptTemplate(template)
    query_engine = index.as_query_engine(
        service_context=service_context,
        text_qa_template=qa_template,
        similarity_top_k=8,
    )
    return query_engine


def ask_question(query_engine, question):
    conn = get_connection()
    start = datetime.datetime.now()
    logger.info("Asking question from query engine")
    response = query_engine.query(question)
    end = datetime.datetime.now()
    source_nodes = [
        {"node_id": i.node_id, "text": i.text, "score": i.score}
        for i in response.source_nodes
    ]
    event = Event(
        prompt=question,
        answer=response.response,
        metadata={
            "model": model,
            "response_metadata": response.metadata,
            "source_nodes": source_nodes,
        },
        created_at=start,
        ended_at=end,
    )

    write_event(conn, event.as_dict())

    return response


@click.command()
@click.argument("question")
def cli(question):
    model = init_model()
    click.echo(f"Question: {question}")
    response = ask_question(model, question)
    click.echo(f"Response: {response}")


if __name__ == "__main__":
    cli()
