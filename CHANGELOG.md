# 0.3.0
- `report` command
  - Enabled filtering, sorting, and other command arguments on 
  - Improved the way remote task errors are displayed
  - Added timeout for long-running tasks
  - Fixed some API metadata interpretations
- Various import optimizations
- Moved `harvest.json` to `harvest.yaml`
- Removed `config.py`
- Implemented logging configuration
- Raw commands are now recorded in the log
- Added the `theme` command to change the color theme
- Added `HarvestConfiguration.update_config()` to update the local configuration and file
- Fixed an issue with `input_pick_choices()` where it did not populate the correct list of choices
- The `print_data()` function no longer appends the `record_index_keyname` when it is already present in the `keys` parameter
- Added the `plugin` command
- Cleaned up some old code
- Updated to CloudHarvestCorePluginManager 0.5.0

# 0.2.5
- Updated to conform with CloudHarvestCorePluginManager 0.2.4
- Updated to Python 3.13

# 0.2.4
- Cleaned up how API errors are written to the terminal
- The `report` command will now display result times rounded to 2 decimal places

# 0.2.3
- Update to conform with CloudHarvestCoreTasks 0.3.0

# 0.2.2
- Added missing `less` requirement to the Dockerfile
- Fixed an issue with `report --format csv`

# 0.2.1
- Added a `__register__.py` to capture definitions and instances.
- Cleaned up imports to use `__register__.py`
- Worked on improving responses from the api
- Updates to support the `--performance` report flag
- Made several improvements to the way data is printed in tables

# 0.2.0
- Updated to conform with CloudHarvestCorePluginManager 0.2.0
  - Added `_register__.py`
- Updated `config.py` to store plugins in `./app/plugins.txt`
- Added this CHANGELOG
- Replaced the `launch.sh` `--network` command with `--no-network` and logic which automatically detects the `cloud-harvest` network
