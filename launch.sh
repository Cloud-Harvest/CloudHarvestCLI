#!/bin/bash

# launch.sh
#
# This script is used to run a Docker container for the Cloud Harvest CLI.
# Please observe the --help section for more information on how to use this script.

# Initialize our own variables
harvest_config=0
image_name="fionajuneleathers/cloud-harvest-cli"
image_tag="latest"
rebuild=0
version=0

# Check for --help, --harvest-config, --image, and --tag flags
for arg in "$@"
do
    case $arg in
        --rebuild)
        rebuild=1
        shift # Remove --rebuild from processing
        ;;
        --harvest-config)
        harvest_config=1
        shift # Remove --harvest-config from processing
        ;;
        --image)
        shift # Remove --image from processing
        image_name="$1"  # Assign the next argument as the image name
        shift # Remove the image name from processing
        ;;
        --tag)
        shift # Remove --tag from processing
        image_tag="$1"  # Assign the next argument as the image tag
        shift # Remove the image tag from processing
        ;;
        --version)
        version=1
        shift # Remove --version from processing
        ;;
        --help)
        echo "Usage: ./launch.sh [--harvest-config] [--image IMAGE_NAME] [--tag IMAGE_TAG] [--rebuild] [--version] [--help]"
        echo ""
        echo "Options:"
        echo "--harvest-config: Triggers the execution of `config.py` script. If the `app/harvest.json` file does not exist or this option is provided, `config.py` is started."
        echo "--image IMAGE_NAME: Allows you to specify the Docker image name. Replace `IMAGE_NAME` with the name of your Docker image."
        echo "--tag IMAGE_TAG: Allows you to specify the Docker image tag. Replace `IMAGE_TAG` with the tag of your Docker image."
        echo "--rebuild: Deletes the entire contents of the `./app` directory."
        echo "--version: Prints the version, commit hash, and branch name from the Docker container's /src/meta.json file."
        echo "--help: Displays this help message and exits."
        exit 0
        ;;
    esac
done

install_path="$(dirname "$(readlink -f "$0")")"

cd "$install_path" || exit

# If --version was provided, print the version from /src/meta.json
if [ $version -eq 1 ]; then
    version_info=$(docker run --rm \
    --entrypoint=/bin/bash \
    "$image_name:$image_tag" \
    -c "version_number=\$(grep '\"version\"' /src/meta.json | cut -d '\"' -f 4 | tr -d '\n'); \
        commit_hash=\$(cd /src && git rev-parse --short HEAD); \
        branch_name=\$(cd /src && git rev-parse --abbrev-ref HEAD); \
        echo \"\$version_number-\$commit_hash(\$branch_name)\"")
    echo "CloudHarvestCLI v$version_info"
    exit 0
fi

if [ $rebuild -eq 1 ]; then
    echo "Rebuilding the app directory."
    rm -rf "$install_path/app/*"
fi

if [ ! -d "$install_path/app" ]; then
    echo "Creating app directory."
    mkdir -p "$install_path/app"
fi

# Check if the app/harvest.json file exists or --harvest-config is provided
if [ ! -f "$install_path/app/harvest.json" ] || [ $harvest_config -eq 1 ]; then
    # If the file does not exist or --harvest-config is provided, start config.py using docker run
    docker run -it --rm \
    -e UID="$(id -u)" \
    -e GID="$(id -g) "\
    -e USER="$USER" \
    -e "TERM=xterm-256color" \
    -v "$install_path/app/:/src/app/" \
    -v "/usr/local/bin:/src/usr-local-bin/" \
    --entrypoint=/bin/bash \
    "$image_name:$image_tag" \
    -c "
      if [ ! -f /src/app/venv/bin/activate ]; then
        echo 'Creating virtual environment.'
        python3 -m venv /src/app/venv &&
        source /src/app/venv/bin/activate &&
        pip install -q -r /src/requirements.txt
      fi &&
      source /src/app/venv/bin/activate &&
      python /src/config.py $*
    "

    # Check the exit status of config.py
    if [ $? -ne 0 ]; then
        # If the exit status is not 0, abort the script
        echo "config.py exited with an error. Aborting."
        exit 1
    fi

    # If --harvest-config was provided, exit with a status code of 0
    if [ $harvest_config -eq 1 ]; then
        echo "--harvest-config was specified. Exiting."
        exit 0
    fi
fi

# Check if the symlink exists and if it's not in the PATH
if [ ! -L "$install_path/harvest" ] && ! which harvest > /dev/null; then
    ln -s "$install_path/launch.sh" harvest

    if [ $? -ne 0 ]; then
        echo "Failed to create symlink to launch.sh"
        exit 1
    else
        echo "Created 'harvest' symlink at $install_path/harvest. Please add/move this to your PATH."
    fi
fi


echo "Launching Cloud Harvest CLI image $image_name:$image_tag"
docker run -it --rm \
  -e UID="$(id -u)" \
  -e GID="$(id -g) "\
  -e USER="$USER" \
  -e "TERM=xterm-256color" \
  -v "$install_path/app/:/src/app/" \
  -v "$HOME:/root/host" \
  -v "$HOME/.ssh:/root/.ssh" \
  --entrypoint=/bin/bash \
  --privileged \
  --user "$(id -u):$(id -g)" \
  --workdir /src \
  "$image_name:$image_tag" \
  -c "
    if [ ! -f /src/app/venv/bin/activate ]; then
      echo 'Creating virtual environment.'
      python3 -m venv /src/app/venv &&
      source /src/app/venv/bin/activate &&
      pip install -q -r /src/requirements.txt
    fi &&
    source /src/app/venv/bin/activate &&
    python /src/CloudHarvestCLI/__main__.py $* &&
    echo 'Goodbye!'
    "
