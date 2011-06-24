#!/bin/sh
#Build BrazilFW Wellcome Screen
#by: Gustavo Lago - Feb/2008 fix: Washington Rodrigues Mar/2008

. /etc/coyote/coyote.conf

[ -z "$SSH_PORT" ] && SSH_PORT=22
[ -z "$WEBADMIN_PORT" ] && WEBADMIN_PORT=8180
[ -z "$ADMIN_AUTH" ] && MESSAGE="password not set yet, press [ENTER]"
CPUINFO1=$(grep "model name" /proc/cpuinfo | cut -f 2 -d ':' | uniq ; grep MHz /proc/cpuinfo | cut -f 2 -d ':' | uniq ; echo "MHz" ; echo "(`grep -ci "model name" /proc/cpuinfo` x)")
SRP_INFO=`echo CPU:[1m$CPUINFO1 [0m/ Memory:[1m\`grep "MemTotal" /proc/meminfo |cut -d: -f2\`[1m`
echo -ne "

SmartRouter Project

Version: [1m`cat /var/lib/lrpkg/root.version`[0m  
Local IP Address: [1m$LOCAL_IPADDR[0m

This software is licensed by GPL 2.


`echo $SRP_INFO | sed 's/[ ]\+/ /g'`







[0mTo remotely access this router use an SSH client to connect on port [1m$SSH_PORT[0m
Access the SmartRouter Web Admin by using the URL: [1mhttp://$LOCAL_IPADDR:$WEBADMIN_PORT

            [0;34mSmartRouter Official Website: [1;34mhttp://www.smartrouter.com.br[0m
                           [0mSmartRouter login is: [0;32mroot 
                    [0;31m $MESSAGE  [0m

" > /etc/issue
