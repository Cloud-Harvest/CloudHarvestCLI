# Convention: PSTAR
_PSTAR_ is the name given to the five primary dimensions that are used to store data in the Harvest Cache. All data is stored and (where relevant) indexed along these five dimensions which are defined in the table below.

# Definitions
| Dimension | Example                    | Description                             |
|-----------|----------------------------|-----------------------------------------|
| Platform  | `aws`                      | The platform for the data.              |
| Service   | `rds`                      | The service name for the data.          |
| Type      | `instance`                 | The service subtype for the data.       |
| Account   | `aws-business-development` | The platform account name for the data. |
| Region    | `us-east-1`                | The account geographical region.        |

# Cache Construct
Most documents within the Harvest Cache contain the PSTAR construct, stored inside the `Harvest` key. 
Consider the following example from the `DMS` `describe_events` BOTO3 call.

```json
{
  "SourceIdentifier": "my-dms-instance",
  "SourceType": "replication-instance",
  "Message": "this is a test message",
  "EventCategories": [
    "test"
  ],
  "Date": "2024-04-06T00:00:00Z",
  "Harvest": {
    "Platform": "aws",
    "Service": "dms",
    "Type": "event",
    "Account": "aws-business-development",
    "Region": "us-east-1"
  }
}
```

Internally, information in the Harvest Cache is stored in separate collections following this format:
`platform.service.type` with information in each account and region sharing space within that collection. This allows us to generate reports for the majority of data stored in the Harvest Cache without resorting to `$lookup` commands which are expensive to execute.

