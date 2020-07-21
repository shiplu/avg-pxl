from concurrent import futures
import logging
import threading
import signal
import time
import sys

import grpc
from grpc_reflection.v1alpha import reflection

import imagestatistics_pb2
import imagestatistics_pb2_grpc

logger = logging.getLogger(__name__)


class ImageStatistics(imagestatistics_pb2_grpc.ImageStatisticsServicer):
    def get_average_rgb(self, filepath):
        return (20, 192, 100)

    def AgeragePixel(self, request, context):
        rgb = self.get_average_rgb(request.filepath)
        return imagestatistics_pb2.PixelValue(
            red=rgb[0],
            green=rgb[1],
            blue=rgb[2]
        )


class TerminationHandler:
    def __init__(self, server, grace=10):
        self.server = server
        self.grace = grace

    def __call__(self, signum, frame):
        logger.info("Got signal {}, {}".format(signum, frame))
        event = self.server.stop(self.grace)
        logger.info("Stopped RPC server, Waiting for RPCs to complete...")
        event.wait()
        logger.info("Goodbye!")
        sys.exit(0)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imagestatistics_pb2_grpc.add_ImageStatisticsServicer_to_server(
        ImageStatistics(), server
    )
    SERVICE_NAMES = (
        imagestatistics_pb2.DESCRIPTOR.services_by_name["ImageStatistics"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    signal.signal(signal.SIGTERM, TerminationHandler(server, 5))

    # Wait for eternity
    while True:
        logger.info("main thread is sleeping")
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Ctrl+C received from user. Bye!")
            break


if __name__ == "__main__":
    logging.basicConfig()
    serve()
