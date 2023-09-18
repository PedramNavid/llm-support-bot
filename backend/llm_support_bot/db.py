import os

import psycopg

from llm_support_bot.types import Event


def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    return psycopg.connect(DATABASE_URL)


def write_event(conn, event: dict):
    with conn.cursor() as cur:
        insert = """
            INSERT INTO responses (prompt, answer, metadata, created_at, ended_at)
            VALUES (%(prompt)s, %(answer)s, %(metadata)s, %(created_at)s, %(ended_at)s)
            """

        cur.execute(insert, event)
        conn.commit()
        cur.close()


if __name__ == "__main__":
    event = Event(
        prompt="What is the meaning of life?", answer="42", metadata={"model": "gpt3"}
    )
    conn = get_connection()
    write_event(conn, event.as_dict())
