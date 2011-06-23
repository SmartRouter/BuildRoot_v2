#!/bin/sh

. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state

cl_header2 "$Lyf"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 if [ -z "$FORM_IPADDR" ] || [ -z "$FORM_NETMASK" ]; then
	echo "<center><div id=alerta>$Lym</div></center>"
	cl_footer2
	exit
 fi
 IF_LOCAL=$FORM_IF_LOCAL
 LOCAL_IPADDR=$FORM_IPADDR
 LOCAL_IPADDR2=$FORM_IPADDR2
 LOCAL_IPADDR3=$FORM_IPADDR3
 LOCAL_NETMASK=$FORM_NETMASK
 LOCAL_NETMASK2=$FORM_NETMASK2
 LOCAL_NETMASK3=$FORM_NETMASK3

 IF_LOCAL2=$FORM_IF_LOCAL2
 LOCAL2_IPADDR=$FORM_LOCAL2_IPADDR
 LOCAL2_NETMASK=$FORM_LOCAL2_NETMASK

 IF_LOCAL3=$FORM_IF_LOCAL3
 LOCAL3_IPADDR=$FORM_LOCAL3_IPADDR
 LOCAL3_NETMASK=$FORM_LOCAL3_NETMASK

 IF_LOCAL4=$FORM_IF_LOCAL4
 LOCAL4_IPADDR=$FORM_LOCAL4_IPADDR
 LOCAL4_NETMASK=$FORM_LOCAL4_NETMASK

 IF_WLAN=$FORM_IF_WLAN
 WLAN_IPADDR=$FORM_WLAN_IPADDR
 WLAN_NETMASK=$FORM_WLAN_NETMASK

 cl_rebuildconf
 echo "<center><div id=alerta>$Lyn<br>$Wtc</div></center>"
fi

cat << CLEOF
<form method="POST" action="/cgi-bin/lanconf.cgi">
<table class=maintable border=0 width="100%">
<tr><th colspan=2>$Lyf</th></tr>
<tr><td width="50%" class=row1 align=right><b>$Psc<br></b></td><td width="50%" class=row2><input type=text name=IF_LOCAL size=5 value="${IF_LOCAL}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=IPADDR size=20 value="${LOCAL_IPADDR}"><br>
 <input type=text name=NETMASK size=20 value="${LOCAL_NETMASK}"></td></tr>
<tr><td class=row1 align=right>($Wop) <b>$Lpj<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=IPADDR2 size=20 value="${LOCAL_IPADDR2}"><br>
 <input type=text name=NETMASK2 size=20 value="${LOCAL_NETMASK2}"></td></tr>
<tr><td class=row1 align=right>($Wop) <b>$Lpk<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=IPADDR3 size=20 value="${LOCAL_IPADDR3}"><br>
 <input type=text name=NETMASK3 size=20 value="${LOCAL_NETMASK3}"></td></tr>

<tr><th colspan=2>$Pte</th></tr>
<tr><td width="50%" class=row1 align=right><b>$Ptg<br></b></td><td width="50%" class=row2><input type=text name=IF_LOCAL2 size=5 value="${IF_LOCAL2}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=LOCAL2_IPADDR size=20 value="${LOCAL2_IPADDR}"><br>
 <input type=text name=LOCAL2_NETMASK size=20 value="${LOCAL2_NETMASK}"></td></tr>
<tr><th colspan=2>$Ptv</th></tr>
<tr><td width="50%" class=row1 align=right><b>$Pty<br></b></td><td width="50%" class=row2><input type=text name=IF_LOCAL3 size=5 value="${IF_LOCAL3}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=LOCAL3_IPADDR size=20 value="${LOCAL3_IPADDR}"><br>
 <input type=text name=LOCAL3_NETMASK size=20 value="${LOCAL3_NETMASK}"></td></tr>
<tr><th colspan=2>$Ptx</th></tr>
<tr><td width="50%" class=row1 align=right><b>$Ptz<br></b></td><td width="50%" class=row2><input type=text name=IF_LOCAL4 size=5 value="${IF_LOCAL4}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=LOCAL4_IPADDR size=20 value="${LOCAL4_IPADDR}"><br>
 <input type=text name=LOCAL4_NETMASK size=20 value="${LOCAL4_NETMASK}"></td></tr>
<tr><th colspan=2>$Ptf</th></tr>
<tr><td width="50%" class=row1 align=right><b>$Pth<br></b></td><td width="50%" class=row2><input type=text name=IF_WLAN size=5 value="${IF_WLAN}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=WLAN_IPADDR size=20 value="${WLAN_IPADDR}"><br>
 <input type=text name=WLAN_NETMASK size=20 value="${WLAN_NETMASK}"></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN><input type=reset value="$Fer"></p></form>
CLEOF

cl_footer2
