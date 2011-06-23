#!/bin/sh
# Changed to support Load Balance with IP Alias interfaces in IF_INET
# by BFW user "marcos do vale" - 28/02/2008
. /var/http/web-functions
. /etc/coyote/coyote.conf
[ -z "$PING_IP" ] && PING_IP=72.14.205.103
[ -z "$PING_RETRY" ] && PING_RETRY=3
cl_header2 "$Lyf"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 LOAD_BALANCE=$FORM_LOAD_BALANCE
 PING_RETRY=$FORM_PING_RETRY
 PING_IP=$FORM_PING_IP
 IF_INET_LB1=$FORM_IF_INET_LB1
 INET_WEIGHT=$FORM_INET_WEIGHT
 IF_INET_LB2=$FORM_IF_INET_LB2
 INET2_WEIGHT=$FORM_INET2_WEIGHT
 IF_INET_LB3=$FORM_IF_INET_LB3
 INET3_WEIGHT=$FORM_INET3_WEIGHT
 IF_INET_LB4=$FORM_IF_INET_LB4
 INET4_WEIGHT=$FORM_INET4_WEIGHT
 cl_rebuildconf
 echo "<center><div id=alerta>$Ptr<br>$Wtc</div></center>"
else
cat << CLEOF
<form method="POST" action="/cgi-bin/loadbalance.cgi">
<table class=maintable border=0 width="100%">
<tr><th colspan=4>$Pti</th></tr>
<tr><td colspan=2 class=row1 align=right><b>$Ptj</b></td>
<td colspan=2 class=row2><input type=radio value=NO name=LOAD_BALANCE `[ "$LOAD_BALANCE" != YES ] && echo CHECKED`>$Fno &nbsp;
<input type=radio value=YES name=LOAD_BALANCE `[ "$LOAD_BALANCE" = YES ] && echo CHECKED`>$Fye</td></tr>
<tr><td colspan=1 class=row1 align=right><b>IP PING</b></td>
<td colspan=1 class=row2><input type=text name=PING_IP size=20 value="${PING_IP}"></td>
<td colspan=1 class=row1 align=right><b>PING RETRY</b></td>
<td colspan=1 class=row2><input type=text name=PING_RETRY size=3 value="${PING_RETRY}"></td></tr>

<tr><td colspan=4 class=row1><b><center>$Ptq</td></tr>
<tr><th colspan=2>$Ptk</th><th colspan=2>$Ptl</th></tr>
<tr><td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td width="25%" class=row2>
<input type=text name=IF_INET_LB1 size=5 value="${IF_INET_LB1}"></td>
<td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td width="25%" class=row2>
<input type=text name=IF_INET_LB2 size=5 value="${IF_INET_LB2}"></td></tr>
<tr><td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET_WEIGHT size=5 value="${INET_WEIGHT}"></td>
<td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET2_WEIGHT size=5 value="${INET2_WEIGHT}"></td></tr>
<tr><th colspan=2>$Ptm</th><th colspan=2>$Ptn</th></tr>
<tr><td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td width="25%" class=row2>
<input type=text name=IF_INET_LB3 size=5 value="${IF_INET_LB3}"></td>
<td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td width="25%" class=row2>
<input type=text name=IF_INET_LB4 size=5 value="${IF_INET_LB4}"></td></tr>
<tr><td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET3_WEIGHT size=5 value="${INET3_WEIGHT}"></td>
<td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET4_WEIGHT size=5 value="${INET4_WEIGHT}"></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN><input type=reset value="$Fer"></p></form>
CLEOF
fi
cl_footer2
