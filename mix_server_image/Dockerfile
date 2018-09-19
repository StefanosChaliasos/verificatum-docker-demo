FROM ubuntu:16.04

ENV HOME /root

# UPDATE AND INSTALL DEPENDENCIES
RUN apt-get -y update && apt-get -y upgrade && apt-get -y dist-upgrade && \
    apt-get install -y gcc make cmake git m4 libgmp-dev wget
RUN apt-get -y update && apt-get install -y python \
    python-pip python-dev build-essential
# RUN apt-get -u update && apt-get install -y ufw
# RUN apt-get -u update && apt-get install -y software-properties-common
# RUN add-apt-repository ppa:openjdk-r/ppa
RUN apt-get -y update && apt-get install -y openjdk-8-jdk

# DOWNLOAD VERIFICATUM
RUN wget https://www.verificatum.org/files/verificatum-vmn-full.tar.gz
RUN tar -xvf verificatum-vmn-full.tar.gz

# INSTALL VERIFICATUM
WORKDIR verificatum-vmn-full
RUN sed -i -- 's/sudo//g' Makefile
RUN make install
RUN vog -rndinit RandomDevice /dev/urandom

# INSTALL PYTHON DEPENDENCIES
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# COPY FILES AND CREATE DIRECTORIES
WORKDIR /
RUN mkdir verificatum
COPY scripts /scripts
COPY utils /scripts/utils
COPY docker_initialize.sh /
RUN chmod +x docker_initialize.sh
RUN mkdir data

# SET UP FIREWALL
# RUN ufw enable
# RUN ufw allow 'Nginx HTTP'

# Central node
ENV SERVER localhost:5000
# Mix server specific ip and ports (verificatum http, verificatum hint)
ENV IP localhost
ENV PORT 8000
ENV PORT_A 8041
ENV PORT_B 4041
# Mix server name
ENV MIXSERVER_NAME 01
ENTRYPOINT ./docker_initialize.sh
