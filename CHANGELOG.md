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
