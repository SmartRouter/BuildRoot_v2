#!/bin/sh

. /etc/coyote/coyote.conf
. /tmp/netsubsys.state
[ -z "$PING_IP" ] && PING_IP=72.14.205.103
[ -z "$PING_RETRY" ] && PING_RETRY=3
ping=/usr/sbin/ping
arping=/usr/bin/arping 
CHECK1=1
CHECK2=1
CHECK3=1
CHECK4=1

if [ "$INET_UP" = "UP" ] ; then
 if [ "$INETTYPE" = "PPP" -o "$INETTYPE" = "PPPOE" ] ; then
	IF_INET=ppp0
	IPADDR=`getifaddr $IF_INET`
	GATEWAY=`ifconfig ppp0 | grep P-t-P`
	GATEWAY=`echo $GATEWAY | cut -f 3 -d " "`
	GATEWAY=`echo $GATEWAY | cut -f 2 -d :`
 elif [ "$INETTYPE" = "ETHERNET_DHCP" ] ; then
	. /etc/dhcpc/$IF_INET.info
	IPADDR=$dhcp_ip
	GATEWAY=$dhcp_router
 fi
fi

check_ping() {
 if [ "$4" = "1" ]; then
	# if $OLD_CHECK=1 gateway conection is down
	# use arping to discovery new MAC
	# if no response exit with error
	# hardware error (cable, conection, power supply...
	# ... remote device no conection )
	loss=`$arping -c 1 -i $1 $3 | grep "Received" | cut -d" " -f2`
	[ "$loss" = "0" ] && return 1
 fi
 # fast test
 # if response exit without error
 # if no response retry ping with loss value
 # if loss value no exist or egual 100% exit with error
 $ping -c 1 -I $2 "$PING_IP" > /dev/null
 [ $? = 0 ] && return 0 || { loss=`ping -c $PING_RETRY -I $2 "$PING_IP" | grep received | cut -d" " -f6`;
 [ -z "$loss" -o "$loss" = "100%" ] && return 1 || return 0; }
}

flush_cache() {
 if [ "$LOAD_BALANCE" = "YES" ]; then
	COMMAND="ip ro add default table 222 proto static"
	[ $1 = 0 ] && COMMAND=$COMMAND" nexthop via $GATEWAY dev $IF_INET weight $INET_WEIGHT"
	[ $2 = 0 ] && COMMAND=$COMMAND" nexthop via $INET2_GATEWAY dev $IF_INET2 weight $INET2_WEIGHT"
	[ $3 = 0 ] && COMMAND=$COMMAND" nexthop via $INET3_GATEWAY dev $IF_INET3 weight $INET3_WEIGHT"
	[ $4 = 0 ] && COMMAND=$COMMAND" nexthop via $INET4_GATEWAY dev $IF_INET4 weight $INET4_WEIGHT"
	ip ro flush table 222
	ip ro flush cache
	$COMMAND
 fi
}

while [ /bin/true ]; do
 # reset SHIFT value
 # if exist INETx iface set OLD_CHECKx with CHECKx value
 # call check_ping with iface, ip addr, gateway and OLD_CHECK value
 # if return without error CHECKx=0
 # if return with error CHECKx=1
 # if CHECKx != OLD_CHECKx the link change the state
 SHIFT=0
 if [ ! -z $IF_INET ]; then
	OLD_CHECK1=$CHECK1
	check_ping $IF_INET $IPADDR $GATEWAY $OLD_CHECK1 && CHECK1=0 || CHECK1=1
	[ $CHECK1 != $OLD_CHECK1 ] && SHIFT=1
 fi
 if [ ! -z $IF_INET2 ]; then
	OLD_CHECK2=$CHECK2
	check_ping $IF_INET2 $INET2_IPADDR $INET2_GATEWAY $OLD_CHECK2 && CHECK2=0 || CHECK2=1
	[ $CHECK2 != $OLD_CHECK2 ] && SHIFT=1
 fi
 if [ ! -z $IF_INET3 ]; then
	OLD_CHECK3=$CHECK3
	check_ping $IF_INET3 $INET3_IPADDR $INET3_GATEWAY $OLD_CHECK3 && CHECK3=0 || CHECK3=1
	[ $CHECK3 != $OLD_CHECK3 ] && SHIFT=1
 fi
 if [ ! -z $IF_INET4 ]; then
	OLD_CHECK4=$CHECK4
	check_ping $IF_INET4 $INET4_IPADDR $INET4_GATEWAY $OLD_CHECK4 && CHECK4=0 || CHECK4=1
	[ $CHECK4 != $OLD_CHECK4 ] && SHIFT=1
 fi
 [ $SHIFT -gt 0 ] && flush_cache $CHECK1 $CHECK2 $CHECK3 $CHECK4
 sleep 50
done

