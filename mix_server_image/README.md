# Dummy Server For Verificatum Image

## Instructions

```bash
docker build -t vrf-mix-server .
docker run -it --rm -p 8041:8041 -p 4041:4041 -e \
    --name mixserver vrf-mix-server
