#!/bin/bash

#[ $EUID -ne 0 ] && echo 'root needed' && exit 1
SSH_USER=mhgame

ECHO='printf "\r%s\n"'
E_LINE='printf "\r%s\n" ---------------------------------'

#1. install pip
$E_LINE '1. install pip'
which pip >> /dev/null
if [ $? -ne 0 ]; then
    $ECHO 'Please install "pip" frist' 
    apt-get -q=2 install python-pip
fi

#2. install python extension
$E_LINE '2. install python extension'
pip -q install PyYAML bson pycurl greenlet pymongo pyzmq gevent
[ $? -ne 0 ] && $ECHO 'install python extension failed' && exit 1

git clone https://github.com/jplana/python-etcd
if [ -e python-etcd ]; then
    cd python-etcd && python setup.py
    [ $? -ne 0] && $ECHO 'install python-etcd failed' && exit 1
    cd ..
    rm -rf python-etcd
fi

#3. install analytics service
$E_LINE '3. install analytics service'
current_path="BASE_DIR=$(pwd)"
sed -i "s:BASE_DIR=.*:$current_path:g" ./shell/init_analytics
cp ./shell/init_analytics /etc/init.d/analytics
chown $SSH_USER:$SSH_USER $(pwd) -R
service analytics start

exit 0
