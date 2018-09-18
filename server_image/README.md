# Dummy Server For Verificatum Image

## Instructions

```bash
docker build -t vrf-server-example .
docker run -it --rm -p 5000:5000 -v \
    /path/to/folder/test_data/params.json:/data/params.json
    --name server vrf-server-example
