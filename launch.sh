#!/bin/bash

# launch.sh
#
# This script template is the basis of the file we install as part of config.py
# which is used to run a Docker container for the Cloud Harvest CLI. When installed with config.py,
# this script is output as `harvest` in the root directory of the project.
#
# It provides several command line options to customize the execution of the Docker container.
#
# Usage:
# (./launch.sh | harvest) [--harvest-config] [--image IMAGE_NAME] [--tag IMAGE_TAG] [--help]
#
# Options:
# --harvest-config: This option triggers the execution of `config.py` script. If the `app/harvest.yaml` file does not exist or this option is provided, `config.py` is started.
# --image IMAGE_NAME: This option allows you to specify the Docker image name. Replace `IMAGE_NAME` with the name of your Docker image.
# --tag IMAGE_TAG: This option allows you to specify the Docker image tag. Replace `IMAGE_TAG` with the tag of your Docker image.
# --help: This option displays the help message and exits.
#
# Examples:
# To run the script with the default settings:
# ./harvest.template.sh
#
# To run the script with a specific Docker image name and tag:
# ./harvest.template.sh --image my_image --tag my_tag
#
# To display the help message:
# ./harvest.template.sh --help


# Initialize our own variables
harvest_config=0
image_name="cloud-harvest-cli"
image_tag="latest"

# Check for --help, --harvest-config, --image, and --tag flags
for arg in "$@"
do
    case $arg in
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
        --help)
        echo "Usage: (./harvest.template.sh | harvest) [--harvest-config] [--image] [--tag] [--help]"
        echo ""
        echo "Options:"
        echo "--harvest-config: Start config.py."
        echo "--image: Specify the Docker image name."
        echo "--tag: Specify the Docker image tag."
        echo "--help: Show this help message."
        exit 0
        ;;
        *)
        shift # Remove generic argument from processing
        ;;
    esac
done

install_path=$(realpath ".")


cd "$install_path" || exit

install_path=$(realpath ".")

cd "$install_path" || exit

# Check if the app/harvest.json file exists or --harvest-config is provided
if [ ! -f "./app/harvest.json" ] || [ $harvest_config -eq 1 ]; then
    # If the file does not exist or --harvest-config is provided, start config.py using docker run
    docker run -it --rm --entrypoint=/bin/bash -v "./app:/src/app" "$image_name:$image_tag" -c "python3 config.py"

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

docker run -it --rm \
  -e UID="$(id -u)" \
  -e GID="$(id -g) "\
  -e "TERM=xterm-256color" \
  -v "$HOME:/root/host" \
  -v "$HOME/.ssh:/root/.ssh" \
  -v "./app/:/src/app/" \
  --workdir /src \
  --user "$(id -u):$(id -g)" \
  --privileged \
  "$image_name:$image_tag"
