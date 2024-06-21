# Replace these variables with your storage account and container details
ACCOUNT_NAME=<your_storage_account_name>
ACCOUNT_KEY=<your_storage_account_key>
CONTAINER_NAME=<your_container_name>

# List all blobs and their sizes in the container
az storage blob list \
  --account-name $ACCOUNT_NAME \
  --account-key $ACCOUNT_KEY \
  --container-name $CONTAINER_NAME \
  --query "[].{Name:name, Size:properties.contentLength}" \
  --output tsv > blobsizes.tsv

# Calculate the total size in bytes
total_size=$(awk '{sum += $2} END {print sum}' blobsizes.tsv)

# Convert to gigabytes
total_size_gb=$(bc <<< "scale=3; $total_size/1024/1024/1024")

echo "Total size in bytes: $total_size"
echo "Total size in gigabytes: $total_size_gb"

