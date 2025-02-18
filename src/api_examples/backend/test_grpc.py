import grpc
from api_examples.backend.protos import housing_pb2, housing_pb2_grpc
from google.protobuf import empty_pb2


def test():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = housing_pb2_grpc.HousingServiceStub(channel)

        stats_resp = stub.GetStats(empty_pb2.Empty())
        print("Total rows:", stats_resp.total_rows)

        meta_resp = stub.GetMetadata(empty_pb2.Empty())
        print("Max Price:", meta_resp.Price.max)


if __name__ == "__main__":
    test()
