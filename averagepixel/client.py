"""
calculate average pixel value of an image using our GRPC microservice
"""
import logging
import argparse
import grpc

import imagestatistics_pb2
import imagestatistics_pb2_grpc

def cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help="image file path")
    return parser.parse_args()

def run():
    args = cli_args()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = imagestatistics_pb2_grpc.ImageStatisticsStub(channel)
        response = stub.AgeragePixel(imagestatistics_pb2.ImageLocation(filepath=args.image))
    print(
        "average pixel of {} is #{:02X}{:02X}{:02X}".format(
            args.image, response.red, response.green, response.blue
        )
    )


if __name__ == "__main__":
    logging.basicConfig()
    run()
