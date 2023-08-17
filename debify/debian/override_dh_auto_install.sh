#!/bin/bash

source debian/vars.sh

set -x

ls -d *

mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-nodejs18
cp -r ./* $DEB_INSTALL_ROOT/opt/cpanel/ea-nodejs18
cd $DEB_INSTALL_ROOT/opt/cpanel/ea-nodejs18
for file in `find . -type f -print | xargs grep -l '^#![ \t]*/usr/bin/env node'`
do
    echo "Changing Shebang (env) for" $file
    sed -i '1s:^#![ \t]*/usr/bin/env node:#!/opt/cpanel/ea-nodejs18/bin/node:' $file
done
mkdir -p $DEB_INSTALL_ROOT/etc/cpanel/ea4
echo -n /opt/cpanel/ea-nodejs18/bin/node > $DEB_INSTALL_ROOT/etc/cpanel/ea4/passenger.nodejs

# changes symlink targets so will get the symlinks to ../…/*.js
chmod 755 $DEB_INSTALL_ROOT/opt/cpanel/ea-nodejs18/bin/*
