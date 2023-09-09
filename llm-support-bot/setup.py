from setuptools import setup, find_packages

setup(
    name="llm-support-bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gql[requests]",
        "langchain==0.0.281",
        "python-dotenv",
        "requests",
        "jq",
    ],
    extras_require={"dev": ["black", "ruff", "mypy"]},
    entry_points={},
)
