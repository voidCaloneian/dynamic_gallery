#!/usr/bin/env bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <timeout> [--strict]" >&2
    exit 1
fi

timeout="$1"
strict="$2"
url="http://localhost:8000/api/photos/"

echo "Waiting for ${url} to be available..."
start_time=$(date +%s)

while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" "${url}")
    echo "Response: ${response}"
    if [ -n "${response}" ]; then
        echo "${url} is available."
        break
    fi

    current_time=$(date +%s)
    elapsed=$(( current_time - start_time ))
    if [ "$elapsed" -ge "$timeout" ]; then
        echo "Timeout after ${timeout} seconds, ${url} still unavailable." >&2
        if [ "$strict" = "--strict" ]; then
            exit 1
        fi
        break
    fi
    sleep 1
done

shift $(( 1 + ($# > 1 ? 1 : 0) ))
exec "$@"
