#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state
SCRIPT=dhcpconf.cgi
cl_header2 "$Mdh - BrazilFW"
if [ "$FORM_ACTION" = "RELOAD" ]; then
   echo "<br><pre>"
   /etc/rc.d/rc.dnsmasq
   echo "</pre><center><div id=\"back\">[ <a href=$SCRIPT class=links><u>$Fbl</u></a> ]</div></center>"
else
  if [ "$FORM_OKBTN" = "$Fsb" ]; then
	if [ "$FORM_DHCPSERVER" = "YES" ]; then
	  if [ -z "$FORM_DHCPD_START_IP" ] || [ -z "$FORM_DHCPD_END_IP" ]; then
                echo "<center><div id=alerta>$Wth</div></center>"
		cl_footer2
		exit
 	  fi
	fi
	DHCPSERVER=$FORM_DHCPSERVER
	DHCPD_START_IP=$FORM_DHCPD_START_IP
	DHCPD_END_IP=$FORM_DHCPD_END_IP
	DHCPD_SUBNET=$FORM_DHCPD_SUBNET
	DHCPD_ROUTER=$FORM_DHCPD_ROUTER
	DHCPD_LEASE=$FORM_DHCPD_LEASE
	DHCPD_DOMAIN=$FORM_DHCPD_DOMAIN
	DHCPD_DNS1=$FORM_DHCPD_DNS1
	DHCPD_DNS2=$FORM_DHCPD_DNS2
	DHCPD_DNS3=$FORM_DHCPD_DNS3
	DHCPD_WINS1=$FORM_DHCPD_WINS1
	DHCPD_WINS2=$FORM_DHCPD_WINS2
	USE_DNS_CACHE=$FORM_DNSCACHE
	cl_rebuildconf
	echo "<br><pre>"
        /etc/rc.d/rc.dnsmasq
        echo "<pre><br>"
        echo "<center><div id=alerta>$Wta<br><b>$Wtl</b><br><a href=dhcpconf.cgi>[ $Fbk ]</a></div></center>"
	cl_footer2
	exit
  fi
	if [ "$DHCPSERVER" = "YES" ]; then
        	CHK1=
		CHK2=checked
	else
        	CHK1=checked
		CHK2=
	fi
	if [ "$USE_DNS_CACHE" = "YES" ]; then
        	CHK3=
		CHK4=checked
	else
        	CHK3=checked
		CHK4=
	fi
cat << CLEOF
<form method="POST" action="/cgi-bin/dhcpconf.cgi"><table class=maintable border=0 width="100%"><tr><th colspan=2>$Adc - $Fcg</th></tr>
<tr><td align=right class=row1><b>$Eed</b><br>$Ecd ($Frc)</td>
 <td class=row2><input type=radio value=NO  name=DNSCACHE ${CHK3}>$Fno &nbsp;<input type=radio value=YES name=DNSCACHE ${CHK4}>$Fye</td></tr>
<tr><th colspan=2>$Ads - $Fcg</th></tr><tr><td align=right class=row1><b>$Eds</b><br>$Eha ($Frc)</td>
 <td class=row2><input type=radio value=NO name=DHCPSERVER ${CHK1}>$Fno &nbsp;<input type=radio value=YES name=DHCPSERVER ${CHK2}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Esa ($Frq)</b><br>$Efs</td><td class=row2><input type=text name=DHCPD_START_IP size=20 value="${DHCPD_START_IP}"></td></tr>
<tr><td class=row1 align=right><b>$Eei ($Frq)</b><br>$Els</td><td class=row2><input type=text name=DHCPD_END_IP size=20 value="${DHCPD_END_IP}"></td></tr>
<tr><td class=row1 align=right><b>$Elt ($Fop)</b><br>$Ebl</td><td class=row2><input type=text name=DHCPD_LEASE size=20 value="${DHCPD_LEASE}"></td></tr>
<tr><th colspan=2>$Ecz</th></tr>
<tr><td class=row1 align=right><b>$Ert ($Fop)</b><br>$Ebk ($Frc)</td><td class=row2><input type=text name=DHCPD_ROUTER size=20 value="${DHCPD_ROUTER}"></td></tr>
<tr><td class=row1 align=right><b>$Esn ($Fop)</b><br>$Esm ($Frc)</td><td class=row2><input type=text name=DHCPD_SUBNET size=20 value="${DHCPD_SUBNET}"></td></tr>
<tr><td class=row1 align=right><b>$Edm ($Fop)</b><br>$Eso ($Frc)</td><td class=row2><input type=text name=DHCPD_DOMAIN size=20 value="${DHCPD_DOMAIN}"></td></tr>
<tr><td class=row1 align=right><b>$Esp ($Fop)</b><br>$Esr<br>$Ess ($Fop)</td><td class=row2><input type=text name=DHCPD_DNS1 size=20 value="${DHCPD_DNS1}"><br><input type=text name=DHCPD_DNS2 size=20 value="${DHCPD_DNS2}"><br><input type=text name=DHCPD_DNS3 size=20 value="${DHCPD_DNS3}"></td></tr>
<tr><td class=row1 align=right><b>$Est ($Fop)</b><br>$Eba<br>$Ebc</td><td class=row2><input type=text name=DHCPD_WINS1 size=20 value="${DHCPD_WINS1}"><br><input type=text name=DHCPD_WINS2 size=20 value="${DHCPD_WINS2}"></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p><table class=maintable>
<tr><td><b>$Egf</b></td><td>[ <a href=$SCRIPT?ACTION=RELOAD><u>$Egg</u></a> | <a href="editconf.cgi?CONFFILE=/etc/dnsmasq.conf.template&DESCFILE=DHCP Custom Configuration"><u>$Psa</u></a> ]</td></tr>
<tr><td><b>$Ebd</b></td><td>[ <a href=localhosts.cgi><u>$Ebe</u></a> ]</td></tr><tr><td><b>$Ebf</b></td><td>[ <a href=leases.cgi><u>$Ebg</u></a> ]</td></tr></table></form>
CLEOF
fi
cl_footer2
