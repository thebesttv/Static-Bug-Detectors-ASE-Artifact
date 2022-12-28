#!/usr/bin/env bash

if docker ps -a | grep bugswarm >/dev/null ; then
    echo 'Removing all BugSwarm Docker containers...'
    docker rm -f $(docker ps -a | grep bugswarm | cut -d' ' -f1)
fi

if docker ps -a | grep datomassi/images:infer-jdk8 >/dev/null ; then
    echo 'Removing Infer Docker containers...'
    docker rm -f $(docker ps -a | grep datomassi/images:infer-jdk8 | cut -d' ' -f1)
fi
