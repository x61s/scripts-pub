#!/bin/bash

svc=$1

if [[ -z "${svc}" ]]; then
    echo "Usage: $0 <service_name>"
    exit
fi

# iterate service name and check last character is hyphen
while read -n1 character; do
    last_character=${svc:0-1}
    if [[ ${last_character} == "-" ]]; then
        svc=${svc::-1}
    fi
done < <(echo -n ${svc})

echo "${svc}"
