FROM python:3.13-bookworm AS python

# Install requirements for the Docker image
RUN apt-get update  \
    && apt-get install -y less \
    && apt-get autoremove -y \
    && apt-get clean -y

WORKDIR /src

ENV PIP_ROOT_USER_ACTION=ignore
ENV TERM xterm-256color

COPY . .

RUN /bin/bash -c " \
        cp -v /src/docker/docker-entrypoint.sh /usr/bin/docker-entrypoint.sh \
        && chmod +x /usr/bin/docker-entrypoint.sh \
        && git rev-parse --abbrev-ref HEAD > harvest.branch \
        && git rev-parse --short HEAD > harvest.commit \
        && rm -rf /src/.git \
        && python -m venv /venv \
        && source /venv/bin/activate \
        && pip install --upgrade pip \
        && pip install . \
        && python -m unittest discover --verbose -s /src/tests/ \
        && chmod -R 777 /venv \
    "

# ENTRYPOINT must be supplied in this format or command line arguments will not be passed from launch.sh
# to the docker-entrypoint.sh script
ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
