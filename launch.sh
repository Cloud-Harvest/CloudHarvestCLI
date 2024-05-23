#!/bin/bash

# launch.sh
#
# This script is used to run a Docker container for the Cloud Harvest CLI.
# Please observe the --help section for more information on how to use this script.

# Initialize our own variables
image="fionajuneleathers/cloud-harvest-cli"
image_tag="latest"
unused_args=()

# Check for --help, --config, --image, and --tag flags
for arg in "$@"
do
    case $arg in
        --image)
        shift # Remove --image from processing
        image="$1"  # Assign the next argument as the image name
        shift # Remove the image name from processing
        ;;
        --tag)
        shift # Remove --tag from processing
        image_tag="$1"  # Assign the next argument as the image tag
        shift # Remove the image tag from processing
        ;;
        --help)
        echo "Cloud Harvest CLI Launcher"
        echo "Usage: ./launch.sh [--image image] [--tag image_tag] [--help]"
        echo ""
        echo "Options:"
        echo "--image image: Allows you to specify the Docker image name."
        echo "--tag image_tag: Allows you to specify the Docker image tag."
        echo "--help: Displays this help message and exits."
#        exit 0
        ;;
      *)
      unused_args+=("$1")
      shift # Remove the unused argument from processing
      ;;
    esac
done

install_path="$(dirname "$(readlink -f "$0")")"

cd "$install_path" || exit

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

docker run -it --rm \
  -e UID="$(id -u)" \
  -e GID="$(id -g) "\
  -e USER="$USER" \
  -e "TERM=xterm-256color" \
  -e "HARVEST_IMAGE=$image:$image_tag" \
  -v "$install_path/app/:/src/app/" \
  -v "$HOME:/root/host" \
  -v "$HOME/.ssh:/root/.ssh" \
  --privileged \
  --user "$(id -u):$(id -g)" \
  --workdir /src \
  "$image:$image_tag" ${unused_args[*]}
