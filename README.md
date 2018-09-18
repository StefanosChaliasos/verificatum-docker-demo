# verificatum docker demo

## Run localhost

First execute the following commands:

```bash
cd server_image && docker build -t vrf-server-example . && \
cd ../mix_server_image && docker build -t vrf-mix-server . && \
cd ../
docker-compose build && docker-compose up
```

## Run on server or on multiple servers

Check COMMANDS file.

## Disclaimer

***This implementation is meant as a prototype and should not
be directly used in real life applications.***
