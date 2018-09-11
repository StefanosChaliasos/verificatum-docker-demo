# verificatum docker demo

## Run localhost

First run the following commands:

```bash
docker-compose build
docker-compose up -it
```

Then make the following request with httpie (you could use curl as well)

```bash
http GET http://localhost:5000/api/start
```

## Run to a server or multiple servers

Check COMMANDS file.

## Disclaimer

***This implementation is meant as a prototype and should not be directly used in real life applications.***
