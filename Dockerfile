FROM python:3.12-bookworm as python

WORKDIR /src

ENV PIP_ROOT_USER_ACTION=ignore
ENV TERM xterm-256color

COPY . .

# This RUN command performs several operations to set up the Docker image:
# 1. Copies the docker-entrypoint.sh script from the /src/docker/ directory to the /usr/bin/ directory in the Docker image.
# 2. Changes the permissions of the docker-entrypoint.sh script to make it executable.
# 3. Retrieves the name of the current Git branch and writes it to a file named harvest.branch.
# 4. Retrieves the short SHA of the current Git commit and writes it to a file named harvest.commit.
# 5. Removes the .git directory from the /src/ directory in the Docker image to save space.
# 6. Creates a new Python virtual environment in the /venv directory.
# 7. Activates the Python virtual environment that was just created.
# 8. Upgrades pip, the Python package installer, to the latest version.
# 9. Installs the setuptools package, which is a collection of enhancements to the Python distutils.
# 10. Installs the Python packages listed in the requirements.txt file.
# 11. Runs unit tests in the /src/tests/ directory.
# 12. Changes the permissions of the /venv directory and all its contents to 777, which means the user, group,
#     and others can read, write, and execute files in the directory. This allows plugins to be installed by the user
#     running the Docker container.
RUN /bin/bash -c " \
        cp -v /src/docker/docker-entrypoint.sh /usr/bin/docker-entrypoint.sh \
        && chmod +x /usr/bin/docker-entrypoint.sh \
        && git rev-parse --abbrev-ref HEAD > harvest.branch \
        && git rev-parse --short HEAD > harvest.commit \
        && rm -rf /src/.git \
        && python -m venv /venv \
        && source /venv/bin/activate \
        && pip install --upgrade pip \
        && pip install setuptools \
        && pip install -r requirements.txt \
        && python -m unittest discover --verbose -s /src/tests/ \
        && chmod -R 777 /venv \
    "

# ENTRYPOINT must be supplied in this format or command line arguments will not be passed from launch.sh
# to the docker-entrypoint.sh script
ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
