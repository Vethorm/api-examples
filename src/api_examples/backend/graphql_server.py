import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from api_examples.backend.database import db


@strawberry.type
class MaxMin:
    max: float
    min: float


@strawberry.type
class Metadata:
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


@strawberry.type
class Stats:
    total_rows: int


@strawberry.type
class Query:
    @strawberry.field
    def stats(self) -> Stats:
        stats_data = db.stats()
        return Stats(total_rows=stats_data["total_rows"])

    @strawberry.field
    def metadata(self) -> Metadata:
        meta_dict = db.metadata()
        # NOTE: strawberry types don't support conversion, have to explicitly set
        # **meta_dict doesn't work
        return Metadata(
            Price=MaxMin(max=meta_dict["Price"]["max"], min=meta_dict["Price"]["min"]),
            Bedrooms=MaxMin(
                max=meta_dict["Bedrooms"]["max"], min=meta_dict["Bedrooms"]["min"]
            ),
            Bathrooms=MaxMin(
                max=meta_dict["Bathrooms"]["max"], min=meta_dict["Bathrooms"]["min"]
            ),
            SquareFeet=MaxMin(
                max=meta_dict["SquareFeet"]["max"], min=meta_dict["SquareFeet"]["min"]
            ),
            YearBuilt=MaxMin(
                max=meta_dict["YearBuilt"]["max"], min=meta_dict["YearBuilt"]["min"]
            ),
            GarageSpaces=MaxMin(
                max=meta_dict["GarageSpaces"]["max"],
                min=meta_dict["GarageSpaces"]["min"],
            ),
            LotSize=MaxMin(
                max=meta_dict["LotSize"]["max"], min=meta_dict["LotSize"]["min"]
            ),
            ZipCode=MaxMin(
                max=meta_dict["ZipCode"]["max"], min=meta_dict["ZipCode"]["min"]
            ),
            CrimeRate=MaxMin(
                max=meta_dict["CrimeRate"]["max"], min=meta_dict["CrimeRate"]["min"]
            ),
            SchoolRating=MaxMin(
                max=meta_dict["SchoolRating"]["max"],
                min=meta_dict["SchoolRating"]["min"],
            ),
        )


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
