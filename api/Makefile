INCLUDES=../protos
SOURCE=../protos/imagestatistics.proto
COMPILER=python -m grpc_tools.protoc

all: test VERSION

test: imagestatistics_pb2.py imagestatistics_pb2_grpc.py imagestatistics_client.py
	PYTHONPATH=. pytest

imagestatistics_pb2_grpc.py:
	${COMPILER} -I${INCLUDES}  ${SOURCE} --grpc_python_out=.

imagestatistics_pb2.py:
	${COMPILER} -I${INCLUDES}  ${SOURCE} --python_out=.

imagestatistics_client.py:
	cp ../averagepixel/client.py imagestatistics_client.py

VERSION:
	git describe > VERSION

clean:
	-rm imagestatistics_pb2.py
	-rm imagestatistics_pb2_grpc.py
	-rm imagestatistics_client.py
	-rm VERSION
