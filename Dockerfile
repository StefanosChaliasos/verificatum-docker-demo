FROM ubuntu:16.04

ENV HOME /root

# UPDATE AND INSTALL DEPENDENCIES
RUN apt-get -y update && apt-get -y upgrade && apt-get -y dist-upgrade && \
    apt-get install -y gcc make cmake git m4 libgmp-dev openjdk-8-jdk wget
RUN apt-get -y update && apt-get install -y python \
    python-pip python-dev build-essential
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# DOWNLOAD VERIFICATUM
RUN wget https://www.verificatum.org/files/verificatum-vmn-full.tar.gz
RUN tar -xvf verificatum-vmn-full.tar.gz

# INSTALL VERIFICATUM
WORKDIR verificatum-vmn-full
RUN sed -i -- 's/sudo//g' Makefile
RUN make install
RUN vog -rndinit RandomDevice /dev/urandom

# COPY FILES AND CREATE DIRECTORIES
WORKDIR /
RUN mkdir api
RUN mkdir verificatum
COPY pkjson ciphertextsjson ciphertexts.json set_pk.sh run.sh create_prot_info.sh set_ciphertexts.sh /verificatum/
RUN chmod +x /verificatum/*.sh

# DEPLOY FLASK API
WORKDIR /
COPY app_central.py /api/
COPY app_mix_server.py /api/
COPY docker_initialize.sh post_prot_info.py initialize.py /
RUN chmod +x docker_initialize.sh
# Mix servers (only use it when create central node)
ENV MIX_SERVERS_ORIGINS localhost:5050,localhost:6000
# Central node
ENV CENTRAL_NODE false
ENV CENTRAL_NODE_IP localhost:5000
# Mix server specific ip and ports (flask, verificatum http, verificatum hint)
ENV IP localhost
ENV PORT 5000
ENV PORT_A 8041
ENV PORT_B 4041
# Mix server name
ENV MIXSERVER_NAME 01
# If you ran central node don't forget to pass params.json as docker volume
# run ... -v /path/to/params.json:/params.json ...
ENTRYPOINT ./docker_initialize.sh
