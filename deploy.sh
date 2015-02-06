#!/bin/bash

[ $EUID -ne 0 ] && echo 'root needed' && exit 1

current_path="BASE_DIR=$(pwd)"
sed -i "s:BASE_DIR=.*:$current_path:g" ./shell/init_analytics
cp ./shell/init_analytics /etc/init.d/analytics
service analytics restart

exit 0
