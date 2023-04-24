#!/bin/bash

# TOKEN=???
GITLAB=gitlab.domain.com
TARGET=/tmp


if [[ -z "${TOKEN}" ]]; then
  echo "TOKEN environment variable is not set!"
  exit;
fi

mkdir -pv ${TARGET}

pushd ${TARGET}

echo "Group IDs:"
printf -- '-%.0s' {1..10}; echo ""
echo "
111 group 1
112 group 2
113 group 3
"

read -p "Enter group id: " GROUPID

if [[ -z "${GROUPID}" ]]; then
  echo "GROUP ID is not set."
  exit;
fi

# Get pages count from API and remove escaped sequences from grep results
pages_count=$(curl -s --head --header "PRIVATE-TOKEN: ${TOKEN}" "https://${GITLAB}/api/v4/groups/${GROUPID}/projects?include_subgroups=true&per_page=100" | grep "x-total-pages" | awk -F ' ' '{print $2}' | sed 's/[^0-9]//g');


echo "API responce has ${pages_count} pages with 100 items each."

counter=1

for page in $(seq 1 ${pages_count});
do
  printf -- '-%.0s' {1..10}; echo ""
  echo "Page ${page}"
  
  for repo in $(curl -s --header "PRIVATE-TOKEN: ${TOKEN}" "https://${GITLAB}/api/v4/groups/${GROUPID}/projects?include_subgroups=true&per_page=100&page=${page}" | jq '.[] | .path_with_namespace + ":" + (.archived|tostring)' | tr -d '"');
  do
    echo "${counter}"
    counter=$((counter+1))
    
    path=$(echo ${repo// /_} | awk -F ':' '{print $1}')
    archived=$(echo ${repo// /_} | awk -F ':' '{print $2}')
    
    echo "${path} : archived=${archived}"
    
    if [[ $archived == "true" ]]; then
      prefix="_archived_"
    else
      prefix="."
    fi
    
    mkdir -pv ${path};
    git clone git@${GITLAB}:${path}.git ${prefix}/${path};

  done

done

popd
