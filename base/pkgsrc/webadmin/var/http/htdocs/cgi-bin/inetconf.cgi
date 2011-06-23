#!/bin/sh
# Revision by BFW user "marcos do vale" - 03/04/2008
# Build new cgi with ethernet, pppoe and ppp-conf.cgi

. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state

SCRIPT="inetconf.cgi"

mount_configuration() {
case $INETTYPE in
 "ETHERNET_DHCP")
	DHCPHOSTNAME=$FORM_DHCPHOSTNAME
	IPADDR=
	IPADDR2=
	IPADDR3=
	NETMASK=
	GATEWAY=
	MAC_SPOOFING=$FORM_MAC_SPOOFING
 ;;
 "ETHERNET_STATIC")
	IPADDR=$FORM_IPADDR
	IPADDR2=$FORM_IPADDR2
	IPADDR3=$FORM_IPADDR3
	NETMASK=$FORM_NETMASK
	NETMASK2=$FORM_NETMASK2
	NETMASK3=$FORM_NETMASK3
	GATEWAY=$FORM_GATEWAY
	MAC_SPOOFING=$FORM_MAC_SPOOFING
 ;;
 "PPPOE")
	[ "$FORM_DEMANDMODE" = "NO" ] && PPPOE_IDLE=NO || PPPOE_IDLE=$FORM_DEMANDTIME
	PPPOE_USERNAME=$FORM_USERNAME
	PPPOE_PASSWORD=$FORM_PASSWORD1
	IPADDR=
	IPADDR2=
	IPADDR3=
	NETMASK=
	GATEWAY=
	MAC_SPOOFING=
;;
 "PPP")
	[ "$FORM_DEMANDMODE" = "NO" ] && PPP_DEMANDDIAL=NO || PPP_DEMANDDIAL=$FORM_IDLETIME
	PPP_USERNAME=$FORM_USERNAME
	PPP_PASSWORD=$FORM_PASSWORD1
	PPP_CHATLOGIN=$FORM_CHATLOGIN
	PPP_PHONENUM=$FORM_PHONENUM
	PPP_INITSTR=$FORM_MODEMINIT
	PPP_MODEMTTY=$FORM_MODEMDEV
	PPP_PORTSPEED=$FORM_PORTSPEED
	[ "$FORM_STATIC" = "NO" ] && { PPP_STATICIP="NO";
	PPP_LOCALREMOTE=$FORM_LOCALREMOTE; } || \
	{ PPP_STATICIP=$FORM_STATICIP;
	PPP_LOCALREMOTE=; }
	PPP_CONFIG_OTF=YES
	[ -z "$PPP_USERNAME" -o -z "$PPP_PASSWORD" ] && echo "<center><div id=back>$Pmh<br><i>$Pmi</i></div></center><br>"
	[ -z "$PPP_PHONENUM" ] && echo "<center><div id=back>$Pmj<br><i>$Pmk</i></div></center><br>"
	[ -z "$PPP_MODEMTTY" ] && echo "<center><div id=back>$Pml<br><i>$Pmm</i></div></center><br>"
	[ -z "$PPP_LOCALREMOTE" ] && echo "<center><div id=back>$Pmn<br><i>$Pmo</i></div></center><br>"
esac
IF_INET2=$FORM_IF_INET2
INET2_IPADDR=$FORM_INET2_IPADDR
INET2_NETMASK=$FORM_INET2_NETMASK
INET2_GATEWAY=$FORM_INET2_GATEWAY
IF_INET3=$FORM_IF_INET3
INET3_IPADDR=$FORM_INET3_IPADDR
INET3_NETMASK=$FORM_INET3_NETMASK
INET3_GATEWAY=$FORM_INET3_GATEWAY
IF_INET4=$FORM_IF_INET4
INET4_IPADDR=$FORM_INET4_IPADDR
INET4_NETMASK=$FORM_INET4_NETMASK
INET4_GATEWAY=$FORM_INET4_GATEWAY
DOMAINNAME=$FORM_DOMAINNAME
DNS1=$FORM_DNS1
DNS2=$FORM_DNS2
DNS3=$FORM_DNS3
IF_INET=$FORM_IF_INET
cl_rebuildconf
echo "<center><div id=alerta>$Wsv<br><a href=backup.cgi class=links>$Wtl</a></div>
<br><div id=back><a href=$SCRIPT class=links>$Egj</a><br></div></center>"
}

show_() {
#for i in "ETHERNET_DHCP" "ETHERNET_STATIC" "PPPoE" "PPP"; do
cat << CLEOF
<form method="POST" action="$SCRIPT"><table class=maintable border=0 width="100%"><tr><th colspan=2>$Eia</th></tr>
<tr><td class=row1 align=right><b>$Icc</b><br><small></small></td>
 <td width=50% class=row2><select name=INETTYPE>
	<option value=ETHERNET_DHCP `[ "$INETTYPE" = "ETHERNET_DHCP" ] && echo selected`>DHCP</option>
	<option value=ETHERNET_STATIC `[ "$INETTYPE" = "ETHERNET_STATIC" ] && echo selected`>STATIC</option>
	<option value=PPPOE `[ "$INETTYPE" = "PPPOE" ] && echo selected`>PPPOE</option>
	<option value=PPP `[ "$INETTYPE" = "PPP" ] && echo selected`>PPP</option>
 </select><input type=submit value="$Fsb" name=OKBTN></td></tr>
 <tr><th colspan=2>$Ptk</th></tr>
CLEOF
 case $INETTYPE in
	ETHERNET_DHCP)
cat << CLEOF
<tr><td class=row1 align=right><b>$Psd</td>
 <td class=row2><input type=text name=IF_INET value="${IF_INET}" size=5></td></tr>
<tr><td class=row1 align=right>$Ema $Emb<br></td>
 <td class=row2><input type=text name=DHCPHOSTNAME value="${DHCPHOSTNAME}" size=20></center></td></tr>
<tr><td class=row1 align=right><b>$Efn</b><br>$Euo</td>
 <td class=row2><input type=text name=MAC_SPOOFING value="${MAC_SPOOFING}" size=20></td></tr>
CLEOF
	;;
	ETHERNET_STATIC)
cat << CLEOF
<tr><td class=row1 align=right><b>$Psd</td>
 <td class=row2><input type=text name=IF_INET value="${IF_INET}" size=5></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br>$Wed $Anm</b></td>
 <td class=row2><input type=text name=IPADDR value="${IPADDR}" size=20><br><input type=text name=NETMASK value="${NETMASK}" size=20></td></tr>
<tr><td class=row1 align=right><b>$Lpj<br>$Wed $Anm</b></td>
 <td class=row2><input type=text name=IPADDR2 value="${IPADDR2}" size=20><br><input type=text name=NETMASK2 value="${NETMASK2}" size=20></td></tr>
<tr><td class=row1 align=right><b>$Lpk<br>$Wed $Anm</b></td>
 <td class=row2><input type=text name=IPADDR3 value="${IPADDR3}" size=20><br><input type=text name=NETMASK3 value="${NETMASK3}" size=20></td></tr>
<tr><td class=row1 align=right><b>$Edg</b></td>
 <td class=row2><input type=text name=GATEWAY value="${GATEWAY}" size=20></td></tr>
<tr><td class=row1 align=right><b>$Efn</b><br>$Euo</td>
 <td class=row2><input type=text name=MAC_SPOOFING value="${MAC_SPOOFING}" size=20></td></tr>
CLEOF
	;;
	PPPOE)
          if [ "$PPPOE_IDLE" = "NO" ]; then
            CHK1=checked
            CHK2=
            IDLE=
          else
            CHK1=
            CHK2=checked
            IDLE=$PPPOE_IDLE
	  fi
cat << CLEOF
<tr><td class=row1 align=right><b>$Psd</td>
 <td class=row2><input type=text name=IF_INET value="${IF_INET}" size=5></td></tr>
<tr><td align=right class=row1><b>$Ioc</b><br>$Iot</td>
 <td class=row2><input type=radio value=NO ${CHK1} name=DEMANDMODE>$Ikc<br><input type=radio value=YES ${CHK2} name=DEMANDMODE>$Iuc<br>
$Itm: &nbsp;<input type=text name=DEMANDTIME value="${IDLE}" size=4>&nbsp;$Wsc</td></tr>
<tr><td class=row1 align=right><b>PPPoE $Ius</b></td>
 <td class=row2><INPUT name=USERNAME value="${PPPOE_USERNAME}" size=20></td></tr>
<tr><td class=row1 align=right><b>PPPoE $Ips</b></td>
 <td class=row2><INPUT type=password name=PASSWORD1 value="${PPPOE_PASSWORD}" size=20></td></tr>
CLEOF
	;;
	PPP)
	 if [ "$PPP_DEMANDDIAL" = "NO" ]; then
		CHK1=checked
		CHK2=
		IDLE=
	 else
		CHK1=
		CHK2=checked
		IDLE=$PPP_DEMANDDIAL
	 fi
	 if [ "$PPP_CHATLOGIN" = "YES" ]; then
		CHK4=checked
		CHK3=
	 else
		CHK4=
		CHK3=checked
	 fi
	 if [ "$PPP_STATICIP" = "NO" ]; then
		CHK5=checked
		CHK6=
		STATICIP=
	 else
		CHK5=
		CHK6=checked
		STATICIP=$PPP_STATICIP
	 fi
cat << CLEOF
<tr><td class=row1 align=right width="50%" rowspan=2><b>$Plb</b><br>$Plc $Pld</td><td class=row2><input type=radio value=NO ${CHK1} name=DEMANDMODE>$Ple</td></tr>
<tr><td class=row2><input type=radio value=YES ${CHK2} name=DEMANDMODE>$Plf<br>$Plg &nbsp;<input type=text name=IDLETIME value="${IDLE}" size=4>&nbsp;$Plh</td></tr>
<tr><td class=row1 align=right><b>$Pli</b><br>$Plj</td><td class=row2><input type=text name=MODEMDEV size=16 value="$PPP_MODEMTTY"></td></tr>
<tr><td class=row1 align=right><b>$Plk</b><br>$Plm</td><td class=row2><input type=text name=PORTSPEED size=16 value="$PPP_PORTSPEED"></td></tr>
<tr><td class=row1 align=right><b>$Pln</b><br>$Plo 'ATZ' $Plp 'AT&FS11=55' $Plq</td><td class=row2><input type=text name=MODEMINIT size=16 value="$PPP_INITSTR"></td></tr>
<tr><td class=row1 align=right><b>$Plr</b><br>$Pls</td><td class=row2><input name=PHONENUM size=16 value="$PPP_PHONENUM"></td></tr>
<tr><td class=row1 align=right><b>$Ius</b><br>$Plt</td><td class=row2><input name=USERNAME size=16 value="$PPP_USERNAME"></td></tr>
<tr><td class=row1 align=right><b>$Ips</b><br>$Plu</td><td class=row2><input type=password name=PASSWORD1 size=16 value="$PPP_PASSWORD"></td></tr>
<tr><td class=row1 align=right><b>$Plw</b><br>$Plv ($Plx)</td></td><td class=row2><input type=radio name="CHATLOGIN" $CHK4 value=YES>$Fye &nbsp;<input type=radio name="CHATLOGIN" $CHK3 value=NO>$Fno</td></tr>
<tr><td class=row1 align=right rowspan=2><b>$Pmb</b><br>$Pmc</td><td class=row2><input type=radio name=STATIC $CHK6 value=YES>$Fye ($Pmd)<br>$Pme &nbsp;<input name=STATICIP size="16" value="$STATICIP"></td></tr>
<tr><td class=row2><input type=radio name=STATIC $CHK5 value=NO>$Fno ($Pmf)<br>$Pmg &nbsp;<input name=LOCALREMOTE size=16 value="$PPP_LOCALREMOTE"></td></tr>
CLEOF
	;;
 esac

cat << CLEOF
<tr><th colspan=2>$Ptl</th></tr>
<tr><td class=row1 align=right><b>$Psd</b></td><td class=row2 ><input type=text name=IF_INET2 size=5 value="${IF_INET2}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br>$Anm<br>$Wed $Edg</b></td><td class=row2>
<input type=text name=INET2_IPADDR size=20 value="${INET2_IPADDR}"><br>
<input type=text name=INET2_NETMASK size=20 value="${INET2_NETMASK}"><br>
<input type=text name=INET2_GATEWAY size=20 value="${INET2_GATEWAY}"><br></td></tr>
<tr><th colspan=2>$Ptm</th></tr>
<tr><td class=row1 align=right><b>$Psd</b></td><td class=row2 ><input type=text name=IF_INET3 size=5 value="${IF_INET3}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br>$Anm<br>$Wed $Edg</b></td><td class=row2>
<input type=text name=INET3_IPADDR size=20 value="${INET3_IPADDR}"><br>
<input type=text name=INET3_NETMASK size=20 value="${INET3_NETMASK}"><br>
<input type=text name=INET3_GATEWAY size=20 value="${INET3_GATEWAY}"><br></td></tr>

<tr><th colspan=2>$Ptn</th></tr>
<tr><td class=row1 align=right><b>$Psd</b></td><td class=row2 ><input type=text name=IF_INET4 size=5 value="${IF_INET4}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br>$Anm<br>$Wed $Edg</b></td><td class=row2>
<input type=text name=INET4_IPADDR size=20 value="${INET4_IPADDR}"><br>
<input type=text name=INET4_NETMASK size=20 value="${INET4_NETMASK}"><br>
<input type=text name=INET4_GATEWAY size=20 value="${INET4_GATEWAY}"><br></td></tr>

<tr><th colspan=2>DNS</th></tr>
<tr><td class=row1 align=right><b>$Afs $Ids</b></td><td class=row2 ><input type=text name=DNS1 value="${DNS1}" size=20></td></tr>
<tr><td class=row1 align=right><b>$And $Ids</b></td><td class=row2 ><input type=text name=DNS2 value="${DNS2}" size=20></td></tr>
<tr><td class=row1 align=right><b>$Ard $Ids</b></td><td class=row2 ><input type=text name=DNS3 value="${DNS3}" size=20></td></tr>
<tr><td class=row1 align=right><b>$Edn</b></td><td class=row2 ><input type=text name=DOMAINNAME value="${DOMAINNAME}" size=20></td></tr>

</table><p align=center><input type=submit value="$Fsv" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p></form>
CLEOF
}

cl_header2 "$Ecf"
case "$FORM_OKBTN" in
 "$Fsv")
	mount_configuration
 ;;
 "$Fsb")
	INETTYPE=$FORM_INETTYPE
	mount_configuration
 ;;
 *) show_ ;;
esac
cl_footer2

