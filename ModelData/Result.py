from dataclasses import dataclass

@dataclass
class Result:
    url: str
    status: int
    content: dict
