#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
CONFFILE=
DESCFILE="$Pjb"

[ -n "$FORM_CONFFILE" ] && CONFFILE="$FORM_CONFFILE"
[ -n "$FORM_DESCFILE" ] && DESCFILE="$FORM_DESCFILE"
[ -z "$FORM_DESCFILE" ] && DESCFILE="$CONFFILE"

cl_header2 "Edit $DESCFILE"
cat << CLEOF
<table class=maintable><tr><th>$Mcf</th></tr><tr><td nowrap>
CLEOF
case "$FORM_OKBTN" in
	"$Feo")
		echo "$Pja $DESCFILE"
		echo "<pre>"
		echo "$FORM_CFGFILE"
		echo "</pre>"
		echo "$FORM_CFGFILE" > $CONFFILE
		echo
  	        echo "<center><div id=back><a href=backup.cgi class=links><u>$Wqa</u></a></div></center>"
		touch /tmp/need.save
		;;
	*)
if [ -n "$CONFFILE" ] ; then
  if [ "$CONFFILE" = "ANY" ] ; then
  cat << CLEOF
<center><form method=POST action=/cgi-bin/editconf.cgi>$Pjc &nbsp;
<input type=text size=30 name=CONFFILE>&nbsp;&nbsp;
<input type=submit value=&nbsp;$Faf&nbsp;></form></center>
CLEOF
   else
   cat << CLEOF
<form method="POST" action="/cgi-bin/editconf.cgi">
<input type=hidden name=CONFFILE value="$CONFFILE">
<input type=hidden name=DESCFILE value="$DESCFILE">
<b>$DESCFILE</b></td></tr>
<tr><td class=row3 align=center>
<br><textarea rows=19 name=CFGFILE cols=80 wrap="off">
CLEOF
cat $CONFFILE
cat << CLEOF
</textarea>
<p align=center><input type=submit value="$Feo" name=OKBTN><input type=reset value="$Fer"></td>
</form>
CLEOF
fi
else
cat << CLEOF
<br><ol>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/coyote/coyote.conf&DESCFILE=$Pjd">$Pjd</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/rc.d/rc.local&DESCFILE=$Pjs">$Pjs</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/modules&DESCFILE=$Pju">$Pju</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/coyote/portforwards&DESCFILE=$Pje">$Pje</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/coyote/firewall&DESCFILE=$Pjf">$Pjf</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/coyote/firewall.local&DESCFILE=$Pjg">$Pjg</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/hosts.dns&DESCFILE=$Pjh">$Pjh</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/dhcpd.reservations&DESCFILE=$Pji">$Pji</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/var/state/dhcp/dhcpd.leases&DESCFILE=$Pjj">$Pjj</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/var/spool/cron/crontabs/root&DESCFILE=$Pjv">$Pjv</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/coyote/qos.filters&DESCFILE=$Pjk">$Pjk</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/coyote/qos.classes&DESCFILE=$Pjl">$Pjl</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/qos.config&DESCFILE=$Pjm">$Pjm</a></li>
CLEOF
if [ "$INETTYPE" = "PPP" ] ; then
cat << CLEOF
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/ppp/options&DESCFILE=$Pjn">$Pjn</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/ppp/$PPP_ISP.chat&DESCFILE=$Pjo">$Pjo</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/ppp/peers/$PPP_ISP&DESCFILE=$Pjp">$Pjp</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/ppp/pap-secrets&DESCFILE=$Pjq">$Pjq</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/etc/ppp/chap-secrets&DESCFILE=$Pjr">$Pjr</a></li>
CLEOF
fi
cat << CLEOF
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=ANY">$Pjt</a></li>
  <li><a href="/cgi-bin/editconf.cgi?CONFFILE=/var/http/style.css&DESCFILE=Style">Style - CSS</a></li>
  </ol>
CLEOF
fi
	;;
esac
echo   "</td></tr></table>"
cl_footer2
