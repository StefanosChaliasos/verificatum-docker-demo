#! /bin/sh

if [ $CENTRAL_NODE = "true" ]; then
    echo "Initialize Central node"
    # Initialize mix server
    python initialize.py $CENTRAL_NODE $CENTRAL_NODE_IP $IP $PORT_A $PORT_B \
        $HOSTNAME $MIXSERVER_NAME
    cp /verificatum/localProtInfo.xml /verificatum/protInfo01.xml
    # Deploy API
    cd /api && python app_central.py
else
    echo "Initialize mix server"
    # Initialize mix server
    python initialize.py $CENTRAL_NODE $CENTRAL_NODE_IP $IP $PORT_A $PORT_B \
        $HOSTNAME $MIXSERVER_NAME
    # post protInfo.xml to central node
    cd /
    python post_prot_info.py $CENTRAL_NODE_IP && \
    # Deploy API
    cd /api && python app_mix_server.py
fi

