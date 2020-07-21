"""
calculate average pixel value of an image using our GRPC microservice
"""
import logging
import argparse
import grpc

import imagestatistics_pb2
import imagestatistics_pb2_grpc


def cli_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("image", help="image file path")
    parser.add_argument("--host", help="server host", default='127.0.0.1')
    parser.add_argument(
        "--port", type=int, help="server port", default=30001
    )
    return parser.parse_args()


def run():
    args = cli_args()
    with grpc.insecure_channel("{}:{}".format(args.host, args.port)) as channel:
        stub = imagestatistics_pb2_grpc.ImageStatisticsStub(channel)
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
