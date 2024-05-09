FROM python:3.12-bookworm as python

WORKDIR /src

ENV PIP_ROOT_USER_ACTION=ignore
ENV TERM xterm-256color

COPY . .

# TODO: add pytest tests/ to the RUN command
RUN pip install setuptools \
    && python -m pip install .

ENTRYPOINT python CloudHarvestCLI
