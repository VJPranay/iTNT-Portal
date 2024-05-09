#!/bin/bash

# Check if the mount point directory exists
if [ ! -d "/opt/portal/mediafiles" ]; then
    echo "Creating mount point directory..."
    sudo mkdir -p /opt/portal/mediafiles
fi

# Check if the NFS share is already mounted
if mount | grep -q "/opt/portal/mediafiles"; then
    echo "NFS share is already mounted."
else
    # Mount the NFS share
    echo "Mounting NFS share..."
    sudo mount -t nfs 10.236.204.105:/opt/portal/mediafiles /opt/portal/mediafiles
    if [ $? -eq 0 ]; then
        echo "NFS share mounted successfully."
    else
        echo "Failed to mount NFS share."
        exit 1
    fi
fi

# Verify the mount
echo "Verifying mount..."
df -h | grep "/opt/portal/mediafiles"

# Exit script
exit 0

