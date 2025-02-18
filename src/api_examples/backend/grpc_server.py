from concurrent import futures
import grpc

from api_examples.backend.protos import housing_pb2, housing_pb2_grpc
from google.protobuf import empty_pb2

from api_examples.backend.database import db

from loguru import logger


class HousingServiceServicer(housing_pb2_grpc.HousingServiceServicer):
    def GetStats(self, request, context):
        stats_dict = db.stats()
        return housing_pb2.Stats(total_rows=stats_dict["total_rows"])

    def GetMetadata(self, request, context):
        metadata_dict = db.metadata()
        return housing_pb2.Metadata(
            Price=housing_pb2.MaxMin(
                max=metadata_dict["Price"]["max"], min=metadata_dict["Price"]["min"]
            ),
            Bedrooms=housing_pb2.MaxMin(
                max=metadata_dict["Bedrooms"]["max"],
                min=metadata_dict["Bedrooms"]["min"],
            ),
            Bathrooms=housing_pb2.MaxMin(
                max=metadata_dict["Bathrooms"]["max"],
                min=metadata_dict["Bathrooms"]["min"],
            ),
            SquareFeet=housing_pb2.MaxMin(
                max=metadata_dict["SquareFeet"]["max"],
                min=metadata_dict["SquareFeet"]["min"],
            ),
            YearBuilt=housing_pb2.MaxMin(
                max=metadata_dict["YearBuilt"]["max"],
                min=metadata_dict["YearBuilt"]["min"],
            ),
            GarageSpaces=housing_pb2.MaxMin(
                max=metadata_dict["GarageSpaces"]["max"],
                min=metadata_dict["GarageSpaces"]["min"],
            ),
            LotSize=housing_pb2.MaxMin(
                max=metadata_dict["LotSize"]["max"], min=metadata_dict["LotSize"]["min"]
            ),
            ZipCode=housing_pb2.MaxMin(
                max=metadata_dict["ZipCode"]["max"], min=metadata_dict["ZipCode"]["min"]
            ),
            CrimeRate=housing_pb2.MaxMin(
                max=metadata_dict["CrimeRate"]["max"],
                min=metadata_dict["CrimeRate"]["min"],
            ),
            SchoolRating=housing_pb2.MaxMin(
                max=metadata_dict["SchoolRating"]["max"],
                min=metadata_dict["SchoolRating"]["min"],
            ),
        )


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    housing_pb2_grpc.add_HousingServiceServicer_to_server(
        HousingServiceServicer(), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"gRPC server running on port {port}")
    server.wait_for_termination()
