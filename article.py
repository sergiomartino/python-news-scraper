from dataclasses import dataclass

@dataclass
class Article:
    title: str

    def __hash__(self):
        return hash(self.title)
