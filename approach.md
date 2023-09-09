## Overall Idea

Dagster support requests come through Slack in one of several
Slack channels, or via Github Issues.

Questions are answered via Slack, or as Github Discussions or Github Issues.

## Phases

### Ingestion

First, we need to ingest a list of reference documents:

- Github Issues
  - Issue title, description, labels, reactions
- Github Discusions
- Docs Pages

Each of these can be stored in a vector database as a set of embeddings
which has a reference to the underlying URL.

## Prompt Engineering

When a question is asked, we find N embeddings and add that to the context
along with the question. Then we have a sequence of activities we want to
complete.

1. Identify if this question has a potentially relevant answer based
   on an existing resource. If so, offer this resource to the user.
2. If there is no highly relevant topic, then consider the user input prompt
   for the following questions:
   a. Did the user provide enough information for support to answer the
   question, i.e. Dagster version, error message, steps they have tried.
   b. ...addition considerations here?
3. Categorize the question. Provide a list of labels and descriptions.
   Potentially provide context examples here as well.

## UX

In the first phase, we want to make these automated questions/follow-ups
available to the support staff without automating the response. As we get
more comfortable with the responses, we may consider automating some of it.

## Considerations

It would be nice if we had a feedback mechanism, thumbs up or thumbs down
to help us get feedback on the responses the LLM generates.
