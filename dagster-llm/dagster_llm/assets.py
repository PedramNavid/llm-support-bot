from dagster import (
    AssetExecutionContext,
    BackfillPolicy,
    MaterializeResult,
    asset,
    DailyPartitionsDefinition,
    file_relative_path,
)
from .parser import issue_to_document, comments_from_issue, discussion_to_document
from .resources import ApifyResource, GithubResource, LlamaResource
from dagstermill import define_dagstermill_asset

from llama_index.readers.schema import Document

partition_def = DailyPartitionsDefinition(start_date="2023-01-01")


@asset(
    partitions_def=partition_def,
    backfill_policy=BackfillPolicy.single_run(),
    compute_kind="Github",
    group_name="ETL",
)
def issues(
    context: AssetExecutionContext, github: GithubResource, llama: LlamaResource
) -> MaterializeResult:
    start, end = context.partition_time_window
    issues = github.get_issues(
        start_date=start.strftime("%Y-%m-%d"), end_date=end.strftime("%Y-%m-%d")
    )
    issue_documents = []
    comment_documents = []
    for issue in issues:
        if len(issue["bodyText"]) > 10:
            issue_documents.append(issue_to_document(issue))
            for comment in issue["comments"]["nodes"]:
                comment_documents.append(comments_from_issue(comment, issue["id"]))
    storage_context = llama.get_storage_context()
    service_context = llama.service_context()
    llama.vector_index(
        issue_documents + comment_documents, storage_context, service_context
    )
    return MaterializeResult(
        metadata={
            "count_issue_documents": len(issue_documents),
            "count_comment_documents": len(comment_documents),
            "count_issues": len(issues),
        }
    )


@asset(
    partitions_def=partition_def,
    backfill_policy=BackfillPolicy.single_run(),
    compute_kind="Github",
    group_name="ETL",
)
def discussion(
    context: AssetExecutionContext, github: GithubResource, llama: LlamaResource
) -> MaterializeResult:
    start, end = context.partition_time_window
    discussions = github.get_discussions(
        start_date=start.strftime("%Y-%m-%d"), end_date=end.strftime("%Y-%m-%d")
    )
    discussion_documents = [discussion_to_document(d) for d in discussions]
    storage_context = llama.get_storage_context()
    service_context = llama.service_context()
    context.log.info("Using storage context: %s", storage_context)
    llama.vector_index(discussion_documents, storage_context, service_context)
    return MaterializeResult(
        metadata={
            "count_discussions": len(discussions),
            "count_discussion_documents": len(discussion_documents),
        }
    )


@asset(compute_kind="Apify", group_name="ETL")
def dagster_docs(
    context: AssetExecutionContext,
    llama: LlamaResource,
    apify: ApifyResource,
) -> MaterializeResult:
    def tranform_dataset_item(item):
        context.log.debug("Transforming item: %s", item)
        return Document(
            doc_id=item.get("url"),
            text=item.get("text"),
            metadata={
                "documentType": "dagster-documentation",
                "url": item.get("url"),
            },
        )

    reader = apify.dataset()
    documents = reader.load_data(
        dataset_id="4FcOr0Tp7AupSeJ7v", dataset_mapping_function=tranform_dataset_item
    )

    # reader = apify.reader()
    # documents = reader.load_data(
    # actor_id="apify/website-content-crawler",
    # run_input={
    # "runMode": "DEVELOPMENT",
    # "startUrls": [{"url": "https://docs.dagster.io/"}],
    # "globs": [{"glob": "https://docs.dagster.io/**/*"}],
    # },
    # dataset_mapping_function=tranform_dataset_item,
    # )

    llama.vector_index(documents, llama.get_storage_context(), llama.service_context())
    return MaterializeResult(metadata={"count_documents": len(documents)})


prompt_validation_asset = define_dagstermill_asset(
    name="prompt_validation",
    notebook_path=file_relative_path(__file__, "notebooks/prompt_validation.ipynb"),
    deps=[issues, discussion, dagster_docs],
    group_name="Validation",
)
