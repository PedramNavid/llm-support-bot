import json
import os
import click
from datetime import datetime
from typing import List

from llama_index import Document
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import MetadataMode, NodeRelationship, RelatedNodeInfo
from llm_support_bot.options import CHUNK_OVERLAP, CHUNK_SIZE


def issue_to_document(issue: dict):
    dt = datetime.strptime(issue["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
    text = "Issue: " + issue["bodyText"]
    excluded_llm_keys = ["documentType"]
    excluded_embed_keys = ["url", "documentType", "createdAt", "votes"]
    metadata = {
        "title": issue["title"],
        "documentType": "issue",
        "state": issue["state"],
        "createdAtYear": dt.year,
        "createdAtMonth": dt.month,
        "url": issue["url"],
        "labels": ",".join([label["name"] for label in issue["labels"]["nodes"]])
        or "None",
        "votes": issue["reactions"]["totalCount"],
    }

    return Document(
        id_=issue["id"],  # type: ignore
        text=text,
        metadata=metadata,  # type: ignore
        excluded_llm_metadata_keys=excluded_llm_keys,
        excluded_embed_metadata_keys=excluded_embed_keys,
    )


def discussion_to_document(d: dict):
    dt = datetime.strptime(d["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
    answer = d["answer"]["bodyText"] if d["answer"] else "None"
    text = "Question: " + d["bodyText"] + "\n\nAnswer: " + answer
    excluded_llm_keys = ["documentType"]
    excluded_embed_keys = ["url", "documentType", "createdAt", "votes"]
    metadata = {
        "documentType": "discussion",
        "title": d["title"],
        "category": d["category"].get("name", "Uncategorized"),
        "createdAtYear": dt.year,
        "createdAtMonth": dt.month,
        "url": d["url"],
        "labels": ",".join([label["name"] for label in d["labels"]["nodes"]]) or "None",
        "votes": d["reactions"]["totalCount"],
    }

    return Document(
        id_=d["id"],  # type: ignore
        text=text,
        metadata=metadata,  # type: ignore
        excluded_llm_metadata_keys=excluded_llm_keys,
        excluded_embed_metadata_keys=excluded_embed_keys,
    )


def comments_from_issue(comment, parent_id):
    return Document(
        text=comment["bodyText"],
        metadata={
            "documentType": "comment",
        },
        relationships={NodeRelationship.PARENT: RelatedNodeInfo(node_id=parent_id)},
    )


def create_node_parser():
    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return node_parser


def generate_nodes(node_parser, documents: List[Document]):
    return node_parser.get_nodes_from_documents(documents)


def create_documents(issue_path, discussion_path):
    issues = json.load(open(issue_path))
    discussions = json.load(open(discussion_path))

    issue_documents = []
    comment_documents = []

    for issue in issues:
        # Ignore issues with no body text
        if len(issue["bodyText"]) > 10:
            issue_documents.append(issue_to_document(issue))
            for comment in issue["comments"]["nodes"]:
                comment_documents.append(comments_from_issue(comment, issue["id"]))

    discussion_documents = [discussion_to_document(d) for d in discussions]

    return (issue_documents, discussion_documents, comment_documents)


@click.command()
@click.option("--issue-path", default="issues.json")
@click.option("--discussion-path", default="discussions.json")
@click.pass_context
def cli(ctx, issue_path, discussion_path):
    if not (os.path.exists(issue_path) and os.path.exists(discussion_path)):
        ctx.fail("Issue/Disccusion files not found.")
    click.echo("Generating documents...")
    issues, discussions, comments = create_documents(issue_path, discussion_path)
    print(issues[0].get_content(metadata_mode=MetadataMode.EMBED))
    print("\n" + "-" * 80)
    print(comments[5].get_content(metadata_mode=MetadataMode.EMBED))
    print("\n" + "-" * 80)
    print(discussions[5].get_content(metadata_mode=MetadataMode.LLM))


if __name__ == "__main__":
    cli()
