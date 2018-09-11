# verificatum docker demo

## Run localhost

First execute the following commands:

```bash
docker-compose build
docker-compose up
```

Then make the following request with curl or httpie

```bash
curl http://localhost:5000/api/start
# OR
http GET http://localhost:5000/api/start
```

## Run on server or on multiple servers

Check COMMANDS file.

## Disclaimer

***This implementation is meant as a prototype and should not
be directly used in real life applications.***
