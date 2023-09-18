from setuptools import find_packages, setup

setup(
    name="llm_support_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gql[requests]",
        "chromadb",
        "pinecone-client",
        "pydantic==1.10.11",
        "python-dotenv",
        "requests",
        "fastapi",
        "uvicorn",
        "llama-index",
        "click",
        "sentence-transformers",
        "psycopg[binary]",
    ],
    extras_require={"dev": ["black", "ruff", "mypy"]},
    entry_points={},
)
