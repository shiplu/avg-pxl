"""
calculate average pixel value of an image using our GRPC microservice
"""
import logging
import argparse
from contextlib import contextmanager

import grpc

import imagestatistics_pb2
import imagestatistics_pb2_grpc


def cli_args():
    """Parses command line interface arguments

    Returns:
        argparser.Namespace: parsed arguments in a Namespace
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("image", help="image file path")
    parser.add_argument("--host", help="server host", default="127.0.0.1")
    parser.add_argument("--port", type=int, help="server port", default=30001)
    return parser.parse_args()


@contextmanager
def stub_client(host, port):
    """Provides a GRPC stub to interact with server

    Args:
        host (string): GRPC server hostname
        port (int): GRPC server port

    Yields:
        ImageStatisticsStub: local stub object
    """
    with grpc.insecure_channel("{}:{}".format(host, port)) as channel:
        stub = imagestatistics_pb2_grpc.ImageStatisticsStub(channel)
        yield stub


def run():
    args = cli_args()
    with stub_client(args.host, args.port) as stub:
        response = stub.AgeragePixel(
            imagestatistics_pb2.ImageLocation(filepath=args.image)
        )
    print(
        "average pixel of {} is #{:02X}{:02X}{:02X}".format(
            args.image, response.red, response.green, response.blue
        )
    )


if __name__ == "__main__":
    run()
