#!/usr/bin/env bash

echo "killing old docker processes"
docker rmi $(docker images --filter dangling=true --quiet)
docker-compose rm -fs

echo "building docker containers"
docker-compose up --build -d
