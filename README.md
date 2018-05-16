# Dash - personal dashboard



## Quickstart

Assuming you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed. 

Start development environment:
```
cd environments/dev
docker-compose up -d
```
(`-d` means run in background, if you omit it start a new terminal for the following.)

Start hacking in [/project](project/).

When done, take down containers with
```
docker-compose down
```

For more details see [environments/dev/README.md](environments/dev/README.md).


## Running on Raspberry Pi

Approximately (TODO check and try from scratch):

``apt-get install`` python3 and npm.

In ``dash/``:

```
pip install -r project/requirements/dev.txt
/usr/local/bin/gunicorn -w 2 -b 127.0.0.1:8000 --max-requests 1 --reload project.www:app
```

In ``dash/project/frontend/``:
```
npm install
npm run start
```

## License

Use any code in this repository as you please according to the [MIT License](LICENSE).
