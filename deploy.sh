#!/bin/bash

[ $EUID -ne 0 ] && echo 'root needed' && exit 1
SSH_USER=mhgame

current_path="BASE_DIR=$(pwd)"
sed -i "s:BASE_DIR=.*:$current_path:g" ./shell/init_analytics
cp ./shell/init_analytics /etc/init.d/analytics
chown $SSH_USER:$SSH_USER $(pwd) -R
service analytics start

exit 0
