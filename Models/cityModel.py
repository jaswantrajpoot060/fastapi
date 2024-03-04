from pydantic import BaseModel


class City(BaseModel):
    StateId: int
    Name: str
    CityCode: str
