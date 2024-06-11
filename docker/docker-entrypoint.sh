#!/bin/bash

# launch.sh
#
# This script is used to run a Docker container for the Cloud Harvest CLI.
# Please observe the --help section for more information on how to use this script.

# Initialize our own variables
config=0
help_requested=0
rebuild=0
version=0
unused_args=()
HARVEST_IMAGE=$HARVEST_IMAGE

# Check for --help, --config, --image, and --tag flags
for arg in "$@"
do
    case $arg in
        --rebuild)
        rebuild=1
        shift # Remove --rebuild from processing
        ;;
        --config)
        config=1
        shift # Remove --config from processing
        ;;
        --version)
        version=1
        shift # Remove --version from processing
        ;;
        --help)
        echo ""
        echo "Image Options:"
        echo "--image image: Allows you to specify the Docker image name."
        echo "--tag tag: Allows you to specify the Docker image tag."
        echo
        echo "Configuration:"
        echo "--config: Run the configuration script to create the harvest.json file."
        echo "--rebuild: Deletes the entire contents of the './app' directory. Implies --config."
        echo "--version: Prints the version, commit hash, and branch name then exits."
        help_requested=1
        ;;
      *)
      unused_args+=("$1")
      shift # Remove the unused argument from processing
      ;;
    esac
done

# Exit if --help was provided
if [ $help_requested -eq 1 ]; then
    exit 0
fi

# Being launching the container

# Display the image name
echo "Image $HARVEST_IMAGE"

# If --version was provided, print the version from /src/meta.json
if [ $version -eq 1 ]; then
    version_number=$(python -c "import json; print(json.load(open('/src/meta.json'))['version'])")
    commit_hash=$(cat /src/harvest.commit)
    branch_name=$(cat /src/harvest.branch)
    echo "CloudHarvestCLI v$version_number-$commit_hash($branch_name)"
    exit 0
fi

# Check if the --rebuild flag was provided; wipe the app directory if it was
if [ $rebuild -eq 1 ]; then
    rm -rf /src/appsource
    mkdir -p /src/app
fi

if [ ! -d "/src/app" ]; then
    echo "Creating app directory."
    mkdir -p "/src/app"
fi

# Check if the app/harvest.json file exists or --config is provided
if [ ! -f "/src/app/harvest.json" ] || [ $config -eq 1 ]; then
    # If the file does not exist or --config is provided, start config.py using docker run
    source /venv/bin/activate && python /src/config.py

    # Check the exit status of config.py
    if [ $? -ne 0 ]; then
        # If the exit status is not 0, abort the script
        echo "config.py exited with an error. Aborting."
        exit 1
    fi

    # If --config was provided, exit with a status code of 0
    if [ $config -eq 1 ] || [ $rebuild -eq 1 ]; then
        echo "You may now restart Harvest"
        exit 0
    fi
fi

echo "Harvest is starting!" \
&& source /venv/bin/activate \
&& touch -a /src/app/plugins.txt \
&& echo "Installing plugins..." \
&& pip install -q -r /src/app/plugins.txt > /dev/null 2>&1 \
&& echo "Here we go!" \
&& python /src/CloudHarvestCLI ${unused_args[*]}

echo "Goodbye!"
