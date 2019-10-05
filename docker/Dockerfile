FROM python:3.6-slim-stretch

MAINTAINER GREG EZEMA

ENV        PYTHONUNBUFFERED 1

RUN        mkdir /var/app
WORKDIR    /var/app

RUN        apt-get update

COPY       manage.py /var/app/
COPY       requirements.txt /var/app/requirements.txt
RUN        pip install pip --upgrade
RUN        pip install -r /var/app/requirements.txt

COPY       stock_trade /var/app/stock_trade

EXPOSE     8001
CMD        ["/var/app/scripts/run_local.sh"]
