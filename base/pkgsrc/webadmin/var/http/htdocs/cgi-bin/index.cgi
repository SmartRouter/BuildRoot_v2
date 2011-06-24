#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state
if [ -f /etc/dhcpc/$IF_INET.info ] ; then
  . /etc/dhcpc/$IF_INET.info
  eval `ipcalc -m $dhcp_ip/$dhcp_mask`
fi

#Environment variables
VEL=`grep MHz /proc/cpuinfo | cut -f 2 -d ':' | uniq ; echo "GHz"`
VERSION=`cat /var/lib/lrpkg/root.version`
KERNEL=`uname -r`
MACHINE=$(grep "model name" /proc/cpuinfo | cut -f 2 -d ':' | uniq ; grep MHz /proc/cpuinfo | cut -f 2 -d ':' | uniq ; echo "MHz" ; echo "(`grep -ci "model name" /proc/cpuinfo` x)")
HOST=`hostname`
NOW=`date`
UPTIME=`uptime | cut -b 14-100 | cut -f 1 -d ','`
LOAD=`cat /proc/loadavg`
LAST1=`echo $LOAD | cut -f 1 -d ' '`
LAST5=`echo $LOAD | cut -f 2 -d ' '`
LAST15=`echo $LOAD | cut -f 3 -d ' '`
MEMTOTAL=`free | grep Mem | sed s/\ */#/g | cut -f 3 -d '#'`
MEMUSED=`free | grep Mem | sed s/\ */#/g | cut -f 4 -d '#'`
MEMFREE=`free | grep Mem | sed s/\ */#/g | cut -f 5 -d '#'`
PERCUSED=$((MEMUSED*100/MEMTOTAL))
PERCFREE=$((100-$PERCUSED))
#SECOND PART
if [ "$INETTYPE" = "ETHERNET_DHCP" ] ; then
 [ -e "/etc/dhcpc/$IF_INET.info" ] && . /etc/dhcpc/$IF_INET.info
fi
[ -z "$DOMAINNAME" -a -n "$dhcp_domain" ] && DOMAINNAME="$dhcp_domain"
[ -z "$DOMAINNAME" -a -n "$DHCPD_DOMAIN" ] && DOMAINNAME="$DHCPD_DOMAIN"
[ -z "$DOMAINNAME" ] && DOMAINNAME="localdomain"
DNSSTATUS=$Abk
[ "$USE_DNS_CACHE" = "YES" ] && DNSSTATUS=$Abj
DHCPSTATUS=$Abk
[ "$DHCPSERVER" = "YES" ] && DHCPSTATUS=$Abj
CRONSTATUS=$Abk
[ "$ENABLE_CRON" = "YES" ] && CRONSTATUS=$Abj
SSHSTATUS=$Abj
[ "$ENABLE_EXTERNAL_SSH" = "NO" ] && SSHSTATUS=$Abl
[ -z "$SSH_PORT" ] && SSH_PORT=22
WEBADMSTATUS=$Abj
[ "$ENABLE_WEBADMIN" = "NO" ] && WEBADMSTATUS=$Abk
[ -z "$WEBADMIN_PORT" ] && WEBADMIN_PORT=8180
[ "$INETTYPE" = "PPP" ] && INTERNET_TYPE="$Abp"
[ "$INETTYPE" = "PPPOE" ] && INTERNET_TYPE="$Abq"
[ "$INETTYPE" = "ETHERNET_STATIC" ] && INTERNET_TYPE="$Abr"
[ "$INETTYPE" = "ETHERNET_DHCP" ] && INTERNET_TYPE="$Abs"
[ "$LOCAL_UP" = "UP" ] && LLOCAL_UP=$Abm
[ "$LOCAL_UP" = "DOWN" ] && LLOCAL_UP=$Abn
[ "$LOCAL_UP" = "READY" ] && LLOCAL_UP=$Abo
[ "$INET_UP" = "UP" ] && LINET_UP=$Abm
[ "$INET_UP" = "DOWN" ] && LINET_UP=$Abn
[ "$INET_UP" = "READY" ] && LINET_UP=$Abo
[ "$DMZ_UP" = "UP" ] && LDMZ_UP=$Abm
[ "$DMZ_UP" = "DOWN" ] && LDMZ_UP=$Abn
[ "$DMZ_UP" = "READY" ] && LDMZ_UP=$Abo
[ "$LOCAL2_UP" = "UP" ] && LLOCAL2_UP=$Abm
[ "$LOCAL2_UP" = "DOWN" ] && LLOCAL2_UP=$Abn
[ "$LOCAL2_UP" = "READY" ] && LLOCAL2_UP=$Abo
[ "$LOCAL3_UP" = "UP" ] && LLOCAL3_UP=$Abm
[ "$LOCAL3_UP" = "DOWN" ] && LLOCAL3_UP=$Abn
[ "$LOCAL3_UP" = "READY" ] && LLOCAL3_UP=$Abo
[ "$LOCAL4_UP" = "UP" ] && LLOCAL4_UP=$Abm
[ "$LOCAL4_UP" = "DOWN" ] && LLOCAL4_UP=$Abn
[ "$LOCAL4_UP" = "READY" ] && LLOCAL4_UP=$Abo
[ "$WLAN_UP" = "UP" ] && LWLAN_UP=$Abm
[ "$WLAN_UP" = "DOWN" ] && LWLAN_UP=$Abn
[ "$WLAN_UP" = "READY" ] && LWLAN_UP=$Abo


cpu_info() {
CPUINFO="$(cat /proc/cpuinfo)"
CPUCOUNT=$(echo "$CPUINFO" | grep -ci "model name")
MODEL=$(echo "$CPUINFO" | grep "model name" | uniq | cut -f2 -d":" | sed s/@.*//g)
VELOCITY=$(echo "$CPUINFO" | grep "cpu MHz" | uniq | cut -f2 -d":" | awk '{iint=int($0);fra=$0-iint;if (fra >= .4) iint=iint+1;if (iint > 999) print (iint/1000)" GHz" ;else print iint" MHz" }')
echo $MODEL @ "($CPUCOUNT"x")" $VELOCITY
}

color() {
     case $1 in
          1) COLOR="008000";;
          2) COLOR="FF0000";;
          3) COLOR="00FF00";;
          4) COLOR="800000";;
          5) COLOR="008080";;
          6) COLOR="000080";;
          7) COLOR="FF69B4";;
          8) COLOR="0000FF";;
          *) COLOR="000000";;
     esac
     echo "#$COLOR"
}

create_cpu_graph() {
 /bin/rrdtool graph /var/http/htdocs/cgi-bin/graph/cpu/cpu.png -a PNG -t "$(cpu_info)" \
 -v "$Ala / $Amu %" -s -24hours -r -w 593 -h 180 --alt-autoscale-max -l 0 -u 100 -r \
 DEF:memory=/tmp/cpu.rrd:memory:AVERAGE \
 DEF:used=/tmp/cpu.rrd:use:AVERAGE \
 $(for x in $(seq 1 $(cat /proc/stat | grep "cpu[0-9]" | wc -l));do echo "DEF:cpu$x=/tmp/cpu.rrd:cpu$x:AVERAGE "; done) \
 CDEF:memo=memory \
 CDEF:mem_mb=used \
 $(for x in $(seq 1 $CPUCOUNT);do echo "CDEF:cpuvar$x=cpu$x "; done) \
 AREA:memo#D9D900:"$Amu" \
 GPRINT:mem_mb:MIN:"Min\: %8.2lf mb" \
 GPRINT:mem_mb:AVERAGE:"Average\: %8.2lf mb" \
 GPRINT:mem_mb:MAX:"Max\: %8.2lf mb" \
 GPRINT:mem_mb:LAST:"Current\: %8.2lf mb\n" \
 $(for x in $(seq 1 $(cat /proc/stat | grep "cpu[0-9]" | wc -l));do echo "LINE1:cpu$x$(color $x):cpu$x\n ";done) >/dev/null 2>&1 
}

list_language(){
IFS=#
 cat /var/language/langlist | while read CODLANG LANGUAGE ; do
 codlang="`echo $CODLANG | tr [A-Z] [a-z]`"
 [ -r /var/language/webadmin.${codlang} ] && echo "<option value=$CODLANG `[ "$LANGUAGE_WEBADMIN" = "$CODLANG" ] && echo selected`>$LANGUAGE</option>"
 done
IFS=":
 "
}

add_info_item_form(){
if [ -z $3 ];then
echo "<tr>
 <td width=50% colspan=2 class=row1 align=right><b>$1</b></td>
 <td width=50% colspan=2 class=row2>$2</td>
</tr>"
else
echo "<tr>
 <td colspan=2 class=row1 align=right><b>$1</b></td>
 <td width=25% class=row2><span id=`get_color $2`>$2</span></td>
 <td width=25% class=row2>$3</td>
</tr>"
fi
}

add_info_item_form_2(){
echo "<tr>
 <td colspan=2 class=row1 align=right><b>$1</b></td>
 <td width=25% class=row2>$2</td>
 <td width=25% class=row2>$3</td>
</tr>"
}

PPPIP=`getifaddr ppp0`
[ "$INETTYPE" = "PPPOE" -o "$INETTYPE" = "PPP" ] && GW=`ifconfig ppp0 | grep P-t-P | cut -f3 -d: | cut -f1 -d" "` \
|| GW=`/usr/sbin/ip route show | grep default | cut -f 3 -d ' '`
/usr/sbin/ip.test -i > /dev/null 2> /dev/null
[ $? != 0 ] && IPSTATUS=$Ptc || IPSTATUS=$Ptb

get_color() {
 case "$1" in
	"$Abm")	echo "Green";;
	"$Ptb")	echo "Green";;
	"$Ptc")	echo "Red";;
	"$Abn")	echo "Red";;
	"$Abj")	echo "Green";;
	"$Abk")	echo "Red";;
	*)		echo "Normal";;
 esac
}

#INIT MAIN

cl_header2 "SmartRouter - $MWE"
create_cpu_graph

if [ "$FORM_OKBTN" = "$Fsb" ]; then
 LANGUAGE_WEBADMIN=$FORM_LANGUAGE_WEBADMIN
 cl_rebuildconf
  echo "<center><div id=alerta><a href=index.cgi class=lnk><u>$Egj</u></a><br>
<a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br>"
fi

init_form
init_main_table
#GENERAL INFORMATION
 add_title "$Agi" "4"
 add_info_item_form "$Baj" "$(init_combobox \"LANGUAGE_WEBADMIN\") $(list_language) $(end_combobox) $(echo "<input type=submit value=\"$Fsb\" name=OKBTN>")"
 add_info_item_form "SmartRouter - $Avs" "$VERSION"
 add_info_item_form "$Ahs" "$HOST"
 add_info_item_form "$Adn" "$DOMAINNAME"
 add_info_item_form "$Pta" "$IPSTATUS" "[ <a href=\"diags.cgi?COMMAND=/usr/sbin/ip.test%20-w\"><u>$Ptd</u></a> ]"

#WAN - FIRST
add_title "$Ans - $Ani" "4"
case "$INETTYPE" in
 ETHERNET_STATIC)
 add_info_item_form "$Ast" "$LINET_UP"
 add_info_item_form "$Ait" "$INTERNET_TYPE"
 add_info_item_form "$Aei" "$IPADDR"
 [ -n "$IPADDR2" ] && add_info_item_form "$And $Aei" "$IPADDR2/$NETMASK2"
 [ -n "$IPADDR3" ] && add_info_item_form "$Ard $Aei" "$IPADDR3/$NETMASK3"
 add_info_item_form "$Anm" "$NETMASK"
 add_info_item_form_2 "$Agt" "$GATEWAY" "[ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]"
 ;;
 ETHERNET_DHCP)
 add_info_item_form "$Ast" "$LINET_UP" "[ <a href=diags.cgi?COMMAND=/usr/sbin/dhcp.release><u>$Abh</u></a> | <a href=diags.cgi?COMMAND=/usr/sbin/dhcp.renew><u>$Abi</u></a> ]"
 add_info_item_form "$Ait" "$INTERNET_TYPE"
  if [ -n "$dhcp_ip" ] ; then
  add_info_item_form "$Aei" "$dhcp_ip"
  add_info_item_form "$Anm" "$NETMASK"
  add_info_item_form_2 "$Agt" "$dhcp_router" "[ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]"
  fi
 ;;
  PPP*)
  add_info_item_form "$Ast" "$LINET_UP" "[ <a href=dial-ppp.cgi><u>$Mdl</u></a> | <a href=hangup-ppp.cgi><u>$Mhg</u></a> ]"
  add_info_item_form "$Ait" "$INTERNET_TYPE"
  add_info_item_form "$Aei" "$PPPIP"
 [ -n "$CONNECTTIME" ] && add_info_item_form "$Acs" "$CONNECTTIME"
 [ -n "$CONNECTSTRING" ] && add_info_item_form "$Act" "$CONNECTSTRING"
 [ -n "$GW" ] && add_info_item_form_2 "$Agt" "$GW" "[ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]"
 ;;
esac


#LAN - FIRST
add_title "$Ans - $Aln" "4"
 add_info_item_form "$Ast" "$LLOCAL_UP" "<a></a>"
 add_info_item_form "$Ali" "$LOCAL_IPADDR"
 add_info_item_form "$Anm" "$LOCAL_NETMASK"
[ -n "$LOCAL_IPADDR2" ] && add_info_item_form "$And $Ali" "$LOCAL_IPADDR2 / $LOCAL_NETMASK2"
[ -n "$LOCAL_IPADDR3" ] && add_info_item_form "$Ard $Ali" "$LOCAL_IPADDR3 / $LOCAL_NETMASK3"

#SECOND LAN
if [ -n "$LOCAL2_UP" ] ; then
add_title "$Ans - $Pua" "4"
 add_info_item_form "$Ast" "$LLOCAL2_UP" "<a></a>"
 add_info_item_form "LAN2 $Aip" "$LOCAL2_IPADDR"
 add_info_item_form "$Anm" "$LOCAL2_NETMASK"
fi
#THIRD LAN
if [ -n "$LOCAL3_UP" ] ; then
add_title "$Ans - $Pub" "4"
 add_info_item_form "$Ast" "$LLOCAL3_UP" "<a></a>"
 add_info_item_form "LAN3 $Aip" "$LOCAL3_IPADDR"
 add_info_item_form "$Anm" "$LOCAL3_NETMASK"
fi
#FOURTH LAN
if [ -n "$LOCAL4_UP" ] ; then
add_title "$Ans - $Puc" "4"
 add_info_item_form "$Ast" "$LLOCAL4_UP" "<a></a>"
 add_info_item_form "LAN4 $Aip" "$LOCAL4_IPADDR"
 add_info_item_form "$Anm" "$LOCAL4_NETMASK"
fi

#WLAN
if [ -n "$WLAN_UP" ] ; then
add_title "$Ans - $Pud" "4"
 add_info_item_form "$Ast" "$LWLAN_UP" "<a></a>"
 add_info_item_form "WLAN $Aip" "$WLAN_IPADDR"
 add_info_item_form "$Anm" "$WLAN_NETMASK"
fi
 
#DMZ
if [ -n "$DMZ_UP" ] ; then
add_title "$Ans - $Adz" "4"
 add_info_item_form "$Ast" "$LDMZ_UP" "<a></a>"
 add_info_item_form "DMZ $Aip" "$DMZ_IPADDR"
 add_info_item_form "$Anm" "$DMZ_NETMASK"
 [ -n "$DMZ_IPADDR2" ] && add_info_item_form "$And DMZ $Aip" "$DMZ_IPADDR2 / $DMZ_NETMASK2"
 [ -n "$DMZ_IPADDR3" ] && add_info_item_form "$Ard DMZ $Aip" "$DMZ_IPADDR3 / $DMZ_NETMASK3"
fi
 
#DNS
add_title "$Adi" "4"
[ -e "/tmp/realdns1" ] && add_info_item_form_2 "$Apn" "`cat /tmp/realdns1`" "[ <a href=diags.cgi?COMMAND=/usr/sbin/dns.test><u>$Abg</u></a> ]"
[ -e "/tmp/realdns2" ] && add_info_item_form "$Asn" "`cat /tmp/realdns2`"
[ -e "/tmp/realdns3" ] && add_info_item_form "$Atn" "`cat /tmp/realdns3`"

 #SYSTEM INFORMATION
add_title "$Asv" "4"
 add_info_item_form "$Adc" "$DNSSTATUS" "$([ "$DNSSTATUS" = "$Abj" ] && echo "[ <a href=diags.cgi?COMMAND=/etc/rc.d/rc.dnsmasq><u>$Fay</u></a> ]")<a></a>"
 add_info_item_form "$Ads" "$DHCPSTATUS" "$([ "$DHCPSTATUS" = "$Abj" ] && echo "[ <a href=diags.cgi?COMMAND=/etc/rc.d/rc.dnsmasq><u>$Fay</u></a> ]")<a></a>"
 add_info_item_form "$Ass" "$SSHSTATUS" "$([ "$SSHSTATUS" != "Disabled" ] && echo " ($Abe $SSH_PORT)")<a></a>"
 add_info_item_form "$Awa" "$WEBADMSTATUS" "$([ "$WEBADMSTATUS" = "$Abj" ] && echo " ($Abe $WEBADMIN_PORT)")<a></a>"
 add_info_item_form "$Msg" "$CRONSTATUS" "$([ "$CRONSTATUS" = "$Abj" ] && echo "[ <a href=diags.cgi?COMMAND=/usr/sbin/cron.reload><u>$Fay</u></a> ]")<a></a>"

#INFORMATIONS OF SYSTEM
add_title "$Asi" "4"
 add_info_item_form "$Akv" "$KERNEL"
 add_info_item_form "$Adt" "$NOW"
 add_info_item_form "$Aup" "$UPTIME"
 echo "<tr>
 <td rowspan=3 width=35% class=row1 align=right><b>$Ala</b></td>
 <td class=row1 align=right><b>$Abb</b></td>
 <td colspan=2 class=row2>$LAST1</td>
</tr>
<tr>
 <td class=row1 align=right><b>$Als 5 $Amn</b></td>
 <td colspan=2 class=row2>$LAST5</td>
</tr>
<tr>
 <td class=row1 align=right><b>$Als 15 $Amn</b></td>
 <td colspan=2 class=row2>$LAST15</td>
</tr>"
#echo "<tr>
# <td rowspan=3 class=row1 align=right><b>$Amu</b></td>
# <td class=row1 align=right><b>$Abd</b></td>
# <td colspan=2 class=row2>$MEMTOTAL kb (100%)</td>
#</tr>
#<tr>
# <td class=row1 align=right><b>$Aus</b></td>
# <td colspan=2 class=row2>$MEMUSED kb ($PERCUSED%)</td>
#</tr>
#<tr>
# <td class=row1 align=right><b>$Afr</b></td>
# <td colspan=2 class=row2>$MEMFREE kb ($PERCFREE%)</td>
#</tr>"
[ -e "graph/cpu/cpu.png" ] && echo "<tr><td width=\"100%\" colspan=4><div align=\"center\"><img src=\"/cgi-bin/graph/cpu/cpu.png\"></div></td></tr>"

end_table

cl_footer2
