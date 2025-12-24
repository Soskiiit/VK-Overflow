#! /bin/bash

cleanup() {
    printf "\nStopping Gunicorn...\n"
    if [ -n "$GUNICORN_PID" ]; then
        kill $GUNICORN_PID
    fi
}

trap cleanup EXIT

echo "Starting Gunicorn..."
gunicorn -w 1 -b 127.0.0.1:8320 app:application > /dev/null 2>&1 &
GUNICORN_PID=$!

sleep 3


echo "All tests is transferring 100kb data"

printf "\nStatic with nginx\n"
ab -q -n 10000 -c 100 http://127.0.0.1:8088/static/test_file.txt | grep "Requests per"

printf "\nStatic with gunicorn\n"
ab -q -n 10000 -c 100 http://127.0.0.1:8320/static/test_file.txt | grep "Requests per"

printf "\nDynamic with gunicorn\n"
ab -q -n 10000 -c 100 http://127.0.0.1:8320/dynamic | grep "Requests per"

printf "\nDynamic trough proxy\n"
ab -q -n 10000 -c 100 http://127.0.0.1:8088/proxy/dynamic | grep "Requests per"

printf "\nDynamic trough proxy with cache\n"
ab -q -n 10000 -c 100 http://127.0.0.1:8088/cached/dynamic | grep "Requests per"
