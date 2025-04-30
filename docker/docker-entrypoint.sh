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
        echo "--rebuild: Deletes the entire contents of the './app' directory."
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
    rm -rf /src/app
fi

if [ ! -d "/src/app" ]; then
    echo "Creating app directory."
    mkdir -p "/src/app"
fi

echo "Harvest is starting!" \
&& source /venv/bin/activate \
&& touch -a /src/app/plugins.txt \
&& echo "Installing plugins..." \
&& pip install -q -r /src/app/plugins.txt > /dev/null 2>&1 \
&& echo "Here we go!" \
&& export PYTHONPATH=/src \
&& python /src/CloudHarvestCLI ${unused_args[*]}

echo "Goodbye!"
