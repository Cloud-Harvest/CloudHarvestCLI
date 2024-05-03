# `cache collect` Command
Directs the API to begin data collection for the given [PSTAR](../conventions/pstar.md). Note that Harvest may belay data collection based on the available processing resources of the API.

# Usage
```
Usage: cache map [-h] [--platform PLATFORM] [--service SERVICE] [--type TYPE] [--account ACCOUNT] [--region REGION]

Optional Arguments:
  -h, --help           show this help message and exit

Pstar:
  --platform PLATFORM  Set the platform for the data. Example: `aws`
  --service SERVICE    Set the service name for the data. Example: `rds`
  --type TYPE          Set the service subtype for the data. Example: instance
  --account ACCOUNT    Set the platform account name for the data. Example: aws-business-development
  --region REGION      The account geographical region. Example: us-east-1
```

