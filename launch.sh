#!/bin/bash

# Initialize our own variables
with_mongo=0
harvest_config=0

# Check for --with-mongo, --harvest-config, --tag, --image and --help flags
for arg in "$@"
do
    case $arg in
        --harvest-config)
        harvest_config=1
        shift # Remove --harvest-config from processing
        ;;
        --tag)
        shift # Remove --tag from processing
        image_tag="$1"  # Assign the next argument as the image tag
        shift # Remove the image tag from processing
        ;;
        --image)
        shift # Remove --image from processing
        image_name="$1"  # Assign the next argument as the image name
        shift # Remove the image name from processing
        ;;
        --help)
        echo "Usage: ./launch.sh [--with-mongo] [--harvest-config] [--tag] [--image] [--help]"
        echo ""
        echo "Options:"
        echo "--harvest-config: Start config.py using docker run."
        echo "--tag: Specify the Docker image tag."
        echo "--image: Specify the Docker image name."
        echo "--help: Show this help message."
        exit 0
        ;;
        *)
        shift # Remove generic argument from processing
        ;;
    esac
done

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

echo "Starting the API service"
LOCAL_UID=$(id -u) \
&& LOCAL_GID=$(id -g) \
&& IMAGE_NAME=$image_name \
&& IMAGE_TAG=$image_tag \
&& docker compose up api
