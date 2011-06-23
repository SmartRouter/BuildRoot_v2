#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state
if [ -f /etc/dhcpc/$IF_INET.info ] ; then
  . /etc/dhcpc/$IF_INET.info
  eval `ipcalc -m $dhcp_ip/$dhcp_mask`
fi
cl_header2 "BrazilFW - $MWE"
VERSION=`cat /var/lib/lrpkg/root.version`
KERNEL=`uname -r`
MACHINE=`cat /proc/cpuinfo | grep name | cut -f 2 -d ':'; cat /proc/cpuinfo | grep MHz | cut -f 2 -d ':'`
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

if [ "$FORM_OKBTN" = "$Fsb" ]; then
 LANGUAGE_WEBADMIN=$FORM_LANGUAGE_WEBADMIN
 cl_rebuildconf
 echo "<br><center><div id=back><a href=index.cgi class=links>$Egj</a><br></div>
 <br><div id=alerta><a href=backup.cgi class=links>$Wtl</a></div></center>"
else

cat << CLEOF
<form method="POST"><table class=maintable width=100%><tr><th colspan=4 align=center class=row1>$Agi</th></tr>

<tr><td width=50% colspan=2 class=row1 align=right><b>$Baj</b><br><small></small></td>
 <td width=50% colspan=2 class=row2><select name=LANGUAGE_WEBADMIN>
CLEOF
IFS=#
 cat /var/language/langlist | while read CODLANG LANGUAGE ; do
 codlang="`echo $CODLANG | tr [A-Z] [a-z]`"
 [ -r /var/language/webadmin.${codlang} ] && echo "<option value=$CODLANG `[ "$LANGUAGE_WEBADMIN" = "$CODLANG" ] && echo selected`>$LANGUAGE</option>"
 done
IFS=":
 "
cat << CLEOF
</select><input type=submit value="$Fsb" name=OKBTN></td></tr>
<tr><td width=50% colspan=2 class=row1 align=right><b>BrazilFW - $Avs</b></td>
<td width=50% colspan=2 class=row2>$VERSION</td></tr><tr><td colspan=2 class=row1 align=right><b>$Ahs</b></td><td colspan=2 class=row2>$HOST</td></tr>
<tr><td colspan=2 class=row1 align=right><b>$Adn</b></td><td colspan=2 class=row2>$DOMAINNAME</td>
<tr><td colspan=2 class=row1 align=right><b>$Pta</b></td>
<td class=row2 width=25%><span id=`get_color $IPSTATUS`>$IPSTATUS</span></td>
<td width=25% class=row2>[ <a href="diags.cgi?COMMAND=/usr/sbin/ip.test%20-w"><u>$Ptd</u></a> ]</td>
</tr><tr><th colspan=4>$Ans - $Ani</th></tr>
CLEOF
case "$INETTYPE" in
 ETHERNET_STATIC)
cat << CLEOF
 <tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>
 <td class=row2><span id=`get_color $LINET_UP`>$LINET_UP</span></td><td class=row2></td></tr>
 <tr><td colspan=2 class=row1 align=right><b>$Ait</b></td>
 <td colspan=2 class=row2>$INTERNET_TYPE</td></tr>
 <tr><td colspan=2 class=row1 align=right><b>$Aei</b></td>
 <td colspan=2 class=row2>$IPADDR</td></tr>
CLEOF
 if [ -n "$IPADDR2" ] ; then
	echo "<tr><td colspan=2 class=row1 align=right><b>$And $Aei</b></td>
	<td colspan=2 class=row2>$IPADDR2/$NETMASK2</td></tr>"
 fi
 if [ -n "$IPADDR3" ] ; then
	echo "<tr><td colspan=2 class=row1 align=right><b>$Ard $Aei</b></td>
	<td colspan=2 class=row2>$IPADDR3/$NETMASK3</td></tr>"
 fi
cat << CLEOF
 <tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
 <td colspan=2 class=row2>$NETMASK</td></tr>
 <tr><td colspan=2 class=row1 align=right><b>$Agt</b></td>
 <td width=25% class=row2>$GATEWAY</td>
 <td width=25% class=row2>[ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]</td></tr>
CLEOF
 ;;
 ETHERNET_DHCP)
cat << CLEOF
 <tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>
 <td width=25% class=row2><span id=`get_color $LINET_UP`>$LINET_UP</span></td>
 <td width=25% class=row2>[ <a href=diags.cgi?COMMAND=/usr/sbin/dhcp.release><u>$Abh</u></a>&nbsp; |&nbsp;
 <a href=diags.cgi?COMMAND=/usr/sbin/dhcp.renew><u>$Abi</u></a> ]</td></tr>
 <tr><td colspan=2 class=row1 align=right><b>$Ait</b></td>
 <td colspan=2 class=row2>$INTERNET_TYPE</td></tr>
CLEOF
  if [ -n "$dhcp_ip" ] ; then
cat << CLEOF
 <tr><td colspan=2 class=row1 align=right><b>$Aei</b></td>
 <td colspan=2 class=row2>$dhcp_ip</td>
 <tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
 <td colspan=2 class=row2>$NETMASK</td></tr>
 <tr><td colspan=2 class=row1 align=right><b>$Agt</b></td>
 <td width=25% class=row2>$dhcp_router</td>
 <td width=25% class=row2>[ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]</td></tr>
CLEOF
  fi
 ;;
  PPP*)
cat << CLEOF
 <tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>
 <td width=25% class=row2><span id=`get_color $LINET_UP`>$LINET_UP</span></td>
 <td width=25% class=row2>[ <a href=dial-ppp.cgi><u>$Mdl</u></a>&nbsp; |&nbsp;
 <a href=hangup-ppp.cgi><u>$Mhg</u></a> ]</td></tr>
 <tr><td colspan=2 class=row1 align=right><b>$Ait</b></td>
 <td colspan=2 class=row2>$INTERNET_TYPE</td></tr>
 <tr><td colspan=2 class=row1 align=right><b>$Aei</b></td>
 <td colspan=2 class=row2>$PPPIP</td></tr>
CLEOF
 [ -n "$CONNECTTIME" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Acs</b></td> \
	<td colspan=2 class=row2>$CONNECTTIME</td></tr>"
 [ -n "$CONNECTSTRING" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Act</b></td> \
	<td colspan=2 class=row2>$CONNECTSTRING</td></tr>"
 [ -n "$GW" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Agt</b></td> \
	<td width=25% class=row2>$GW</td> \
	<td width=25% class=row2>[ <a href=diags.cgi?COMMAND=/usr/sbin/gateway.test><u>$Abf</u></a> ]</td></tr>"
 ;;
esac
echo "<tr><th colspan=4>$Ans - $Aln</th></tr>"
echo "<tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>"
echo "<td class=row2><span id=`get_color $LLOCAL_UP`>$LLOCAL_UP</span></td><td class=row2></td></tr>"
echo "<tr><td colspan=2 class=row1 align=right><b>$Ali</b></td>"
echo "<td colspan=2 class=row2>$LOCAL_IPADDR</td></tr>"
[ -n "$LOCAL_IPADDR2" ] &&  echo "<tr><td colspan=2 class=row1 align=right><b>$And $Ali</b></td> \
 <td colspan=2 class=row2>$LOCAL_IPADDR2 / $LOCAL_NETMASK2</td></tr>"
[ -n "$LOCAL_IPADDR3" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Ard $Ali</b></td> \
 <td colspan=2 class=row2>$LOCAL_IPADDR3 / $LOCAL_NETMASK3</td></tr>"
echo "<tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
 <td colspan=2 class=row2>$LOCAL_NETMASK</td></tr>"

if [ -n "$LOCAL2_UP" ] ; then
  echo "<tr><th colspan=4>$Ans - $Pua</th></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>"
  echo "<td class=row2><span id=`get_color $LLOCAL2_UP`>$LLOCAL2_UP</span></td><td class=row2></td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>LAN2 $Aip</b></td>"
  echo "<td colspan=2 class=row2>$LOCAL2_IPADDR</td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
  <td colspan=2 class=row2>$LOCAL2_NETMASK</td></tr>"
fi

if [ -n "$LOCAL3_UP" ] ; then
  echo "<tr><th colspan=4>$Ans - $Pub</th></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>"
  echo "<td class=row2><span id=`get_color $LLOCAL3_UP`>$LLOCAL3_UP</span></td><td class=row2></td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>LAN3 $Aip</b></td>"
  echo "<td colspan=2 class=row2>$LOCAL3_IPADDR</td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
  <td colspan=2 class=row2>$LOCAL3_NETMASK</td></tr>"
fi

if [ -n "$LOCAL4_UP" ] ; then
  echo "<tr><th colspan=4>$Ans - $Puc</th></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>"
  echo "<td class=row2><span id=`get_color $LLOCAL4_UP`>$LLOCAL4_UP</span></td><td class=row2></td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>LAN4 $Aip</b></td>"
  echo "<td colspan=2 class=row2>$LOCAL4_IPADDR</td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
  <td colspan=2 class=row2>$LOCAL4_NETMASK</td></tr>"
fi

if [ -n "$WLAN_UP" ] ; then
  echo "<tr><th colspan=4>$Ans - $Pud</th></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>"
  echo "<td class=row2><span id=`get_color $LWLAN_UP`>$LWLAN_UP</span></td><td class=row2></td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>WLAN $Aip</b></td>"
  echo "<td colspan=2 class=row2>$WLAN_IPADDR</td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
  <td colspan=2 class=row2>$WLAN_NETMASK</td></tr>"
fi

if [ -n "$DMZ_UP" ] ; then
  echo "<tr><th colspan=4>$Ans - $Adz</th></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Ast</b></td>"
  echo "<td class=row2><span id=`get_color $LDMZ_UP`>$LDMZ_UP</span></td><td class=row2></td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>DMZ $Aip</b></td>"
  echo "<td colspan=2 class=row2>$DMZ_IPADDR</td></tr>"
  [ -n "$DMZ_IPADDR2" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$And DMZ $Aip</b></td> \
	<td colspan=2 class=row2>$DMZ_IPADDR2 / $DMZ_NETMASK2</td></tr>"
  [ -n "$DMZ_IPADDR3" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Ard DMZ $Aip</b></td> \
	<td colspan=2 class=row2>$DMZ_IPADDR3 / $DMZ_NETMASK3</td></tr>"
  echo "<tr><td colspan=2 class=row1 align=right><b>$Anm</b></td>
  <td colspan=2 class=row2>$DMZ_NETMASK</td></tr>"
fi

echo "<tr><th colspan=4>$Adi</th></tr>"
[ -e "/tmp/realdns1" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Apn</b></td> \
 <td width=25% class=row2>`cat /tmp/realdns1`</td> \
 <td width=25% class=row2>[ <a href=diags.cgi?COMMAND=/usr/sbin/dns.test><u>$Abg</u></a> ]</td></tr>"
[ -e "/tmp/realdns2" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Asn</b></td> \
 <td colspan=2 class=row2>`cat /tmp/realdns2`</td></tr>"
[ -e "/tmp/realdns3" ] && echo "<tr><td colspan=2 class=row1 align=right><b>$Atn</b></td> \
 <td colspan=2 class=row2>`cat /tmp/realdns3`</td></tr>"

echo "<tr><th colspan=4>$Asv</th></tr>"
echo "<tr><td colspan=2 class=row1 align=right><b>$Adc</b></td>"
echo "<td width=25% class=row2><span id=`get_color $DNSSTATUS`>$DNSSTATUS</span></td>"
echo "<td width=25% class=row2>"
[ "$DNSSTATUS" = "$Abj" ] && echo "[ <a href=diags.cgi?COMMAND=/etc/rc.d/rc.dnsmasq><u>$Fay</u></a> ]"
echo "&nbsp;</td></tr>"

echo "<tr><td colspan=2 class=row1 align=right><b>$Ads</b></td>"
echo "<td width=25% class=row2><span id=`get_color $DHCPSTATUS`>$DHCPSTATUS</span></td>"
echo "<td width=25% class=row2>"
[ "$DHCPSTATUS" = "$Abj" ] && echo "[ <a href=diags.cgi?COMMAND=/etc/rc.d/rc.dnsmasq><u>$Fay</u></a> ]"
echo "&nbsp;</td></tr>"

echo "<tr><td colspan=2 class=row1 align=right><b>$Ass</b></td>"
echo "<td class=row2><span id=`get_color $SSHSTATUS`>$SSHSTATUS</span></td><td class=row2>"
[ "$SSHSTATUS" != "Disabled" ] && echo " ($Abe $SSH_PORT)"
echo "</td></tr>"

echo "<tr><td colspan=2 class=row1 align=right><b>$Awa</b></td>"
echo "<td class=row2><span id=`get_color $WEBADMSTATUS`>$WEBADMSTATUS</span></td><td class=row2>"
[ "$WEBADMSTATUS" = "$Abj" ] && echo " ($Abe $WEBADMIN_PORT)"
echo "</td></tr>"

echo "<tr><td colspan=2 class=row1 align=right><b>$Msg</b></td>"
echo "<td width=25% class=row2><span id=`get_color $CRONSTATUS`>$CRONSTATUS</span></td>"
echo "<td width=25% class=row2>"
[ "$CRONSTATUS" = "$Abj" ] && echo "[ <a href=diags.cgi?COMMAND=/usr/sbin/cron.reload><u>$Fay</u></a> ]"
echo "&nbsp;</td></tr>"

cat << CLEOF
<tr>
  <th colspan=4>$Asi</th>
</tr>   
<tr>
  <td colspan=2 class=row1 align=right><b>$Akv</b></td>
  <td colspan=2 class=row2>$KERNEL</td>
</tr>
<tr>
  <td colspan=2 class=row1 align=right><b>$Amc</b></td>
  <td colspan=2 class=row2>$MACHINE</td>
</tr>
<tr>
  <td colspan=2 class=row1 align=right><b>$Adt</b></td>
  <td colspan=2 class=row2>$NOW</td>
</tr>
<tr>
  <td colspan=2 class=row1 align=right><b>$Aup</b></td>
  <td colspan=2 class=row2>$UPTIME</td>
</tr>
<tr>
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
</tr>
<tr>
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
</tr>
</table></center>
CLEOF
fi
cl_footer2
