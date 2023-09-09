import os
import json
import gql
from dotenv import load_dotenv
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

query = gql.gql("""
query {
  repository(owner:"dagster-io", name: "dagster") {
    issues(last: 100 ) {
          edges{
            node{
              id
              number
              title
              bodyText
              state
              createdAt
              closedAt
              url
              labels(first: 5) {
                nodes {
                    name
                    description
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
""")

client = gql.Client(
    schema=None,
    transport=RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f'Bearer {os.getenv("GITHUB_API_TOKEN")}'},
        use_json=True,
    ),
    fetch_schema_from_transport=True,
)

# TODO: Add pagination and cursor

# Execute the query
result = client.execute(query)
results_json: list[dict] = []
for node in result["repository"]["issues"]["edges"]:
    results_json.append(node["node"])
# Print the results

json.dump(results_json, open("data.json", "w"), indent=2)
