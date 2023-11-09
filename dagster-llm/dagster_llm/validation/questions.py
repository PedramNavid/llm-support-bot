QUESTION_ONE = """
question = '''Hello :wave:
General question:
I have an assets file with three basic assets defined with
@asset decorator, and a basic @op and @job setup from the example in 
the docs.  I was curious why the @op function do_something doesn't show 
up in the Dagit UI?  Do they have to be attached to a graph or something 
logically simple?  When I run the launchpad and try to configure 
concurrency, the @op methods don't appear in the dynamic config UI so
I'm assuming there must be a reason it doesn't show up?  There are no errors.
TIA!'''
"""

QUESTION_TWO = """
Hey friends, new to Dagster, and am trying to track down any good articles/documents about how best to architect a pipeline 
— for example, I have an asset that generates a pandas DataFrame, then the next asset saves it to a database. But would it 
be better to have an IO manager do that? But then feels like it isn’t as clear or explicit . . . so maybe an op?')
"""

QUESTION_THREE = """
Hi everyone,probably a newbie question: how can I iterate through values in an op 
so it executes downstream ops for each value?  In my case I want to migrate data 
and I need to iterate through schemas names. In the original script it's done 
simply using for loops, but I feel a Dagster job needs another approach.
"""

QUESTION_FOUR = """
So I have a dbt_assets decorator that is pulling in 4 dbt models. All siblings. But I can't seem to pull them together 
into a job since I switched to using the decorator for dagster asset creation. How would I select 4 siblings inside an 
AssetSelection?
"""

QUESTION_FIVE = """
Is it possible to turn off auto materialize policy only for a specific asset?
"""

QUESTION_SIX = """
Hello everyone, does any one know how can we delete partitions from the dagster cloud ?
"""

QUESTION_SEVEN = """
Hello ... How do you run a "dbt source freshness" with @dbt_assets ?
There are no models associated (to be materialized) when dbt runs a source freshness so is this even possible? I.e. something like below.
My first attempt was just putting together a function that only ran a source freshness (the manifest.json has one model in it)

@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
    io_manager_key="snowflake_io_manager",
)

def my_dbt_assets(context: OpExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["source","freshness"], context=context).stream()
Running dbt command: `dbt --no-write-json --no-use-colors source freshness --target dev --select fqn:the_models_@dbt_assets`.
"""

QUESTION_EIGHT = """
Hi. Is there an option to check whether an asset run was triggered as part of a backfill?
"""

ALL_QUESTIONS = [
    QUESTION_ONE,
    QUESTION_TWO,
    QUESTION_THREE,
    QUESTION_FOUR,
]
