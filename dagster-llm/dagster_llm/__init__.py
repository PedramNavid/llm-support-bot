from dagster import Definitions, load_assets_from_modules, EnvVar

import os
from . import assets
from .resources import ApifyResource, GithubResource, LlamaResource
from dagstermill import ConfigurableLocalOutputNotebookIOManager

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "github": GithubResource(github_token=EnvVar("GITHUB_API_TOKEN")),
        "llama": LlamaResource(environ=EnvVar("DAGSTER_ENV")),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
        "apify": ApifyResource(token=EnvVar("APIFY_TOKEN")),
    },
)
