rest-server:
	uv run uvicorn api_examples.backend.rest_server:app --reload

generate-proto:
	uv run python -m grpc_tools.protoc \
		-I=src/api_examples/backend/protos \
		--python_out=src/api_examples/backend/protos \
		--grpc_python_out=src/api_examples/backend/protos \
		src/api_examples/backend/protos/housing.proto

grpc-server:
	uv run grpc_server

graphql-server:
	uv run uvicorn api_examples.backend.graphql_server:app --reload

streamlit:
	uv run streamlit run src/api_examples/frontend/main.py