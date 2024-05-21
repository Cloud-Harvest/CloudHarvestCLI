#!/bin/bash

# Initialize our own variables
harvest_config=0

# Check for --harvest-config flags
for arg in "$@"
do
    case $arg in
        --harvest-config)
        harvest_config=1
        shift # Remove --harvest-config from processing
        ;;
        *)
        shift # Remove generic argument from processing
        ;;
    esac
done

# Check if the app/harvest.json file exists or --harvest-config is provided
if [ ! -f "./app/harvest.json" ] || [ $harvest_config -eq 1 ]; then
    # If the file does not exist or --harvest-config is provided, start config.py using docker run
    docker run -it --rm harvest-api /bin/bash -c "python3 config.py"

    # Check the exit status of config.py
    if [ $? -ne 0 ]; then
        # If the exit status is not 0, abort the script
        echo "config.py exited with an error. Aborting."
        exit 1
    fi
fi

echo "Starting the API service"
UID=$(id -u) GID=$(id -g) docker compose up api
