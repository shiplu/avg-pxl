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
        """Calcualte the average rgb value of an image file in specified path

        Args:
            filepath (string): image file path

        Returns:
            tuple: 3-tuple of integers containing Red, Green and Blue components
        """
        logger.debug("calculating average pixel value of {}".format(filepath))
        red, green, blue = 0.0, 0.0, 0.0
        with Image.open(filepath) as image:
            pixel_count = mul(*image.size)

            # Read image data as we read the file.
            # This way we don't have to store all data in memory
            for pixel in image.getdata():
                red += pixel[0] / pixel_count
                green += pixel[1] / pixel_count
                blue += pixel[2] / pixel_count

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
    """Handles graceful termination of a server
    """
    def __init__(self, server, grace_period=10):
        """Initialized termination handler

        Args:
            server (grpc.Server): grpc server
            grace_period (int, optional): gracefull shutdown period. Defaults to 10.
        """
        self.server = server
        self.grace_period = grace_period

    def __call__(self, signum, frame):
        logger.info("Got signal {}. Stopping server. . .".format(signum))
        event = self.server.stop(self.grace_period)
        logger.info("Stopped RPC server, Waiting for RPCs to complete. . .")
        event.wait()
        logger.info("Goodbye!")
        sys.exit(0)


def main():
    args = cli_args()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), maximum_concurrent_rpcs=10
    )
    imagestatistics_pb2_grpc.add_ImageStatisticsServicer_to_server(
        ImageStatistics(), server
    )
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
