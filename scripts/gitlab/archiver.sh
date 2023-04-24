#!/bin/bash

GITLAB=gitlab.domain.com

GROUPID=$1
TARGET=$2

if [[ -z "${TOKEN}" ]] || [[ -z "${GROUPID}" ]] || [[ -z "${TARGET}" ]]; then
  echo "Usage: TOKEN=<...> ./archiver.sh <gid> <dir>"
fi

if [[ -z "${TOKEN}" ]]; then
  echo "TOKEN environment variable is not set."
  exit;
fi

if [[ -z "${GROUPID}" ]]; then
  echo "GROUP ID is not set."
  exit;
fi

if [[ -z "${TARGET}" ]]; then
  echo "TARGET directory is not set."
  exit;
fi

mkdir -pv ${TARGET}

pushd ${TARGET}

# Get pages count from API and remove escaped sequences from grep results
pages_count=$(curl -s --head --header "PRIVATE-TOKEN: ${TOKEN}" "https://${GITLAB}/api/v4/groups/${GROUPID}/projects?include_subgroups=true&per_page=100" | grep "x-total-pages" | awk -F ' ' '{print $2}' | sed 's/[^0-9]//g');


echo "API responce has ${pages_count} pages with 100 items each."

counter=1

for page in $(seq 1 ${pages_count});
do
  printf -- '-%.0s' {1..10}; echo ""
  echo "Page ${page}"
  
  for id in $(curl -s --header "PRIVATE-TOKEN: ${TOKEN}" "https://${GITLAB}/api/v4/groups/${GROUPID}/projects?include_subgroups=true&per_page=100&page=${page}" | jq '.[] | .id' | tr -d '"');
  do
    
    echo
    echo "${counter}"
    echo "Processing ID ${id}"
    repo=$(curl -s --header "PRIVATE-TOKEN: ${TOKEN}" "https://${GITLAB}/api/v4/projects/${id}" | jq '. | .path_with_namespace + ":" + .name + ":" + (.archived|tostring)' | tr -d '"')
    
    path=$(echo ${repo// /_} | awk -F ':' '{print $1}')
    name=$(echo ${repo// /_} | awk -F ':' '{print $2}')
    archived=$(echo ${repo// /_} | awk -F ':' '{print $3}')
    
    if [[ $archived == "true" ]]; then
      path="_archived_/${path}"
    fi
  
    echo "${path} : ${name} : archived=${archived}"
    mkdir -pv ${path}
    
    curl -f --header "PRIVATE-TOKEN: ${TOKEN}" "https://${GITLAB}/api/v4/projects/${id}/repository/archive.zip" -o ${path}/${name}.zip
  
    counter=$((counter+1))
  
  done

done

popd
