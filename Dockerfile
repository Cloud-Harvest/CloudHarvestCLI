FROM python:3.12-bookworm as python

WORKDIR /src

ENV PIP_ROOT_USER_ACTION=ignore
ENV TERM xterm-256color

COPY . .

#RUN pip install setuptools \
#    && pip install -r requirements.txt

ENTRYPOINT /bin/bash