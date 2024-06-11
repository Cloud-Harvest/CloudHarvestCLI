#!/bin/bash

# launch.sh
#
# This script is used to run a Docker container for the Cloud Harvest CLI.
# Please observe the --help section for more information on how to use this script.

# Initialize our own variables
image="fionajuneleathers/cloud-harvest-cli"
image_tag="latest"
no_network=0
unused_args=()

# Process the arguments
while (( "$#" )); do
  case "$1" in
    --image)
      image="$2"
      shift 2
      ;;
    --no-network)
      no_network=1
      shift
      ;;
    --tag)
      image_tag="$2"
      shift 2
      ;;
    --help)
      echo "Cloud Harvest CLI Launcher"
      echo "Usage: ./launch.sh [--image image] [--tag image_tag] [--help]"
      echo ""
      echo "Docker Options:"
      echo "--image image: Allows you to specify the Docker image name."
      echo "--no-network: Disables the use of the 'harvest-network' Docker network."
      echo "--tag image_tag: Allows you to specify the Docker image tag."
      echo "--help: Displays this help message and exits."
      # DO NOT EXIT HERE: --help continues in docker/docker-entrypoint.sh
      # and will exit there.
      ;;
    *)
      echo "Unused argument: $1"
      unused_args+=("$1")
      shift
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

# Only include this option if the network exists and the user has not specified --no-network
network_option=""
if [ $no_network -eq 0 ]; then
  harvest_network_id="$(docker network ls | grep 'harvest-network' | awk '{print $1; exit}')"

  if [ -n "$harvest_network_id" ]; then
    echo "Using 'harvest-network' Docker network: $harvest_network_id"
    network_option="--network $harvest_network_id"

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
  $network_option \
  --user "$(id -u):$(id -g)" \
  --workdir /src \
  "$image:$image_tag" ${unused_args[*]}
