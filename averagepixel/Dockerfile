FROM python:3.7-slim

ADD . /code/
ENV PYTHONPATH /code

WORKDIR /code
RUN apt-get update && apt-get install make && pip install -r requirements.txt && make

CMD ["/usr/local/bin/python", "-m", "server"]


