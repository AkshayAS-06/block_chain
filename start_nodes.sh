#!/bin/bash
echo "Starting Blockchain P2P Network..."
python node.py -p 5001 &
sleep 2
python node.py -p 5002 &
sleep 2
python node.py -p 5003 &
echo "All nodes started!"
