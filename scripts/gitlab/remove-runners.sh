#!/bin/bash

if [ "$1" == "help" ]; then
	echo
	echo "$0 <status> <type> <id> <tag> <name>"
	echo
	echo "status: online|offline|paused|active"
	echo "type: projects|groups"
	echo "id: project or group integer id"
	echo "tag: one of the runner tags available, example: hostname-shell"
	echo "name: runner registration name, example: loadtest-shell"
	exit 0
fi

if [ -z "$1" ]; then
	echo "No runner status argument provided."
	echo "https://docs.gitlab.com/ee/api/runners.html"
	exit 1
fi

if [ -z "$2" ]; then
	echo "No projects/group selector provided."
	exit 1
fi

if [ -z "$3" ]; then
	echo "No runner group id argument provided."
	echo "https://docs.gitlab.com/ee/api/runners.html"
	exit 1
fi

if [ -z "$4" ]; then
	echo "WARNING: Tag is not provided."
	exit 1
fi

if [ -z "$5" ]; then
	echo "WARNING: Name is not provided. You can accidentally delete all available runners."
fi

if [ -z "$PAMTOKEN" ]; then
	echo "Empty PAMTOKEN environment variable."
	echo "https://gitlab.domain.com/-/profile/personal_access_tokens"
	exit 1
fi

echo "Extracting runner IDs to ./remove.list file"

curl -s --header "PRIVATE-TOKEN: $PAMTOKEN" "https://gitlab.domain.com/api/v4/$2/$3/runners?per_page=100&status=$1&tag_list=$4" | jq --arg desc $5 -r '.[] | select(.description==$desc) | .id' > remove.list

if ! [ -s remove.list ]
then
	echo "List is empty. Nothing to do!"
	exit 0
fi

read -r -p "Type yes if you are sure the runners must be removed from Gitlab. " response
if ! [[ "$response" =~ ^(yes)$ ]]
then
	echo "Negative answer. Nothing to do!"
    exit 0
fi

while read id; do
	echo "Removing $id"
	curl --request DELETE --header "PRIVATE-TOKEN: $PAMTOKEN" "https://gitlab.domain.com/api/v4/runners/$id"
done < remove.list

rm ./remove.list || true
