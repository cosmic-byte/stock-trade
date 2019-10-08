# Stock Trading API
A stock trading platform for users to browse company stocks, fund their accounts, buy and sell stocks.
## Setup and installation
Pull the github repo
```bash
$ git clone https://github.com/cosmic-byte/stock-trade.git
```

## Run without Docker

Create a virtual environment to store project's Python requirements
```bash
$ cd stock-trade
$ virtualenv venv --python=python3
$ source venv/bin/activate
```

Install python requirements
```bash
$ pip install requirements.txt
```

Create a postgres database
```bash
$ sudo -i -u postgres psql
$ create database stock_trade;
$ grant all PRIVILEGES on database stock_trade to postgres;

```

Run database migrations
```bash
$ python manage.py migrate
```

Now you can run the application

```bash
$ python manage.py runserver

```
Launch your browser and access the app with `localhost:8000`

Run tests
```bash
$ py.test -n 8  stock_trade/tests/

```

## Run with Docker (Development Environment)

Note: make sure docker and docker-compose is installed

```bash
$ sh docker/run_dev.sh
```
Confirm the docker containers are running using `docker ps`,
Launch your browser and access the app with `localhost:8001`


#### To run tests

```bash
$ docker exec -it stock-trade_api bash
$ ./scripts/test_local_backend.sh

```
