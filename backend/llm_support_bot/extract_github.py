import json
import os
from datetime import datetime

import click
import gql
from dotenv import load_dotenv
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

issues_query_str = """
query {
  repository(owner:"dagster-io", name: "dagster") {
    issues(first: 100, after: CURSOR_PLACEHOLDER) {
        pageInfo {
            endCursor
            hasNextPage
            }
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
              comments(last: 10) {
                totalCount
                nodes {
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
"""
discussion_query_str = """query {
  repository(owner:"dagster-io", name: "dagster") {
    discussions(first: 100, after: CURSOR_PLACEHOLDER) {
      pageInfo{
        endCursor
        hasNextPage
        }
          edges{
            node{
              id
              number
              title
              bodyText
              answer{
                bodyText
              }
              category{
                name
              }
              createdAt
              closedAt
              url
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
"""

client = gql.Client(
    schema=None,
    transport=RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f'Bearer {os.getenv("GITHUB_API_TOKEN")}'},
        use_json=True,
    ),
    fetch_schema_from_transport=True,
)


def fetch_results(query_str: str, object_type: str, fname: str):
    results_json: list[dict] = []
    has_next_page = True
    cursor = None

    click.echo(f"Fetching {object_type} from Github")
    while has_next_page:
        click.echo(f"Fetching {object_type}... {len(results_json)}")
        current_query = gql.gql(
            query_str.replace("CURSOR_PLACEHOLDER", f'"{cursor}"' if cursor else "null")
        )
        result = client.execute(current_query)
        issues = result["repository"][object_type]["edges"]
        for node in issues:
            results_json.append(node["node"])

        cursor = result["repository"][object_type]["pageInfo"]["endCursor"]
        has_next_page = result["repository"][object_type]["pageInfo"]["hasNextPage"]

    json.dump(results_json, open(fname, "w"), indent=2)
    click.echo(f"Done! {len(results_json)} {object_type} fetched.")


@click.command()
@click.option("--issues", is_flag=True, default=False)
@click.option("--discussions", is_flag=True, default=False)
@click.pass_context
def cli(ctx, issues, discussions):
    # Create data dir
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.getenv("GITHUB_API_TOKEN"):
        ctx.fail("GITHUB_API_TOKEN not set in .env file")

    if not issues and not discussions:
        ctx.fail("Must specify at least one of --issues or --discussions")

    if issues:
        click.echo("Fetching issues...")
        fname_issues = os.path.join(
            "data", f"issues-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        )
        fetch_results(issues_query_str, "issues", fname_issues)
        click.echo(f"Wrote issues to {fname_issues}")

    if discussions:
        click.echo("Fetching discussions...")
        fname_discussions = os.path.join(
            "data", f"discussions-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        )
        fetch_results(discussion_query_str, "discussions", fname_discussions)


if __name__ == "__main__":
    cli()
