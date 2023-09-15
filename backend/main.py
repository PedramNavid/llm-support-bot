"""Main webserver file for the Question Answering API."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from question import ask_question, init_model

app = FastAPI()
query_engine = init_model()


class Question(BaseModel):
    question: str


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
    try:
        response = ask_question(query_engine, q.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    PORT = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
