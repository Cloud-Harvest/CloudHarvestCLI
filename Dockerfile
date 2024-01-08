FROM python:3.12-bookworm as python

USER root

RUN apt-get update \
    && apt-get -y autoclean

WORKDIR /src

COPY . .

RUN pip install -r ./requirements.txt

ENTRYPOINT python harvest
