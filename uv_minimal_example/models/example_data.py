from pydantic import BaseModel


class ExampleData(BaseModel):
    name: str
    age: int
    pets: list[str]
