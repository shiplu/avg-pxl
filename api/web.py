import os
import uuid
import logging
import argparse

from flask import Flask
from flask import request
from flask_restful import Api
from flask_restful import Resource

import config
import imagestatistics_client
import imagestatistics_pb2
import imagestatistics_pb2_grpc


logger = logging.getLogger(__name__)

app = Flask(config.APP_NAME)
app.config.from_object(config)
api = Api(app)


def cli_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", help="listening host", default=config.DEFAULT_HOST)
    parser.add_argument(
        "--port", type=int, help="listening port", default=config.DEFAULT_PORT
    )
    parser.add_argument(
        "--debug",
        help="enable web server debug logs",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


class BaseResource(Resource):
    """Base resource handler that handles response formats
    """

    def format_error(self, message, code, **extra):
        """Formats error message as json

        Args:
            message (str): error message
            code (int): http code

        Returns:
            (dict, int): tuple of response dict and http code
        """
        response = dict(**extra)
        response["error"] = message
        return response, code

    def format_data(self, data, code=200, length=None):
        """Formats data as json

        Args:
            data (any): data to put in the response container in 'data' field.
            code (int): http code. default 200.
            length (int): if data is comp

        Returns:
            (dict, int): tuple of response dict and http code
        """
        response = {"data": data}
        if isinstance(data, (tuple, list)) and length is None:
            response["count"] = len(data)
        if length:
            response["count"] = length
        return response, code


class PostImagePixelAverage(BaseResource):
    def allowed_file(self, filename):
        _, extension = filename.rsplit(".", 1)
        return extension.lower() in config.ALLOWED_IMAGE_EXTENSIONS

    def storage_filename(self, filename):
        unique_filename = uuid.uuid3(uuid.NAMESPACE_URL, filename)
        return os.path.join(config.DATA_STORAGE, str(unique_filename))

    def post(self):
        if "image" not in request.files:
            return self.format_error("'image' not found in submitted files", 400)

        file = request.files["image"]

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return self.format_error("No selected file", 400)

        if not file:
            return self.format_error("Empty file", 400)

        if not self.allowed_file(file.filename):
            return self.format_error("Unsupported file '{}'".format(file.filename), 400)

        filename = self.storage_filename(file.filename)

        if config.OVERRIDE_SAMEFILE:
            file.save(filename)
        # write only when the file doesn't exist
        elif not os.path.isfile(filename):
            file.save(filename)

        with imagestatistics_client.stub_client(
            config.IMAGE_STATISTICS_HOST, config.IMAGE_STATISTICS_PORT
        ) as client:
            response = client.AgeragePixel(
                imagestatistics_pb2.ImageLocation(filepath=filename)
            )

        return self.format_data(
            {
                "filename": os.path.basename(filename),
                "color": "#{:02X}{:02X}{:02X}".format(
                    response.red, response.green, response.blue
                ),
            }
        )


class HealthCheck(BaseResource):
    def get(self):
        storage = config.DATA_STORAGE
        healthy = os.path.isdir(storage) and os.access(storage, os.W_OK)
        if healthy:
            return self.format_data({"status": "OK"})
        else:
            return self.format_error("Internal problem", 503, status="FAIL")


class About(BaseResource):
    def get(self):
        try:
            with open("VERSION") as version_file:
                version = version_file.read().strip()
        except IOError:
            return self.format_error("Error extracting version info.", 500)
        else:
            return self.format_data({"version": version, "app": config.APP_NAME})


api.add_resource(PostImagePixelAverage, "/image/pixel/average/")
api.add_resource(HealthCheck, "/health-check/")
api.add_resource(About, "/about/")


def main():
    args = cli_args()

    for rule in app.url_map.iter_rules():
        logger.info(
            "%20s\t%-30s\t%s" % (", ".join(rule.methods), rule.rule, rule.endpoint)
        )

    app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
