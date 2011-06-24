#!/bin/sh
# Revision by BFW user "marcos do vale" - 28/02/2008
# Changed to support Load Balance with IP Alias interfaces in IF_INET
# Revision by BFW user "marcos do vale" - 13/10/2008
# Add Static route for nets and ports
# Revision 27/07/2009 AdslWiFi añadiendo pruebas a 4 Ping's diferentes

. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state

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

SCRIPT="loadbalance.cgi"
FILE="/etc/coyote/route.cfg"
RELOAD="/etc/rc.d/rc.loadbalance"
AWK_SCRIPT='{ LINHA=$1; COMMENT=substr($2,1); search=" "; n=split(LINHA,array,search);
 { if ( array[2] == "y" ) { ACTIVE=Fye } else { ACTIVE=Fno } }
 }{print array[1]" "ACTIVE" "array[3]" "array[4]" "array[5]" "array[6]" "COMMENT}'

#==================================
list_wan() {
 eval LINK=\$IF_INET_LB$1
 echo "<select name=IF_INET_LB$1><option value= `[ "$LINK" = " " ] && echo selected`></option>"
 [ ! -z $IF_INET ] && echo "<option value=WAN1 `[ "$LINK" = "WAN1" ] && echo selected`>WAN1</option>"
 [ ! -z $IF_INET2 ] && echo "<option value=WAN2 `[ "$LINK" = "WAN2" ] && echo selected`>WAN2</option>"
 [ ! -z $IF_INET3 ] && echo "<option value=WAN3 `[ "$LINK" = "WAN3" ] && echo selected`>WAN3</option>"
 [ ! -z $IF_INET4 ] && echo "<option value=WAN4 `[ "$LINK" = "WAN4" ] && echo selected`>WAN4</option>"
}
=================================
treat_line() {
 ACTIVE=${2}
 LB=${3}
 LAN=${4}
 NET=${5}
 MASK=${6}
 COMMENT=`echo $TMPLINE | sed s/.*#//`
 [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
 DCOMMENT=$COMMENT
 ACTIVE=`echo $ACTIVE | tr [A-Z] [a-z]`
 [ "$ACTIVE" = "y" ] && DACTIVE="Yes" || DACTIVE="No"
}
#==================================
show_list_port() {
 init_main_table
 add_title "Porta" "6"
 header_table "$Faj" "LINK" "$Paj" "$Pbp" "$Pbr" "$Fad"
 LINECOUNT=0
 awk -vFno=$Fno -vFye=$Fye -F"#" "$AWK_SCRIPT" $FILE | while read TYPE ACTIVE LB PROTO INIT END COMMENT; do
	LINECOUNT=$(($LINECOUNT+1))
	case "$TYPE" in
	 port*) output_line "$ACTIVE" "$LB" "$PROTO" "$INIT" "$END" "$COMMENT";;
	esac
 done
}
#==================================
show_list_dest() {
 init_main_table
 add_title "Destino" "5"
 header_table "$Faj" "LINK" "$Aip" "$Anm" "$Fad"
 LINECOUNT=0
 awk -vFno=$Fno -vFye=$Fye -F"#" "$AWK_SCRIPT" $FILE | while read TYPE ACTIVE LB IP MASK COMMENT; do
	LINECOUNT=$(($LINECOUNT+1))
	case "$TYPE" in
	 dest*) output_line "$ACTIVE" "$LB" "$IP" "$MASK" "$COMMENT";;
	esac
 done
}
#==================================
show_list_net() {
 init_main_table
 add_title "Origem" "6"
 header_table "$Faj" "LINK" "LAN" "$Aip" "$Anm" "$Fad"
 LINECOUNT=0
 awk -vFno=$Fno -vFye=$Fye -F"#" "$AWK_SCRIPT" $FILE | while read TYPE ACTIVE LB LAN IP MASK COMMENT; do
	LINECOUNT=$(($LINECOUNT+1))
	case "$TYPE" in
	 net*) output_line "$ACTIVE" "$LB" "$LAN" "$IP" "$MASK" "$COMMENT";;
	esac
 done
}
#==================================
mount_configuration() {
 LOAD_BALANCE=$FORM_LOAD_BALANCE
 PING_RETRY=$FORM_PING_RETRY
 PING_IP=$FORM_PING_IP
 PING_RETRY_2=$FORM_PING_RETRY_2
 PING_IP_2=$FORM_PING_IP_2
 PING_RETRY_3=$FORM_PING_RETRY_3
 PING_IP_3=$FORM_PING_IP_3
 PING_RETRY_4=$FORM_PING_RETRY_4
 PING_IP_4=$FORM_PING_IP_4
 IF_INET_LB1=$FORM_IF_INET_LB1
 INET_WEIGHT=$FORM_INET_WEIGHT
 IF_INET_LB2=$FORM_IF_INET_LB2
 INET2_WEIGHT=$FORM_INET2_WEIGHT
 IF_INET_LB3=$FORM_IF_INET_LB3
 INET3_WEIGHT=$FORM_INET3_WEIGHT
 IF_INET_LB4=$FORM_IF_INET_LB4
 INET4_WEIGHT=$FORM_INET4_WEIGHT
 cl_rebuildconf
}
#==================================
show_list() {
 init_table "maintable"
 init_add_control "$Pid"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=P" "New Port"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=N" "New Net"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=D" "New Dest"
 add_control "editconf.cgi?CONFFILE=$FILE&DESCFILE=Route Configuration File" "Edit Conf. File"
 add_control "$SCRIPT?ACTION=RELOAD" "Reload"
 end_add_control
 end_table
 echo "<br>"
cat << CLEOF
<form method="POST" action="$SCRIPT">
<table class=maintable border=0 width="100%"><tr><th colspan=4>$Pti</th></tr>
<tr><td colspan=2 class=row1 align=right><b>$Ptj</b></td>
<td colspan=2 class=row2><input type=radio value=NO name=LOAD_BALANCE `[ "$LOAD_BALANCE" != YES ] && echo CHECKED`>$Fno &nbsp;
<input type=radio value=YES name=LOAD_BALANCE `[ "$LOAD_BALANCE" = YES ] && echo CHECKED`>$Fye</td></tr>
<tr><td colspan=1 class=row1 align=right><b>IP PING</b></td>
<td colspan=1 class=row2><input type=text name=PING_IP size=20 value="${PING_IP}"></td>
<td colspan=1 class=row1 align=right><b>PING RETRY</b></td>
<td colspan=1 class=row2><input type=text name=PING_RETRY size=3 value="${PING_RETRY}"></td></tr>
<tr><td colspan=1 class=row1 align=right><b>2ª IP PING</b></td>
<td colspan=1 class=row2><input type=text name=PING_IP_2 size=20 value="${PING_IP_2}"></td>
<td colspan=1 class=row1 align=right><b>2º PING RETRY</b></td>
<td colspan=1 class=row2><input type=text name=PING_RETRY_2 size=3 value="${PING_RETRY_2}"></td></tr>
<tr><td colspan=1 class=row1 align=right><b>3ª IP PING</b></td>
<td colspan=1 class=row2><input type=text name=PING_IP_3 size=20 value="${PING_IP_3}"></td>
<td colspan=1 class=row1 align=right><b>3º PING RETRY</b></td>
<td colspan=1 class=row2><input type=text name=PING_RETRY_3 size=3 value="${PING_RETRY_3}"></td></tr>
<tr><td colspan=1 class=row1 align=right><b>4ª IP PING</b></td>
<td colspan=1 class=row2><input type=text name=PING_IP_4 size=20 value="${PING_IP_4}"></td>
<td colspan=1 class=row1 align=right><b>4º PING RETRY</b></td>
<td colspan=1 class=row2><input type=text name=PING_RETRY_4 size=3 value="${PING_RETRY_4}"></td></tr>
<tr><td colspan=4 class=row1><b><center>$Ptq</td></tr>
<tr><th colspan=2>$Ptk</th><th colspan=2>$Ptl</th></tr>
<tr><td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td class=row2>
CLEOF
 list_wan "1"
 echo "</td><td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td class=row2>"
 list_wan "2"
cat << CLEOF
</tr><tr><td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET_WEIGHT size=5 value="${INET_WEIGHT}"></td>
<td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET2_WEIGHT size=5 value="${INET2_WEIGHT}"></td></tr>
<tr><th colspan=2>$Ptm</th><th colspan=2>$Ptn</th></tr>
<tr><td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td class=row2>
CLEOF
 list_wan "3"
 echo "</td><td width="25%" class=row1 align=right><b>$Ptp<br></b></td><td class=row2>"
 list_wan "4"
cat << CLEOF
</tr><tr><td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET3_WEIGHT size=5 value="${INET3_WEIGHT}"></td>
<td width="25%" class=row1 align=right><b>$Pto</b></td>
<td width="25%" class=row2><input type=text name=INET4_WEIGHT size=5 value="${INET4_WEIGHT}"></td></tr>
</table><br>
CLEOF
 end_form
 show_list_port
 echo "</table><br>"
 show_list_dest
 echo "</table><br>"
 show_list_net
 echo "</table><table class=maintable>"
}
#==================================
show_form() {
 [ "$METHOD" = "P" ] && FORMTITLE="PORT" || [ "$METHOD" = "N" ] && FORMTITLE="NET" || FORMTITLE="DEST"
cat << CLEOF
<form method="POST" action="$SCRIPT">
<input type=hidden value="$LINE" name=LINE>
<input type=hidden value="$ACTION" name=ACTION>
<input type=hidden value="$METHOD" name=METHOD>
<table class=maintable width=100%><tr><th colspan=2>$FORMTITLE</th></tr>
<tr><td class=row1 align=right><b>$Paz</b><br>$Pba</td>
<td class=row2><input type=radio value=n name=ACTIVE `[ "$ACTIVE" = "n" ] && echo checked`>$Fno &nbsp;<input type=radio value=y name=ACTIVE `[ "$ACTIVE" != "n" ] && echo checked`>$Fye</td></tr>
<tr><td class=row1 align=right><b>LINK</b></td><td class=row2><select name=LB>
CLEOF
 [ ! -z $IF_INET_LB1 ] && echo "<option value=LB1 `[ "$LB" = "LB1" ] && echo selected`>LB1</option>"
 [ ! -z $IF_INET_LB2 ] && echo "<option value=LB2 `[ "$LB" = "LB2" ] && echo selected`>LB2</option>"
 [ ! -z $IF_INET_LB3 ] && echo "<option value=LB3 `[ "$LB" = "LB3" ] && echo selected`>LB3</option>"
 [ ! -z $IF_INET_LB4 ] && echo "<option value=LB4 `[ "$LB" = "LB4" ] && echo selected`>LB4</option>"
echo "</td></tr>
<tr><td class=row1 align=right><b>"
case $METHOD in
 N)
  echo "LAN</b></td><td class=row2><select name=LAN>"
  [ ! -z $IF_LOCAL ] && echo "<option value=LAN1 `[ "$LAN" = "LAN1" ] && echo selected`>LAN1</option>"
  [ ! -z $IF_LOCAL2 ] && echo "<option value=LAN2 `[ "$LAN" = "LAN2" ] && echo selected`>LAN2</option>"
  [ ! -z $IF_LOCAL3 ] && echo "<option value=LAN3 `[ "$LAN" = "LAN3" ] && echo selected`>LAN3</option>"
  [ ! -z $IF_LOCAL4 ] && echo "<option value=LAN4 `[ "$LAN" = "LAN4" ] && echo selected`>LAN4</option>"
  [ ! -z $IF_WLAN ] && echo "<option value=WLAN `[ "$LAN" = "WLAN" ] && echo selected`>WLAN</option>"
  [ ! -z $IF_DMZ ] && echo "<option value=DMZ `[ "$LAN" = "DMZ" ] && echo selected`>DMZ</option>"
  echo "</td></tr>
  <tr><td class=row1 align=right><b>$Aip</b></td>"
  echo "<td class=row2><input type=text size=22 name=NET value="$NET"></td></tr>
  <tr><td class=row1 align=right><b>$Anm</b></td>
  <td class=row2><input type=text size=22 name=MASK value="$MASK"></td></tr>"
 ;;
 P)
  echo "$Paj</b></td><td class=row2><select name=LAN>"
  echo "<option value=tcp `[ "$LAN" = "tcp" ] && echo selected`>TCP</option>"
  echo "<option value=udp `[ "$LAN" = "udp" ] && echo selected`>UDP</option>"
  echo "</td></tr>
  <tr><td class=row1 align=right><b>$Pbp</b></td>"
  echo "<td class=row2><input type=text size=10 name=NET value="$NET"></td></tr>
  <tr><td class=row1 align=right><b>$Pbr</b></td>
  <td class=row2><input type=text size=10 name=MASK value="$MASK"></td></tr>"
 ;;
 D)
  echo "$Aip</b></td><td class=row2><input type=text size=22 name=LAN value="$LAN"></td></tr>"
  echo "<tr><td class=row1 align=right><b>$Anm</b></td>
  <td class=row2><input type=text size=22 name=NET value="$NET"></td></tr>"
 ;;
esac
echo "<tr><td class=row1 align=right><b>$Fad ($Fop)</b><br>$Egr</td><td class=row2><input type=text size=30 name=COMMENT value="$COMMENT"></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;&nbsp;<input type=reset value="$Fer"></p></form>"
}
#==================================
# MAIN ROUTINE
cl_header2 "$Pti - BrazilFW"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 [ "$FORM_METHOD" = "P" ] && CONFIG_LINE="port $FORM_ACTIVE $FORM_LB $FORM_LAN $FORM_NET $FORM_MASK #$FORM_COMMENT"
 [ "$FORM_METHOD" = "N" ] && CONFIG_LINE="net $FORM_ACTIVE $FORM_LB $FORM_LAN $FORM_NET $FORM_MASK #$FORM_COMMENT"
 [ "$FORM_METHOD" = "D" ] && CONFIG_LINE="dest $FORM_ACTIVE $FORM_LB $FORM_LAN $FORM_NET #$FORM_COMMENT"
 if [ -n "$CONFIG_LINE" ]; then
	[ "$FORM_ACTION" = "ADD" ] && echo -e "$CONFIG_LINE" >> $FILE \
	|| sed -i "$FORM_LINE"s/.*/"$CONFIG_LINE"/ $FILE
 else
	mount_configuration
 fi
 alert "$Wsv" "$Psv"
fi
case "$FORM_ACTION" in
 "DELETE")
	sed -i "$FORM_LINE"d $FILE
	alert "" "$Psv"
	show_list
 ;;
 "CALL_EDIT")
	TMPLINE=`sed $FORM_LINE!d $FILE`
	ACTION="EDIT"
	LINE=$FORM_LINE
	case "$TMPLINE" in
	 \#*|"") continue ;;
	 port*) { treat_line $TMPLINE; METHOD=P; show_form; } ;;
	 net*) { treat_line $TMPLINE; METHOD=N; show_form; } ;;
	 dest*) { treat_line $TMPLINE; METHOD=D; show_form; } ;;
	esac
 ;;
 "CALL_ADD")
	METHOD=$FORM_METHOD
	ACTION="ADD"
	LINE=0
	show_form
 ;;
 "RELOAD") command_reload;;
 *) show_list;;
esac
cl_footer2
