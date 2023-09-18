import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    prompt: str
    answer: str
    metadata: dict
    created_at: datetime = datetime.now()
    ended_at: datetime = datetime.now()

    def as_dict(self):
        return {
            "prompt": self.prompt,
            "answer": self.answer,
            "metadata": json.dumps(self.metadata),
            "created_at": self.created_at,
            "ended_at": self.ended_at,
        }
