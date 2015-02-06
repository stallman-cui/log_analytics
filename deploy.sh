#!/bin/bash

[ $EUID -ne 0 ] && echo 'root needed' && exit 1

git clone https://github.com/coreos/etcd.git
pushd
cd etcd
./build
cp ./bin/etcd /usr/bin
cp ./shell/init_etcd /etc/init.d/etcd
service etcd restart

#rm -rf etcd

popd
current_path="BASE_DIR=$(pwd)"
sed -i "s:BASE_DIR=:$current_path:" ./shell/init_analytics
cp ./shell/init_analytics /etc/init.d/analytics
service analytics restart

exit 0
