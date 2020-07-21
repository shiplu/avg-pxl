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


import grpc
from grpc_reflection.v1alpha import reflection

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
        return (20, 192, 100)

    def AgeragePixel(self, request, context):
        rgb = self.get_average_rgb(request.filepath)
        return imagestatistics_pb2.PixelValue(red=rgb[0], green=rgb[1], blue=rgb[2])


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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
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
