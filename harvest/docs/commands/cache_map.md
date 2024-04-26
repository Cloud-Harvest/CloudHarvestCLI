# `cache map` Command
Generates a JSON map of the available data for the given [PSTAR](../conventions/pstar.md). This command is useful for understanding the available data and its structure.

Note that the `cache map` command will only compare based on the first 50 records. This is to prevent the command from taking too long to execute.

# Usage
```
Usage: cache map [-h] [--account ACCOUNT] [--region REGION] [--flatten FLATTEN] platform service type

Positional Arguments:
  platform           Set the platform for the data. Example: `aws`
  service            Set the service name for the data. Example: `rds`
  type               Set the service subtype for the data. Example: instance

Optional Arguments:
  -h, --help         show this help message and exit
  --account ACCOUNT  Set the platform account name for the data. Example: aws-business-development
  --region REGION    The account geographical region. Example: us-east-1
  --flatten FLATTEN  Flatten the data using the specified separator. Example: `.`
```

# Example
```
[harvest] cache map aws rds events
{
  "Date": "str",
  "EventCategories": [
    "str"
  ],
  "Harvest": {
    "Account": "str",
    "Active": "bool",
    "Dates": {
      "DeactivatedOn": "str",
      "LastSeen": "str"
    },
    "Module": {
      "FilterCriteria": [
        "str",
        "str",
        "str"
      ],
      "Name": "str",
      "Repository": "str",
      "Version": "str"
    },
    "Platform": "str",
    "Region": "str",
    "Service": "str",
    "Type": "str",
    "UniqueIdentifier": {
      "Harvest": {
        "Account": "str",
        "Region": "str"
      },
      "SourceIdentifier": "str"
    }
  },
  "Message": "str",
  "SourceArn": "str",
  "SourceIdentifier": "str",
  "SourceType": "str",
  "_id": "ObjectId"
}

Returned aws.rds.events in 0.026226 seconds.
```