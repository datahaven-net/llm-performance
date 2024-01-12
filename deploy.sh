#!/bin/sh

git pull

make migrate

make collectstatic

touch ./etc/uwsgi/vassals/llm-performance.ini
