#!/bin/bash

payload=$1
content=${2:-text/csv}

for record in `cat ${payload}`
do
    curl --data-binary ${record} -H "Content-Type: ${content}" -v http://localhost:8080/invocations
done
