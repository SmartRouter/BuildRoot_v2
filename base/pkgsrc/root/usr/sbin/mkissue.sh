#!/bin/sh
#Build SmartRouter Wellcome Screen
#by: Gustavo Lago - Feb/2008 fix: Washington Rodrigues Mar/2008
#modified in 26/11/2010 --> naufragoweb

. /etc/coyote/coyote.conf

[ -z "$SSH_PORT" ] && SSH_PORT=22
[ -z "$WEBADMIN_PORT" ] && WEBADMIN_PORT=8180
[ -z "$ADMIN_AUTH" ] && MESSAGE="password not set yet, press [ENTER]"
CPU=`grep "model name" /proc/cpuinfo | cut -f 2 -d ':' | uniq`
VENDOR=`grep "vendor_id" /proc/cpuinfo | cut -f 2 -d ':' | uniq`
MEMTOTAL=`grep "MemTotal" /proc/meminfo | awk '{print$2$3}'`
MEMFREE=`grep "MemFree" /proc/meminfo | awk '{print$2$3}'`
SYSTIME=`uptime | awk '{print $3$4}' | sed 's/,\+ *$//g'`
VERSION=`cat /var/lib/lrpkg/root.version`
echo -ne "

SmartRouter Project

Version: [1m$VERSION[0m  
Local IP Address: [1m$LOCAL_IPADDR[0m

This software is licensed by GPL 2.

Processor Vendor = [1m$VENDOR[0m
CPU              = [1m$CPU[0m
Mem. Total       = [1m$MEMTOTAL[0m
Mem. Free        = [1m$MEMFREE[0m

Uptime: [1m$SYSTIME[0m

                                 

[0mTo remotely access this router use an SSH client to connect on port [1m$SSH_PORT[0m
Access the SmartRouter Web Admin by using the URL: [1mhttp://$LOCAL_IPADDR:$WEBADMIN_PORT

            [0;34mSmartRouter Official Website: [1;34mhttp://www.smartrouter.com.br[0m
                           [0mSmartRouter login is: [0;32mroot 
                    [0;31m $MESSAGE  [0m

" > /etc/issue
