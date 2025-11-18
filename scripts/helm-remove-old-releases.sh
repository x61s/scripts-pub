#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="dev"
DAYS=7
CUTOFF=$(date -d "-${DAYS} days" +%s)
PREFIX="prefix-"

echo "Scanning for $PREFIX* releases older than ${DAYS} days in namespace: ${NAMESPACE}"
echo

# Phase 1: collect candidates
mapfile -t TO_DELETE < <(
  helm list -n "$NAMESPACE" -o json \
    | jq -c '.[]' \
    | while read -r item; do

        name=$(echo "$item" | jq -r '.name')
        updated=$(echo "$item" | jq -r '.updated')

        # Only $PREFIX* releases
        [[ "$name" != $PREFIX* ]] && continue

        # Normalize timestamp for GNU date:
        norm=$(echo "$updated" | sed -E 's/\.[0-9]+//; s/ UTC$//')

        epoch=$(date -d "$norm" +%s 2>/dev/null || echo 0)

        # Check age
        if [ "$epoch" -lt "$CUTOFF" ]; then
            echo "$name | $updated"
        fi

      done
)

COUNT=${#TO_DELETE[@]}

if (( COUNT == 0 )); then
    echo "No outdated $PREFIX* releases found."
    exit 0
fi

echo "Found $COUNT $PREFIX* releases to delete:"
printf '%s\n' "${TO_DELETE[@]}"
echo

# Optional: uncomment this if you want a manual confirmation
# read -rp "Continue with deletion? (yes/no): " answer
# [[ "$answer" != "yes" ]] && echo "Aborted." && exit 0

echo "Deleting $COUNT releases..."
echo

# Phase 2: deletion
for entry in "${TO_DELETE[@]}"; do
    name="${entry%% | *}"   # extract release name (before " | ")
    echo "Deleting: $name"
    helm uninstall "$name" -n "$NAMESPACE" --debug --dry-run
done

echo
echo "Done."

