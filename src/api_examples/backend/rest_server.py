from fastapi import FastAPI
from api_examples.backend.database import db

from pydantic import BaseModel

app = FastAPI()


class Stats(BaseModel):
    total_rows: int


class MaxMin(BaseModel):
    max: int | float
    min: int | float


class Metadata(BaseModel):
    Price: MaxMin
    Bedrooms: MaxMin
    Bathrooms: MaxMin
    SquareFeet: MaxMin
    YearBuilt: MaxMin
    GarageSpaces: MaxMin
    LotSize: MaxMin
    ZipCode: MaxMin
    CrimeRate: MaxMin
    SchoolRating: MaxMin


@app.get("/")
def read_root():
    return ["Hello World"]


@app.get("/stats")
def stats() -> Stats:
    return Stats(**db.stats())


@app.get("/metadata")
def metadata():
    return Metadata(**db.metadata())
