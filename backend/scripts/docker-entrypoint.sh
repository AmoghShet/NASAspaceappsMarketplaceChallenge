#!/bin/sh
if [ ! -f .initialized ]; then
    echo "Initializing container"
    sh /scripts/font-config.sh
    touch .initialized
else
    echo "Already initialized"
fi
echo "Starting the server"
npm start