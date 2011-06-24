#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state
cl_header2 "DMZ Configuration"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
	IF_DMZ=$FORM_IF_DMZ
	DMZ_IPADDR=$FORM_IPADDR
	DMZ_IPADDR2=$FORM_IPADDR2
	DMZ_IPADDR3=$FORM_IPADDR3
	DMZ_NETMASK=$FORM_NETMASK
	DMZ_NETMASK2=$FORM_NETMASK2
	DMZ_NETMASK3=$FORM_NETMASK3
	cl_rebuildconf
. /usr/sbin/write_state.sh
        echo "<center><div id=alerta>SmartRouter - $Lyn<br>$Wtc</div></center>"
else
cat << CLEOF
<form method="POST" action="/cgi-bin/dmzconf.cgi">
<table border=0 width="100%" class=maintable>
<tr><th colspan=2>$Mdz</th></tr>
<tr><td width=50% class=row1 align=right><b>$Pse</b></td><td width="50%" class=row2><input type=text name=IF_DMZ size=5 value="${IF_DMZ}"></td></tr>
<tr><td class=row1 align=right><b>$Lpi<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=IPADDR size=20 value="${DMZ_IPADDR}"><br><input type=text name=NETMASK size=20 value="${DMZ_NETMASK}"></td></tr>
<tr><td class=row1 align=right>($Wop) <b>$Lpj<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=IPADDR2 size=20 value="${DMZ_IPADDR2}"><br><input type=text name=NETMASK2 size=20 value="${DMZ_NETMASK2}"></td></tr>
<tr><td class=row1 align=right>($Wop) <b>$Lpk<br></b>$Wed<b> $Anm</b></td><td class=row2><input type=text name=IPADDR3 size=20 value="${DMZ_IPADDR3}"><br><input type=text name=NETMASK3 size=20 value="${DMZ_NETMASK3}"></td></tr>
</table>
<p align=center>
<input type=submit value="$Fsb" name=OKBTN>
<input type=reset value="$Fer"></p></form>
CLEOF
fi
cl_footer2
