#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state
if [ -f /etc/dhcpc/$IF_INET.info ] ; then
  . /etc/dhcpc/$IF_INET.info
  eval `ipcalc -m $dhcp_ip/$dhcp_mask`
fi

#Environment variables
VERSION=`cat /var/lib/lrpkg/root.version`
[ `uname -rv | awk '{print $3}'` = "SMP" ] && KERNEL=`uname -rv | awk '{print $1 "-" $3}'` || KERNEL=`uname -r`
HOST=`hostname`
NOW=`date`
UPTIME=`uptime | cut -b 14-100 | cut -f 1 -d ','`

LOAD=`cat /proc/loadavg`
LAST1=`echo $LOAD | cut -f 1 -d ' '`
LAST5=`echo $LOAD | cut -f 2 -d ' '`
LAST15=`echo $LOAD | cut -f 3 -d ' '`
MEMTOTAL=`free | grep Mem | awk '{print $2}'`
MEMUSED=`free | grep Mem | awk '{print $3}'`
MEMFREE=`free | grep Mem | awk '{print $4}'`
PERCUSED=$((MEMUSED*100/MEMTOTAL))
PERCFREE=$((100-$PERCUSED))

#STATUS NETWORK AND MORE
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
[ "$INET_UP" = "UP" ] && LINET_UP=$Abm
[ "$INET_UP" = "DOWN" ] && LINET_UP=$Abn
[ "$INET_UP" = "READY" ] && LINET_UP=$Abo
[ "$INET2_UP" = "UP" ] && LINET2_UP=$Abm
[ "$INET2_UP" = "DOWN" ] && LINET2_UP=$Abn
[ "$INET2_UP" = "READY" ] && LINET2_UP=$Abo
[ "$INET3_UP" = "UP" ] && LINET3_UP=$Abm
[ "$INET3_UP" = "DOWN" ] && LINET3_UP=$Abn
[ "$INET3_UP" = "READY" ] && LINET3_UP=$Abo
[ "$INET4_UP" = "UP" ] && LINET4_UP=$Abm
[ "$INET4_UP" = "DOWN" ] && LINET4_UP=$Abn
[ "$INET4_UP" = "READY" ] && LINET4_UP=$Abo
[ "$LOCAL_UP" = "UP" ] && LLOCAL_UP=$Abm
[ "$LOCAL_UP" = "DOWN" ] && LLOCAL_UP=$Abn
[ "$LOCAL_UP" = "READY" ] && LLOCAL_UP=$Abo
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

header_table() {
 echo "   <tr>"
 for argnum in $(seq 1 $#); do
	eval $(echo "vargs=\$$argnum")
	header_name="$(echo "$vargs" | cut -f1 -d",")"
	echo "      <td class=\"header\">$header_name</td>"
 done
echo "   </tr>"
}

get_color() {
 case "$1" in
	"$Abm")	echo "Green";;
	"$Ptb")	echo "Green";;
	"$Ptc")	echo "Red";;
	"$Abn")	echo "Red";;
	"$Abj")	echo "Green";;
	"$Abk")	echo "Red";;
	*)	echo "";;
 esac
}

output_line() {
 [ "$COLOR" = "row8" -o "$COLOR" = "" ] && COLOR="row6" || COLOR="row8"
 echo "   <tr>"
 for argnum in $(seq 1 $#); do
	eval $(echo "items_value=\$$argnum")
	items_value="$(echo "$items_value")"
	 echo "      <td class=\"$COLOR\"><span id=`get_color $items_value`>$items_value</span></td>"
 done
echo "   </tr>"
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

PPPIP=`getifaddr ppp0`
[ "$INETTYPE" = "PPPOE" -o "$INETTYPE" = "PPP" ] && GW=`ifconfig ppp0 | grep P-t-P | cut -f3 -d: | cut -f1 -d" "` \
|| GW=`/usr/sbin/ip route show | grep default | cut -f 3 -d ' '`
/usr/sbin/ip.test -i > /dev/null 2> /dev/null
[ $? != 0 ] && IPSTATUS=$Ptc || IPSTATUS=$Ptb

#INIT MAIN

cl_header2 "SmartRouter - $MWE"

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
 add_info_item_form "CPU" "$(cpu_info)"
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
echo "<tr>
 <td rowspan=3 class=row1 align=right><b>$Amu</b></td>
 <td class=row1 align=right><b>$Abd</b></td>
 <td colspan=2 class=row2>$MEMTOTAL kb (100%)</td>
</tr>
<tr>
 <td class=row1 align=right><b>$Aus</b></td>
 <td colspan=2 class=row2>$MEMUSED kb ($PERCUSED%)</td>
</tr>
<tr>
 <td class=row1 align=right><b>$Afr</b></td>
 <td colspan=2 class=row2>$MEMFREE kb ($PERCFREE%)</td>
</tr>"

#WAN
case "$INETTYPE" in
 ETHERNET_STATIC)
  init_main_table
  add_title "$Ani" "5"
  header_table "Interface" "Nome" "Descrição" "$Ast" "$Aei" "GATEWAY"
  output_line "$IF_INET" "<b>WAN1</b>" "$Aei" "$LINET_UP" "$IPADDR / $NETMASK" "$GATEWAY [ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]"
 ;;
 ETHERNET_DHCP)
  init_main_table
  add_title "$Ani" "5"
  header_table "Interface" "Nome" "Descrição" "$Ast" "$Aei" "GATEWAY"
  output_line "$IF_INET" "$INTERNET_TYPE <b>WAN1</b>" "$LINET_UP" " $dhcp_ip / $dhcp_mask  [ <a href=diags.cgi?COMMAND=/usr/sbin/dhcp.release><u>$Abh</u></a> | <a href=diags.cgi?COMMAND=/usr/sbin/dhcp.renew><u>$Abi</u></a> ]" "$dhcp_router [ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]"
 ;;
 PPP*)
  init_main_table
  add_title "PPPoE" "6"
  header_table "Interface" "Nome" "Descrição" "$Ast" "$Aei" "GATEWAY" "$Acs" "$Act"
  output_line "$IF_INET" "<b>WAN1</b>" "$INTERNET_TYPE" "$LINET_UP" "$PPPIP [ <a href=dial-ppp.cgi><u>$Mdl</u></a> | <a href=hangup-ppp.cgi><u>$Mhg</u></a> ]" "$GW [ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]" "$CONNECTTIME" "$CONNECTSTRING"
  end_table
  echo "<br>"
  init_main_table
  add_title "$Ani" "5"
  header_table "Interface" "Nome" "Descrição" "$Ast" "$Aei" "GATEWAY"
 ;;
esac
 [ -n "$IPADDR2" ] && output_line "$IF_INET" "<b>WAN1</b>" "$And $Aei" "$LINET_UP" "$IPADDR2 / $NETMASK2" ""
 [ -n "$IPADDR3" ] && output_line "$IF_INET" "<b>WAN1</b>" "$Ard $Aei" "$LINET_UP" "$IPADDR3 / $NETMASK3" ""
 [ -n "$LINET2_UP" ] && output_line "$IF_INET2" "<b>WAN2</b>" "$Pua" "$LINET2_UP" "$INET2_IPADDR / $INET2_NETMASK" "$INET2_GATEWAY"
 [ -n "$LINET3_UP" ] && output_line "$IF_INET3" "<b>WAN3</b>" "$Pub" "$LINET3_UP" "$INET3_IPADDR / $INET3_NETMASK" "$INET3_GATEWAY"
 [ -n "$LINET4_UP" ] && output_line "$IF_INET4" "<b>WAN4</b>" "$Puc" "$LINET4_UP" "$INET4_IPADDR / $INET4_NETMASK" "$INET4_GATEWAY"
end_table
#DNS
if [ -e "/tmp/realdns1" ]; then
init_main_table
 add_title "$Adi - [ <a href=diags.cgi?COMMAND=/usr/sbin/dns.test><u>$Abg</u></a> ]" "4"
 header_table "$Apn" "$Asn" "$Atn"
 output_line "`cat /tmp/realdns1`" "`cat /tmp/realdns2`" "`cat /tmp/realdns3`"
end_table
fi
echo "<br>"

#LAN
init_main_table
 add_title "$Aln" "5"
 header_table "Interface" "Nome" "Descrição" "$Ast" "$Ali" 
 output_line "$IF_LOCAL" "<b>LAN1</b>" "$Ali" "$LLOCAL_UP" "$LOCAL_IPADDR / $LOCAL_NETMASK"
 [ -n "$LOCAL_IPADDR2" ] && output_line "$IF_LOCAL" "<b>LAN1</b>" "$And $Ali" "$LLOCAL_UP" "$LOCAL_IPADDR2 / $LOCAL_NETMASK2"
 [ -n "$LOCAL_IPADDR3" ] && output_line "$IF_LOCAL" "<b>LAN1</b>" "$Ard $Ali" "$LLOCAL_UP" "$LOCAL_IPADDR3 / $LOCAL_NETMASK3"
 [ -n "$LOCAL2_UP" ] && output_line "$IF_LOCAL2" "<b>LAN2</b>" "$Pua" "$LLOCAL2_UP" "$LOCAL2_IPADDR / $LOCAL2_NETMASK"
 [ -n "$LOCAL3_UP" ] && output_line "$IF_LOCAL3" "<b>LAN3</b>" "$Pub" "$LLOCAL3_UP" "$LOCAL3_IPADDR / $LOCAL3_NETMASK"
 [ -n "$LOCAL4_UP" ] && output_line "$IF_LOCAL4" "<b>LAN4</b>" "$Puc" "$LLOCAL4_UP" "$LOCAL4_IPADDR / $LOCAL4_NETMASK"
 [ -n "$WLAN_UP" ] && output_line "$IF_WLAN" "<b>WLAN</b>" "$Pud" "$LWLAN_UP" "$WLAN_IPADDR / $WLAN_NETMASK"
end_table

#DMZ
if [ -n "$DMZ_UP" ]; then
init_main_table
 add_title "$Adz" "4"
 header_table "Interface" "Nome" "$Ast" "$Ali" 
 output_line "$IF_DMZ" "<b>DMZ</b>" "$LDMZ_UP" "$DMZ_IPADDR / $DMZ_NETMASK"
 [ -n "$DMZ_IPADDR2" ] && output_line "$IF_DMZ" "<b>DMZ</b>" "$LDMZ_UP" "$DMZ_IPADDR2 / $DMZ_NETMASK2"
 [ -n "$DMZ_IPADDR3" ] && output_line "$IF_DMZ" "<b>DMZ</b>" "$LDMZ_UP" "$DMZ_IPADDR3 / $DMZ_NETMASK3"
end_table
fi

end_table

cl_footer2
