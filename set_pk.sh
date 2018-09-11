#! /bin/sh
cd /verificatum && vmnc -pkey -ini json -outi raw protInfo.xml pkjson publicKey && vmn -setpk publicKey
