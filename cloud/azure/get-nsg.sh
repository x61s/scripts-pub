#!/bin/bash

# Specify the resource group name
resource_group="RESOURCE_GROUP_NAME"

# Get a list of NSGs in the specified resource group
nsgs=$(az network nsg list --resource-group $resource_group --query '[].name' -o tsv)

# Iterate over each NSG and retrieve its network security rules
for nsg in $nsgs; do
	  echo
    echo ">>> Network Security Group: $nsg"
		az network nsg rule list --nsg-name $nsg --resource-group $resource_group --query '[].{Name:name, ResourceGroup:resourceGroup, Priority:priority, SourcePortRanges:sourcePortRange, SourceAddressPrefixes:sourceAddressPrefix, Access:access, Protocol:protocol, Direction:direction, DestinationPortRanges:destinationPortRange, DestinationAddressPrefixes:destinationAddressPrefix, Description:description}' --output table
    echo "-------------------------------------------------------"
		echo
done

