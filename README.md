Calculate average pixel value of an image

Setup
======

The project can be up and running if you have `docker-compose`. 

    docker-compose up

Local setup
-----------

### Run servers
It's also possible to run all the applications locally. Go to any of the `averagepixel` or `api` directory.
Then run either `server.py` or `web.py` using python
For `averagepixel` GRPC server

    cd averagepixel
    PYTHONPATH=. python -m server --port 8081

For `api`
    cd api
    PYTHONPATH=. python -m web --port 8080

If you use arbitrary ports for averagepixel micro-service, then that should be adjusted on `config.py` of `api` server.

### Run tests

With `make` and `pytest` it's very easy to run tests. In any of the `averagepixel` or `api` directory, running `make test` would run test for that directory

From root you can run test of `api` like this

    make -C api

Same goes for `averagepixel` directory


Features
========

### Image upload
Once it's running, you can upload an image and see the result

    curl -i  http://localhost:8000/image/pixel/average/ -F image=@/path/to/image.jpg

- You can upload PNG and JPEG images only. 
- The payload size cannot exceed 4Mb (configurable)

### Health check
There is an health-check endpoint at `/health-check` showing health of the system as in both body and HTTP status code.

### About
`/about` endpoint shows the current version


### Graceful termination
Both of the GRPC service and REST API handles SIGTERM.

Technology choices
=================

### Flask
Pretty simple and easy to setup. We are also using `flask_restful` to make it a REST API. Other choices was Django, WebPy, etc. Django is heavy and WebPy is too light. For this very light REST API flask seems good. 

### Storage
There is no database here. Images are uploaded to a directory and the directory is shared to other micro-services. Only the path of the image is passed to another micro-service for calculation

### Makefile
It's very useful to quickly setup build components based on dependency. It's also very simple and proven to be available in most system. If not the setup is always minimal (unlike *scons*, *ant*)

### GRPC
Only to explore the protocol and see how the *protobuf* compiling and others affects development workflow.

### pytest
Very good introspection upon test failure

### Gunicorn
It's always better to use a dedicated web-server (*gunicorn*, *nginx* etc) for the application. Gunicorn is used as it's written in python, which means it's extensible.