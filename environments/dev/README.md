# Development environment

Docker setup that creates

- nginx server on port 80
- flask + gunicorn app server on port 8000

## Get started

Assuming you have Docker installed, execute in this directory
```
docker-compose up
```

Browse to [localhost](http://localhost).


To get a shell in the app server, execute
```
docker-compose run flask-gunicorn bash
```


To force rebuild of images (for example if you change the python requirements)
```
docker-compose down
docker-compose build
```

If you only change docker-compose.yml, say for environment variables to app, restart with
```
docker compose down && docker-compose up
```

## Description

### App server

A python3 image that binds /src/project to the project folder on the host to allow hot-reloading of code.

pip installs requirements in project/requirements/dev.txt when image is built.

Runs gunicorn server serving flask app on start.

### Nginx

Listens on :80

Binds project/www/static to /www/static, and tries that first, if not found forwards to app server.

