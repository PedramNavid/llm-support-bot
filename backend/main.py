"""Main webserver file for the Question Answering API."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from question import ask_question, init_model
import logging

app = FastAPI()
query_engine = init_model("gpt-3.5-turbo-16k")
query_engine_gpt4 = init_model("gpt-4")
logger = logging.getLogger(__name__)

class Question(BaseModel):
    question: str
    model: str


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask")
async def read_question(q: Question):
    model = 'gpt3'
    logger.info(f"Asked Question: {q} with model: {model}")
    try:
        if model == "gpt4":
            response = ask_question(query_engine_gpt4, q.question)
        elif 'gpt3' in model:
            response = ask_question(query_engine, q.question)
        else:
            return HTTPException(status_code=400, detail="Invalid model specified")
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    PORT = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
