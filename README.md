# CLI Client
This module allows users to interface with the Harvest API. 

# Standalone Operation
The repository includes a [`docker/docker-compose.yaml`](docker) file. This file will deploy containers of the three main components of Cloud Harvest:
- [The API](https://github.com/Cloud-Harvest/api)
- [A Mongo Database](https://www.mongodb.com/)
- [This CLI](https://github.com/Cloud-Harvest/client-cli)

Container directories will be stored in `~/.harvest` which allows users to change configurations as needed.

You may need to build the API image first. [Follow the Build Instructions for steps to build to the API.](https://github.com/Cloud-Harvest/api/blob/main/README.md).

```bash
cd docker
$ docker compose up -d
[+] Running 2/2
 ✔ Container docker-mongo-1  Running                                                                                                               0.0s 
 ✔ Container docker-api-1    Started                                                 
```
