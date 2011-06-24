#!/bin/sh
# Revision 27/07/2009 AdslWiFi añadiendo pruebas a 4 Ping's diferentes
# LS=0 - Link UP: Internet Conection is OK
# LS=1 - Link DOWN: IP Conection to the Gateway OK
# LS=2 - Link WAIT: Link Conection to the Gateway OK
# LS=3 - Link FAIL: Link Conection to the Gateway dead
# LS=4 - Link DESABLE

. /etc/coyote/coyote.conf
[ -z "$PING_IP" ] && PING_IP=192.58.128.30
[ -z "$PING_RETRY" ] && PING_RETRY=3
# Ping a www.google.com
[ -z "$PING_IP_2" ] && PING_IP_2=209.85.227.147
[ -z "$PING_RETRY_2" ] && PING_RETRY_2=3
# Ping a www.no-ip.com
[ -z "$PING_IP_3" ] && PING_IP_3=204.16.252.112
[ -z "$PING_RETRY_3" ] && PING_RETRY_3=3
# Ping a www.dyndns.com
[ -z "$PING_IP_4" ] && PING_IP_4=204.13.248.107
[ -z "$PING_RETRY_4" ] && PING_RETRY_4=3
TIME=50

PING="/usr/sbin/ping -U -Lq -Q 0x10 -c"
ARPING="/usr/bin/arping -c 1 -I"
ip="/usr/sbin/ip"

#==========
net_check() {
   [ "$INETTYPE" = "ETHERNET_DHCP" ] && return 0
 #1=IP 2=GTW 3=MSK
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
 loss=`$ARPING ${1} ${2} | grep "Received" | cut -d" " -f2`
 [ "$loss" = "0" ] && LS="3" || LS="2"
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
 
 # Voy cambiando el valor de PING_IP porque si hago IF's anidados no funciona
 # Primero hago un ping de 1 línea para saber el estado con la IP almacenada
 
 #echo "PING_IP_TEMP=$PING_IP_TEMP LS=$LS" >> /tmp/ping.txt
 $PING 1 -I ${1} ${PING_IP_TEMP} > /dev/null
 if [ "$LS" = "1" ]; then
    case $PING_IP_TEMP in
        $PING_IP)
            PING_IP=$PING_IP_2
            PING_RETRY=$PING_RETRY_2
            ;;
        $PING_IP_2)
            PING_IP=$PING_IP_3
            PING_RETRY=$PING_RETRY_3
            ;;
        $PING_IP_3)
            PING_IP=$PING_IP_4
            PING_RETRY=$PING_RETRY_4
            ;;
        $PING_IP_4)
            PING_IP=$PING_IP
            PING_RETRY=$PING_RETRY
            ;;
    esac
    PING_IP_TEMP=$PING_IP
 fi
 
 #Recupero valor ultimo utilizado por si no pasa por el case anterior
 PING_IP=$PING_IP_TEMP
 
 $PING 1 -I ${1} ${PING_IP} > /dev/null
 if [ $? = 0 ]; then
    LS="0"
    # Línea correcta, responde a ping.
 else
    $PING $PING_RETRY -I ${1} ${PING_IP} >> /dev/null
    [ $? = 0 ] && LS="0" || LS="1"
 fi
   
 # errors=`$PING $PING_RETRY -I ${1} ${PING_IP} | grep errors | cut -d" " -f6`
 # [ -z "$errors" -o "$errors" != "+3" ] && LS="0" || LS="1"
 
 # Retornamos el valor de LS
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
