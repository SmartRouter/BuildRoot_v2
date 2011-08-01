#!/bin/sh
# LS=0 - Link UP: Internet Conection is OK
# LS=1 - Link DOWN: IP Conection to the Gateway OK
# LS=2 - Link WAIT: Link Conection to the Gateway OK
# LS=3 - Link FAIL: Link Conection to the Gateway dead
# LS=4 - Link DESABLE

. /etc/coyote/coyote.conf
[ -z "$PING_IP" ] && PING_IP=74.125.229.115
[ -z "$PING_RETRY" ] && PING_RETRY=3
TIME=50

PING="/bin/ping -q -c"
ARPING="/usr/bin/arping -q -c 1 -I"
ip="/usr/sbin/ip"

#==========
net_check() {
 #1=IP 2=GTW 3=MSK
 [ "$INETTYPE" = "ETHERNET_DHCP" ] && return 0
 eval `ipcalc -b -n $1 $3`
 IP_NET=$NETWORK
 IP_BRD=$BRODCAST
 eval `ipcalc -b -n $2 $3`
 GTW_NET=$NETWORK
 GTW_BRD=$BRODCAST
 [ ${IP_NET} = ${GTW_NET} -a ${IP_BRD} = ${GTW_BRD} ] && return 0 || return 1
}

#==========
arp_check() {
 # if Link Status is FAIL then use arping to discovery new MAC
 $ARPING ${1} ${2}
 [ $? = 0 ] && LS="1" || LS="2"
 return $LS
}

#==========
gtw_check() {
 # if Link Status is WAIT then use ping to the Gateway IP
 $PING 1 ${1} > /dev/null
 [ $? = 0 ] && LS="1" || LS="2"
 return $LS
}

#==========
ip_check() {
. /etc/coyote/coyote.conf
 # fast test: if response exit with UP status
 # if no response retry ping with loss value
 # if loss value no exist or egual 100% exit with DOWN status
 $PING 1 -I ${1} ${PING_IP} > /dev/null
 if [ $? = 0 ]; then
	LS="0"
 else
	$PING $PING_RETRY -I ${1} ${PING_IP} > /dev/null
	[ $? = 0 ] && LS="0" || LS="1"
 fi
 return $LS
}

#========== 
link_check() {
#1=IF 2=IP 3=GTW 4=OLD_LS
 local LS=$4
 if [ "$LS" = "3" ]; then
  arp_check $1 $3
  [ $? = 3 ] && LS="3" || LS="2"
 fi
 if [ "$LS" = "2" ]; then
  gtw_check $3
  if [ $? = 2 ]; then
   if [ $4 = 2 ]; then
    arp_check $1 $3
    [ $? = 3 ] && LS="3" || LS="2"
   elif [ $4 = 3 ]; then
    LS="2"
   fi
  else
   LS="1"
  fi
 fi
 if [ "$LS" = "1" ]; then
  [ $4 = 1 ] && $ip ro add via $3 dev $1 src $2 proto static
  ip_check $2
  if [ $? = 1 ]; then
   if [ $4 = 1 ]; then
    gtw_check $3
    [ $? = 2 ] && LS="2" || LS="1"
   elif [ $4 = 2 ]; then
    LS="1"
   fi
  else
   LS="0"
  fi
  [ $4 = 1 ] && $ip ro del via $3 dev $1 src $2 proto static
 fi
 if [ "$LS" = "0" ]; then
  ip_check $2
  [ $? = 0 ] && LS="0" || LS="1"
 fi
 return $LS
}

#==========
while [ /bin/true ]; do
 # reset SHIFT value
 # if exist INETx iface set OLD_LS var. with LS value
 # call link_check with iface, ip addr, gateway and OLD_LS value
 # if LS != OLD_LS then the state link change
 SHIFT=0
. /etc/coyote/coyote.conf
 for i in 1 2 3 4; do
  case $i in
   1)

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

    IF="$IF_INET"
    IP="$IPADDR"
    GTW="$GATEWAY"
    MSK="$NETMASK"
   ;;
   *)
    IF="$(eval "echo \${$(echo IF_INET$i)}")"
    IP="$(eval "echo \${$(echo INET${i}_IPADDR)}")"
    GTW="$(eval "echo \${$(echo INET${i}_GATEWAY)}")"
    MSK="$(eval "echo \${$(echo INET${i}_NETMASK)}")"
   ;;
  esac
  if [ ! -z "$IF" ]; then
   net_check $IP $GTW $MSK
   if [ $? = 0 ]; then
    [ -z $LS ] && LS=3
    [ -e /tmp/wan${i}.state ] && . /tmp/wan${i}.state
    OLD_LS=$LS
    link_check "$IF" "$IP" "$GTW" $OLD_LS
    LS=$?
    [ "$LS" -eq "0" -a "$OLD_LS" -ge "1" ] && SHIFT=1
    [ "$LS" -ge "1" -a "$OLD_LS" -eq "0" ] && SHIFT=1
   else
    LS=
   fi
   [ -n "$LS" ] && echo -n "LS=${LS}" > /tmp/wan${i}.state ||  echo -n "" > /tmp/wan${i}.state
  fi
 done
 [ $SHIFT -gt 0 ] && /etc/rc.d/rc.line_up
 IF=
 IP=
 GTW=
 sleep $TIME
done
