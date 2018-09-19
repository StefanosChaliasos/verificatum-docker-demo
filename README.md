# verificatum docker demo

## Run localhost

```bash
docker-compose build && docker-compose up
```

## Build

```bash
cd server_image && docker build -t vrf-server-example . && \
cd ../mix_server_image && docker build -t vrf-mix-server . && cd ../
```

## Disclaimer

***This implementation is meant as a prototype and should not
be directly used in real life applications.***
