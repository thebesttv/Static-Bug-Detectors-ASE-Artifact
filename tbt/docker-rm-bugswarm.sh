#!/usr/bin/env bash

if docker ps -a | grep bugswarm >/dev/null ; then
    echo 'Removing all BugSwarm Docker containers...'
    docker rm -f $(docker ps -a | grep bugswarm | cut -d' ' -f1)
else
    echo 'No BugSwarm Docker container'
fi
