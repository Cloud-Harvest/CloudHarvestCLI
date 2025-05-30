# `report` Command

The `report` command is used to generate reports generated by the API, leveraging the Harvest Cache. It accepts several arguments to customize the report output.

# Usage
```
Usage: report [-h] [-a ADD_KEYS [ADD_KEYS ...]] [-e EXCLUDE_KEYS [EXCLUDE_KEYS ...]] [-H HEADER_ORDER [HEADER_ORDER ...]] [-m MATCHES [MATCHES ...]]
              [--format {csv,json,pretty-json,table}] [--flatten FLATTEN] [--unflatten UNFLATTEN] [--page] [--refresh REFRESH] [--count] [--describe]
              [--limit LIMIT] [--sort [SORT ...]]
              report_name
```

# Arguments

| Command      | Example                                                        | Description                                                                                                                                                                                                                                                      |
|--------------|----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--count`    | `--count`                                                      | Returns the count of records, not the actual records in question. Note the return result will always be a key `result` with the value being the number of records found.                                                                                         |
| `--describe` | `--describe`                                                   | Returns the schema of the report, including its headers, in `pretty-json` format.                                                                                                                                                                                |
| `--limit`    | `--limit 10`                                                   | Limits the number of records returned.                                                                                                                                                                                                                           |
| `--sort`     | `--sort Field` or `--sort Field:desc` or `--sort A:desc B:asc` | Sorts the output by the specified field. Accepts `asc` (default) and `desc` sort orders using the `Field:Order` syntax. By default, records are sorted based on the headers defined by the report `--describe` _or_ user field orders provided with `--headers`  |

## Matching `-m`
This argument is used to match (or "filter") data in the report output. Each Match statement contains three important components: the field, the operator, and the value.

### Matching Syntax
The following basic examples demonstrate the three components to a match statement: the field, the operator, and the value.

| Syntax                          | Description                                                                                  |
|---------------------------------|----------------------------------------------------------------------------------------------|
| `-m Field=Value`                | Match the field `Field` with the value `Value`.                                              |
| `-m Field=Value Field=Value`    | Match the field `Field` with the value `Value` and the field `Field` with the value `Value`. |
| `-m Field=Value -m Field=Value` | Match the field `Field` with the value `Value` or the field `Field` with the value `Value`.  |


### Matching Operators
Harvest supports the following operators for matching. Pay special attention to the quotations around most of the operators. This is required whenever the operator is a symbol which may be [interpreted by `cmd2` for Output Redirection](https://cmd2.readthedocs.io/en/latest/features/redirection.html), such as `|`, `>`, and `<`. Although `cmd2` supports `allow_redirection=False`, we intentionally leave redirection on because this functionality is useful to Harvest users and (perhaps most relevantly) attempts to set this flag to `False` do not have the intended effect of allowing the use of these symbols in the `--matches` argument without the aid of quotations.

| Operator   | Description              | Example                      | Output                                                         | 
|------------|--------------------------|------------------------------|----------------------------------------------------------------|
| `==`       | Equal                    | `Field==Value`               | Records where the `Field` is exactly equal to `Value`          |
| `=`        | Regex Expression         | `"-m Field=^(some\|value)"`  | Records starting with `some` or `value` in the `Field` column. |
| `!=`       | Inverse Regex Expression | `"-m Field!=^(some\|value)"` | Records which do not contain `Value` in the `Field` column.    |
| `>`        | Greater than             | `"-m Field>Value"`           | Records where `Field` is greater than `Value`.                 | 
| `>=`, `=>` | Greater than or equal to | `"-m Field>=Value"`          | Records where `Field` is greater than or equal to `Value`.     |
| `<`        | Less than                | `"-m Field<Value"`           | Records where `Field` is less than `Value`.                    | 
| `<=`, `=<` | Less than or equal to    | `"-m Field<=Value"`          | Records where `Field` is less than or equal to `Value`.        |


>`-m`, `--matches`: Provide matching statements. Matches are defined in several ways. For example, `-m Field=Value` 
> just matches this field/value. One `-m` and multiple field/value pairs is an `AND`. Additional `-m` are an `OR`.

> For null value searches, provide the word 'null'. For example, `-m Field=null` will match all records where the field 
> is a null object. Regex keys (`=` and `!=`) are converted to empty strings. 

## Formatting `--format`

These arguments are used to set the command output format and manipulate the output data.

| Command       | Description                                                                                                                                            |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--format`    | Sets the command output format. Users can route output to files using `> path`. Available choices are `csv`, `json`, `pretty-json`, `table` (default). |
| `--flatten`   | Converts a nested JSON object into a one with a single key/value pair with fields separated by the character provided.                                 |
| `--unflatten` | Converts a flattened JSON object into a nested object based on the character provided.                                                                 |
| `--page`      | Output is halted when it fills the screen, similar to `less` or `more`.                                                                                |

## Key Manipulation
These arguments are used to manipulate the keys and headers in the report output.

| Command                | Example        | Description                                                                                                                                                                                                                                                                          |
|------------------------|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-a`, `--add-keys`     | `-a Key1 Key2` | Append keys to the report output.                                                                                                                                                                                                                                                    |
| `-e`, `--exclude-keys` | `-e Key3`      | Removes keys from the report output.                                                                                                                                                                                                                                                 |
| `-H`, `--header-order` | `-H Key1 Key2` | Changes the header order to the provided input. Fields not included are hidden as if the user removed them with `-e`. Note that this will also chain the sort order of the records, as records are automatically sorted based on header position _unless_ `--sort` is also provided. |

## Refresh
This argument is used to refresh the output every n seconds. Please be judicious when using this option.
- `--refresh`: Refresh the output n seconds.
