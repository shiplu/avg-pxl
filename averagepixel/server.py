"""
GRPC server that calculates average pixel of an image
"""
from concurrent import futures
import logging
import threading
import signal
import time
import sys
import argparse
from operator import mul
from dataclasses import dataclass

import grpc
from grpc_reflection.v1alpha import reflection
from PIL import Image

import config
import imagestatistics_pb2
import imagestatistics_pb2_grpc

logger = logging.getLogger(__name__)


def cli_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", help="listening host", default=config.DEFAULT_HOST)
    parser.add_argument(
        "--port", type=int, help="listening port", default=config.DEFAULT_PORT
    )
    return parser.parse_args()


class ImageStatistics(imagestatistics_pb2_grpc.ImageStatisticsServicer):
    def get_average_rgb(self, filepath):
        logger.debug("calculating average pixel value of {}".format(filepath))
        image = Image.open(filepath)
        pixel_count = mul(*image.size)

        # Read image data as we read the file.
        # This way we don't have to store all data in memory
        red, green, blue = 0.0, 0.0, 0.0
        for pixel in image.getdata():
            red += pixel[0] / pixel_count
            green += pixel[1] / pixel_count
            blue += pixel[2] / pixel_count

        image.close()

        logger.debug(
            "{} has average pixel value of ({}, {}, {})".format(
                filepath, red, green, blue
            )
        )

        return int(red), int(green), int(blue)

    def AgeragePixel(self, request, context):
        pixel = self.get_average_rgb(request.filepath)
        return imagestatistics_pb2.PixelValue(
            red=pixel[0], green=pixel[1], blue=pixel[2]
        )


class TerminationHandler:
    def __init__(self, server, grace=10):
        self.server = server
        self.grace = grace

    def __call__(self, signum, frame):
        logger.info("Got signal {}. Stopping server. . .".format(signum))
        event = self.server.stop(self.grace)
        logger.info("Stopped RPC server, Waiting for RPCs to complete. . .")
        event.wait()
        logger.info("Goodbye!")
        sys.exit(0)


def main():
    args = cli_args()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        maximum_concurrent_rpcs=10)
    imagestatistics_pb2_grpc.add_ImageStatisticsServicer_to_server(
        ImageStatistics(), server
    )
    SERVICE_NAMES = (
        imagestatistics_pb2.DESCRIPTOR.services_by_name["ImageStatistics"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("{}:{}".format(args.host, args.port))
    server.start()
    signal.signal(signal.SIGTERM, TerminationHandler(server, 5))

    logger.info("Server accepting connection on {}:{}".format(args.host, args.port))
    # Wait for eternity
    while True:
        logger.info("main thread is sleeping")
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Ctrl+C received from user.")
            logger.info("Bye!")
            break


if __name__ == "__main__":
    main()
