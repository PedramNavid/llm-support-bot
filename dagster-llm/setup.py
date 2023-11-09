from setuptools import find_packages, setup

setup(
    name="dagster_llm",
    packages=find_packages(exclude=["dagster_llm_tests"]),
    install_requires=[
        "dagster~=1.5.5",
        "dagster-cloud~=1.5.5",
        "llama_index~=0.8.53.post3",
        "chromadb~=0.4.15",
        "gql",
        "pinecone-client~=2.2.4",
        "jupyter",
        "pandas",
        "notebook",
        "dagstermill"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
