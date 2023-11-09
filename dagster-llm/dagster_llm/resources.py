from dagster import ConfigurableResource, EnvVar, get_dagster_logger, file_relative_path
from gql.transport.requests import RequestsHTTPTransport
import gql
import pinecone
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores import PineconeVectorStore, ChromaVectorStore
from llama_index import (
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
    download_loader,
    set_global_service_context,
)
import chromadb


class GithubResource(ConfigurableResource):
    github_token: str

    def client(self):
        return gql.Client(
            schema=None,
            transport=RequestsHTTPTransport(
                url="https://api.github.com/graphql",
                headers={
                    "Authorization": f"Bearer {self.github_token}",
                },
                retries=3,
            ),
            fetch_schema_from_transport=True,
        )

    def get_issues(self, start_date="2023-01-01", end_date="2023-12-31"):
        issues_query_str = """
query {
  search(
    query: "repo:dagster-io/dagster created:START_DATE..END_DATE is:issue"
    type: ISSUE
    first: 100
    after: CURSOR_PLACEHOLDER
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    issueCount
    edges {
      node {
        ... on Issue {
          id
          number
          title
          bodyText
          createdAt
          closedAt
          state
          stateReason
          url
          comments(last: 10) {
            totalCount
            nodes {
              id
              bodyText
            }
          }
          labels(first: 10) {
            nodes {
              name
            }
          }
          reactions(content: THUMBS_UP) {
            totalCount
          }
        }
      }
    }
  }
}
""".replace(
            "START_DATE", start_date
        ).replace(
            "END_DATE", end_date
        )
        return self.fetch_results(issues_query_str, "issues")

    def get_discussions(self, start_date="2023-01-01", end_date="2023-12-31"):
        discussion_query_str = """
query {
  search(
    query: "repo:dagster-io/dagster updated:START_DATE..END_DATE is:discussion"
    type: DISCUSSION
    first: 100
    after: CURSOR_PLACEHOLDER
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    discussionCount
    edges {
      node {
        ... on Discussion {
          id
          number
          title
          bodyText
          createdAt
          closed
          closedAt
          stateReason
          url
          isAnswered
          upvoteCount
          category { 
            name
            slug
          }
          answer {
            bodyText
          }
          comments(last: 10) {
            totalCount
            nodes {
              id
              bodyText
            }
          }
          labels(first: 10) {
            nodes {
              name
            }
          }
          reactions(content: THUMBS_UP) {
            totalCount
          }
        }
      }
    }
  }
}
""".replace(
            "START_DATE", start_date
        ).replace(
            "END_DATE", end_date
        )
        return self.fetch_results(discussion_query_str, "discussions")

    def fetch_results(self, query_str: str, object_type: str):
        log = get_dagster_logger()
        log.info("Using Query: %s", query_str)
        client = self.client()
        cursor = None
        results = []
        while True:
            log.info(
                f"Fetching results from Github: {object_type} with cursor: {cursor}"
            )
            query = gql.gql(
                query_str.replace(
                    "CURSOR_PLACEHOLDER", f'"{cursor}"' if cursor else "null"
                ),
            )
            result = client.execute(query)
            search = result["search"]
            edges = search["edges"]
            for node in edges:
                results.append(node["node"])
            log.info(f"Total results: {len(results)}")
            if not search["pageInfo"]["hasNextPage"]:
                break
            cursor = search["pageInfo"]["endCursor"]
        return results


def pinecone_storage_context(name: str = "dagsterbot"):
    pinecone_api_key = EnvVar("PINECONE_API_KEY").get_value()
    environment: str = "us-west1-gcp"

    pinecone.init(api_key=pinecone_api_key, environment=environment)
    index = pinecone.Index(name)
    vector_store = PineconeVectorStore(
        pinecone_index=index,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return (vector_store, storage_context)


def dev_storage_context():
    chroma_client = chromadb.PersistentClient(
        path=file_relative_path(__file__, "../chromadb/")
    )
    chroma_collection = chroma_client.get_or_create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return (vector_store, storage_context)


class LlamaResource(ConfigurableResource):
    environ: str

    def get_storage_context(self):
        if self.environ.upper() == "PROD":
            return pinecone_storage_context()
        return dev_storage_context()

    @staticmethod
    def service_context():
        embed_model = OpenAIEmbedding(embed_batch_size=256)
        service_context = ServiceContext.from_defaults(embed_model=embed_model)
        set_global_service_context(service_context)
        return service_context

    @staticmethod
    def vector_index(documents, storage_context, service_context):
        index = VectorStoreIndex.from_vector_store(
            storage_context[0],
            storage_context=storage_context[1],
        )
        for doc in documents:
            index.update(doc)
        return index


class ApifyResource(ConfigurableResource):
    token: str

    def reader(self):
        ApifyActor = download_loader("ApifyActor")
        return ApifyActor(self.token)  # type: ignore

    def dataset(self):
        ApifyDataset = download_loader("ApifyDataset")
        return ApifyDataset(self.token)
