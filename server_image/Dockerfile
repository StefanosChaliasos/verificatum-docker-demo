FROM ubuntu:16.04

ENV HOME /root

# UPDATE AND INSTALL DEPENDENCIES
RUN apt-get -y update && apt-get install -y python \
    python-pip python-dev build-essential
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir data

# DEPLOY FLASK API
WORKDIR /api
COPY app.py /api/
# Don't forget to pass params.json
# run ... -v /path/to/params.json:/data/params.json ...
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
