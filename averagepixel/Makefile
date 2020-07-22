INCLUDES=../protos
SOURCE=../protos/imagestatistics.proto
COMPILER=python -m grpc_tools.protoc

all: test

test: imagestatistics_pb2.py imagestatistics_pb2_grpc.py
	PYTHONPATH=. pytest

imagestatistics_pb2_grpc.py:
	${COMPILER} -I${INCLUDES}  ${SOURCE} --grpc_python_out=.

imagestatistics_pb2.py:
	${COMPILER} -I${INCLUDES}  ${SOURCE} --python_out=.

clean:
	-rm imagestatistics_pb2.py
	-rm imagestatistics_pb2_grpc.py