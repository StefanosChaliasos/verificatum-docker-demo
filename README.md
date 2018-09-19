# verificatum docker demo

## Run localhost

```bash
docker-compose build && docker-compose up
```

## Run in server

* Server
```bash
docker pull schal/vrf-server-example
docker run -it --rm -p 5000:5000 \
-v /path/to/params.json:/data/params.json \
--name server schal/vrf-server-example
```

* Mix server
```bash
# Example with port 8000, port_a 8041, port_b 4041 and mixserver_name 01
docker pull schal/vrf-mix-server
docker run -it --rm -p 8000:8000 -p 8041:8041 -p 4041:4041 \
-e SERVER=<SERVER_IP>:5000 -e IP=<IP> \
-e PORT=8000 -e PORT_A=8041 -e PORT_B=4041 \
-e MIXSERVER_NAME=01 --name mix1 schal/vrf-mix-server
```

## Build

```bash
cd server_image && docker build -t vrf-server-example . && \
cd ../mix_server_image && docker build -t vrf-mix-server . && cd ../
```

## Disclaimer

***This implementation is meant as a prototype and should not
be directly used in real life applications.***
