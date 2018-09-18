#! /bin/sh

echo "Initialize mix server"
# Initialize mix server
cd /data  && python -m SimpleHTTPServer $PORT &> /dev/null & \
cd /scripts && \
    python initialize.py $SERVER $IP $PORT $PORT_A $PORT_B $HOSTNAME \
        $MIXSERVER_NAME && \
        jobs
