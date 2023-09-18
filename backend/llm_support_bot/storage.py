import click
import os

import pinecone
from llama_index import (
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
    set_global_service_context,
)
from llm_support_bot import document_parser as dp
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores import PineconeVectorStore


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in environment variables.")
pinecone.init(api_key=PINECONE_API_KEY, environment="gcp-starter")
pinecone_index = pinecone.Index("dagsterbot")


def get_vector_store():
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    return vector_store


def get_embedding_model():
    return OpenAIEmbedding(embed_batch_size=256)


def get_context():
    vector_store = get_vector_store()
    embed_model = get_embedding_model()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(embed_model=embed_model)
    set_global_service_context(service_context)
    return storage_context, service_context


def create_index(issue_path, discussion_path):
    i, d, c = dp.create_documents(issue_path, discussion_path)
    storage_context, service_context = get_context()

    index = VectorStoreIndex.from_documents(
        i + d + c, storage_context=storage_context, service_context=service_context
    )
    return index


def load_index():
    vector_store = get_vector_store()
    _, service_context = get_context()
    index = VectorStoreIndex.from_vector_store(vector_store, service_context)
    return index


@click.command()
@click.option("--issue-path", default="issues.json")
@click.option("--discussion-path", default="discussions.json")
@click.pass_context
def init_index(ctx, issue_path, discussion_path):
    if not (os.path.exists(issue_path) and os.path.exists(discussion_path)):
        ctx.fail("Issue/Disccusion files not found.")
    click.echo("Generating documents...")
    click.echo("Initializing the index")
    create_index(issue_path, discussion_path)
    click.echo("Initialized the index")


if __name__ == "__main__":
    init_index()
