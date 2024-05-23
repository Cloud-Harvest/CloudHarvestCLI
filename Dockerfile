FROM python:3.12-bookworm as python

WORKDIR /src

ENV PIP_ROOT_USER_ACTION=ignore
ENV TERM xterm-256color

COPY . .

RUN /bin/bash -c " \
        python -m venv /venv \
        && source /venv/bin/activate \
        && pip install --upgrade pip \
        && pip install setuptools \
        && pip install -r requirements.txt \
        && python -m unittest discover --verbose -s /src/tests/ \
        && chmod -R 777 /venv \
    "

ENTRYPOINT /bin/bash
