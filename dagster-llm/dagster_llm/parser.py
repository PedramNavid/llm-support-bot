from datetime import datetime
from llama_index import Document
from llama_index.schema import NodeRelationship, RelatedNodeInfo


def issue_to_document(issue: dict):
    dt = datetime.strptime(issue["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
    text = "Issue: " + issue["bodyText"]
    excluded_llm_keys = ["documentType"]
    excluded_embed_keys = ["url", "documentType", "createdAt", "votes"]
    metadata = {
        "title": issue["title"],
        "documentType": "issue",
        "state": issue.get("state"),
        "createdAtYear": dt.year,
        "createdAtMonth": dt.month,
        "url": issue["url"],
        "labels": (
            ",".join([label["name"] for label in issue["labels"]["nodes"]]) or "None"
        ),
        "votes": issue["reactions"]["totalCount"],
    }

    return Document(
        doc_id=issue["id"],  # type: ignore
        text=text,
        metadata=metadata,  # type: ignore
        excluded_llm_metadata_keys=excluded_llm_keys,
        excluded_embed_metadata_keys=excluded_embed_keys,
    )


def comments_from_issue(comment, parent_id):
    return Document(
        doc_id=comment["id"],
        text=comment["bodyText"],
        metadata={
            "documentType": "comment",
        },
        relationships={NodeRelationship.PARENT: RelatedNodeInfo(node_id=parent_id)},
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
        doc_id=d["id"],  # type: ignore
        text=text,
        metadata=metadata,  # type: ignore
        excluded_llm_metadata_keys=excluded_llm_keys,
        excluded_embed_metadata_keys=excluded_embed_keys,
    )
