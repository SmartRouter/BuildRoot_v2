#!/bin/sh
# Subnet Configuration Webadmin Script
# Author: Claudio Roberto Cussuol
# Changed to support subnet QOS in others LAN interfaces
# by BFW user "maeliseu" - Revision by BFW user "marcos do vale" - 08/04/2008

. /var/http/web-functions

SCRIPT="subnet.cgi"
FILE="/etc/coyote/subnet.cfg"
COLOR="row6"
#==================================
find_lan() {
 case "$1" in
	LAN1)	LAN="LAN1" ;;
	LAN2)	LAN="LAN2" ;;
	LAN3)	LAN="LAN3" ;;
	LAN4)	LAN="LAN4" ;;
	WLAN)	LAN="WLAN" ;;
	DMZ)	LAN="DMZ" ;;
	*)	LAN="LAN1" ;;
 esac
}
#==================================
output_line() {
 [ "$DACTIVE" = "Yes" ] &&	MyC="row4" ||	MyC="row5"
cat << CLEOF
<tr><td class=$MyC>$DACTIVE</td>
<td class=$COLOR>$ID</td>
<td class=$COLOR>$IP</td>
<td class=$COLOR>$MASK</td>
<td class=$COLOR>$DDHCP</td>
<td class=$COLOR>$DQOS</td>
<td class=$COLOR nowrap>$DDOWN_RATE</td>
<td class=$COLOR nowrap>$DDOWN_CEIL</td>
<td class=$COLOR nowrap>$DUP_RATE</td>
<td class=$COLOR nowrap>$DUP_CEIL</td>
<td class=$COLOR>$LAN</td>
<td class=$COLOR>$LAN_ID</td>
<td class=$COLOR nowrap>$CONLIMIT</td>
<td class=$COLOR nowrap>$DCOMMENT</td>
<td class=$COLOR nowrap><a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>&nbsp;[$Faf]&nbsp;</a><a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>&nbsp;[$Fae]&nbsp;</a></td></tr>
CLEOF
 [ "$COLOR" = "row6" ] && COLOR="row8" || COLOR="row6"
}
#==================================
treat_rate() {
 DRATE=
 NRATE=
 SRATE=
 case $1 in
	'$COMP_DOWN') { SRATE="$Pha"; DRATE=$SRATE; };;
	'$COMP_UP') { SRATE="$Phb"; DRATE=$SRATE; };;
	'$CLEAR_DOWNSTREAM') { SRATE="$Phc"; DRATE=$SRATE; };;
	'$CLEAR_UPSTREAM') { SRATE="$Phd";  DRATE=$SRATE; };;
	*) { NRATE=$1; DRATE="$1 kbit/s"; };;
 esac
}
#==================================
treat_line() {
 ACTIVE=$2
 ID=$3
 IP=$4
 MASK=$5
 DHCP=$6
 QOS=$7
 ACTIVE=`echo $ACTIVE | tr [A-Z] [a-z]`
 DHCP=`echo $DHCP | tr [A-Z] [a-z]`
 QOS=`echo $QOS | tr [A-Z] [a-z]`
 if [ "$QOS" = "y" ]; then
	DOWN_RATE=$8
	DOWN_CEIL=$9
	UP_RATE=$10
	UP_CEIL=$11
	treat_rate $DOWN_RATE
	DDOWN_RATE=$DRATE
	NDOWN_RATE=$NRATE
	SDOWN_RATE=$SRATE
	treat_rate $DOWN_CEIL
	DDOWN_CEIL=$DRATE
	NDOWN_CEIL=$NRATE
	SDOWN_CEIL=$SRATE
	treat_rate $UP_RATE
	DUP_RATE=$DRATE
	NUP_RATE=$NRATE
	SUP_RATE=$SRATE
	treat_rate $UP_CEIL
	DUP_CEIL=$DRATE
	NUP_CEIL=$NRATE
	SUP_CEIL=$SRATE
 else
	DOWN_RATE=
	DOWN_CEIL=
	UP_RATE=
	UP_CEIL=
	DDOWN_RATE=$Psk
	DDOWN_CEIL=$Psk
	DUP_RATE=$Psk
	DUP_CEIL=$Psk
 fi
 case $11 in
	\#*) { LAN="LAN1"; LAN_ID=$ID; CONLIMIT=0; };;
	*) { find_lan $12; LAN_ID=$13; CONLIMIT=$14; };;
 esac
 [ -z "$CONLIMIT" ] && CONLIMIT=0
 COMMENT=`echo $TMPLINE | sed s/.*#//`
 [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
 DCOMMENT=$COMMENT
 [ "$ACTIVE" = "y" ] && DACTIVE="Yes" || DACTIVE="No"
 [ "$DHCP" = "y" ] && DDHCP="Yes" || DDHCP="No"
 [ "$QOS" = "y" ] && DQOS="Yes" || DQOS="No"
 LASTID=$ID
 LASTMASK=$MASK
}
#==================================
mount_configuration() {
 DOWN_RATE=$FORM_NDOWN_RATE
 DOWN_CEIL=$FORM_NDOWN_CEIL
 UP_RATE=$FORM_NUP_RATE
 UP_CEIL=$FORM_NUP_CEIL
 [ -z $DOWN_RATE ] && DOWN_RATE='$'$FORM_SDOWN_RATE
 [ -z $DOWN_CEIL ] && DOWN_CEIL='$'$FORM_SDOWN_CEIL
 [ -z $UP_RATE ] && UP_RATE='$'$FORM_SUP_RATE
 [ -z $UP_CEIL ] && UP_CEIL='$'$FORM_SUP_CEIL
 CONFIG_LINE="subnet $FORM_ACTIVE $FORM_ID $FORM_IP $FORM_MASK $FORM_DHCP $FORM_QOS $DOWN_RATE $DOWN_CEIL $UP_RATE $UP_CEIL $FORM_LAN  $FORM_LAN_ID $FORM_CONLIMIT #$FORM_COMMENT"
}
#==================================
show_list() { #<td align="center"><b>Line#</td>
cat << CLEOF
<table class=maintable border=0 width="100%"><tr><th colspan=15>$Psg</th></tr>
<tr><td class=header>$Faj</td>
<td class=header>$Psh</td>
<td class=header>$Aip</td>
<td class=header>$Anm</td>
<td class=header>$Psi</td>
<td class=header>$Psj</td>
<td class=header>$Phi</td>
<td class=header>$Phj</td>
<td class=header>$Phk</td>
<td class=header>$Phl</td>
<td class=header>LAN</td>
<td class=header>LAN ID</td>
<td class=header>CONN LIMIT</td>
<td class=header>$Fad</td>
<td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | tr [\\] [\|] | while read TMPLINE; do
 LINECOUNT=$(($LINECOUNT+1))
 case "$TMPLINE" in
	\#*|"") continue;;
	 subnet*) { treat_line $TMPLINE; output_line; };;
 esac
done
cat << CLEOF
</table><br>
<table class=maintable>
<tr><td class=row1><b>$Pid</b></td><td class=row2>[ &nbsp;<a href=$SCRIPT?ACTION=CALL_ADD><u>$Psl</u></a>&nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=$FILE&DESCFILE=Subnet Configuration File"><u>$Psm</u></a>&nbsp;  | &nbsp;
<a href=$SCRIPT?ACTION=RELOAD><u>Reload</u></a>&nbsp ]</td></tr>
</table></form>
CLEOF
}
#==================================
show_form() {
FORMTITLE="$Psg"
if [ -z "$ID" ]; then
 LASTLINE=`grep subnet $FILE | tail -n 1`
 [ -n "$LASTLINE" ] && treat_line $LASTLINE
 ID=$(($LASTID+1))
 IP=
fi
[ -z "$DOWN_RATE" ] && NDOWN_RATE='' && SDOWN_RATE='Individual Download'
[ -z "$DOWN_CEIL" ] && NDOWN_CEIL='' && SDOWN_CEIL='Total Download'
[ -z "$UP_RATE" ] && NUP_RATE='' && SUP_RATE='Individual Upload'
[ -z "$UP_CEIL" ] && NUP_CEIL='' && SUP_CEIL='Total Upload'
cat << CLEOF
<form method="POST" action="$SCRIPT">
<input type=hidden value="$LINE" name=LINE>
<input type=hidden value="$ACTION" name=ACTION>
<table class=maintable width=100%><tr><th colspan=2>$FORMTITLE</th></tr>
<tr><td class=row1 align=right><b>$Paz</b><br>$Pba</td>
    <td class=row2><input type=radio value=n name=ACTIVE `[ "$ACTIVE" = "n" ] && echo checked`>$Fno &nbsp;<input type=radio value=y name=ACTIVE `[ "$ACTIVE" != "n" ] && echo checked`>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Psh</b><br><small>$Psn</small></td>
    <td class=row2><input type=text name=ID value="$ID" size=5></td></tr>
<tr><td class=row1 align=right><b>$Aip</b><br><small>$Pso</small></td>
    <td class=row2><input type=text name=IP value="$IP" size=20></td></tr>
<tr><td class=row1 align=right><b>$Anm</b><br><small>$Psp</small></td>
    <td class=row2><input type=text name=MASK value="$MASK" size=20></td></tr>
<tr><td class=row1 align=right><b>$Psi</b><br>$Psq</td>
    <td class=row2><input type=radio value=n name=DHCP `[ "$DHCP" = "n" ] && echo checked`>$Fno &nbsp;<input type=radio value=y name=DHCP `[ "$DHCP" != "n" ] && echo checked`>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Psj</b><br>$Psr</td>
    <td class=row2><input type=radio value=n name=QOS `[ "$QOS" = "n" ] && echo checked`>$Fno &nbsp;<input type=radio value=y name=QOS `[ "$QOS" != "n" ] && echo checked`>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Phi</b><br><small>$Phv  $Phw</small></td><td class=row2><input type=text name=NDOWN_RATE value="$NDOWN_RATE" size=4>&nbsp; kbits/s $Far<br>
 <select name=SDOWN_RATE><option value></option><option value='COMP_DOWN' `[ "$SDOWN_RATE" = "Individual Download" ] && echo selected`>$Phx</option>
 <option value='CLEAR_DOWNSTREAM' `[ "$SDOWN_RATE" = "Total Download" ] && echo selected`>$Phy</option></select></td></tr>
<tr><td class=row1 align=right><b>$Phj</b><br><small>$Phz  $Phw</small></td><td class=row2><input type=text name=NDOWN_CEIL value="$NDOWN_CEIL" size=4>&nbsp; kbits/s $Far<br>
 <select name=SDOWN_CEIL><option value></option><option value='COMP_DOWN' `[ "$SDOWN_CEIL" = "Individual Download" ] && echo selected`>$Phx</option>
 <option value='CLEAR_DOWNSTREAM' `[ "$SDOWN_CEIL" = "Total Download" ] && echo selected`>$Phy</option></select></td></tr>
<tr><td class=row1 align=right><b>$Phk</b><br><small>$Phv  $Phw</small></td><td class=row2><input type=text name=NUP_RATE value="$NUP_RATE" size=4>&nbsp; kbits/s $Far<br>
 <select name=SUP_RATE><option value></option><option value='COMP_UP' `[ "$SUP_RATE" = "Individual Upload" ] && echo selected`>$Phb</option>
 <option value='CLEAR_UPSTREAM' `[ "$SUP_RATE" = "Total Upload" ] && echo selected`>$Phd</option></select></td></tr>
<tr><td class=row1 align=right><b>$Phl</b><br><small>$Phz  $Phw</small></td><td class=row2><input type=text name=NUP_CEIL value="$NUP_CEIL" size=4>&nbsp; kbits/s $Far<br>
 <select name=SUP_CEIL><option value></option><option value='COMP_UP' `[ "$SUP_CEIL" = "Individual Upload" ] && echo selected`>$Phb</option>
 <option value='CLEAR_UPSTREAM' `[ "$SUP_CEIL" = "Total Upload" ] && echo selected`>$Phd</option></select></td></tr>
<tr><td class=row1 align=right><b>LAN</b><br><small></small></td>
    <td class=row2><select name=LAN>
     <option value=LAN1 `[ "$LAN" = "LAN1" ] && echo selected`>LAN1</option>
CLEOF
 [ ! -z $IF_LOCAL2 ] && echo "<option value=LAN2 `[ "$LAN" = "LAN2" ] && echo selected`>LAN2</option>"
 [ ! -z $IF_LOCAL3 ] && echo "<option value=LAN3 `[ "$LAN" = "LAN3" ] && echo selected`>LAN3</option>"
 [ ! -z $IF_LOCAL4 ] && echo "<option value=LAN4 `[ "$LAN" = "LAN4" ] && echo selected`>LAN4</option>"
 [ ! -z $IF_WLAN ] && echo "<option value=WLAN `[ "$LAN" = "WLAN" ] && echo selected`>WLAN</option>"
 [ ! -z $IF_DMZ ] && echo "<option value=DMZ `[ "$LAN" = "DMZ" ] && echo selected`>DMZ</option>"
cat << CLEOF
</select></td></tr>
<tr><td class=row1 align=right><b>ID da LAN</b><br><small></small></td>
    <td class=row2><input type=text name=LAN_ID value="$LAN_ID" size=5></td></tr>
<tr><td class=row1 align=right><b>CONLIMIT</b><br><small></small></td>
    <td class=row2><input type=text name=CONLIMIT value="$CONLIMIT" size=5></td></tr>
<tr><td class=row1 align=right><b>$Fad ($Fop)</b><br><small>$Pss</small></td><td class=row2><input type=text name=COMMENT value="$COMMENT" size=30></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p>
</form>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Psg - BrazilFW"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 mount_configuration
 if [ -n "$CONFIG_LINE" ]; then
	[ "$FORM_ACTION" = "ADD" ] && echo -e "$CONFIG_LINE" >> $FILE \
	|| sed -i "$FORM_LINE"s/.*/"$CONFIG_LINE"/ $FILE
	echo "<center><div id=alerta>$Pst<br>
	$Wsv<br>
	<a href=backup.cgi class=links>$Wtl</a></div><br>
	<div id=back><a href=$SCRIPT?ACTION=RELOAD class=links>$Psv</a><br></div><br></center>"
 fi
fi

case "$FORM_ACTION" in
 "DELETE")
	sed -i "$FORM_LINE"d $FILE
	echo "<center><div>$Psu<br>"
	echo "<a>$Wtl</a><br>"
	echo "<a>$Psv</a></div></center><br>"
	show_list
 ;;
 "CALL_EDIT")
	TMPLINE=`sed $FORM_LINE!d $FILE`
	treat_line $TMPLINE
	ACTION="EDIT"
	LINE=$FORM_LINE
	show_form
 ;;
 "CALL_ADD")
	METHOD=$FORM_METHOD
	ACTION="ADD"
	LINE=0
	show_form
 ;;
 "RELOAD")
	echo "<br><pre>"
	/etc/rc.d/rc.subnet
	echo "</pre><center><div id=\"back\">[ <a href=$SCRIPT class=links><u>$Fbl</u></a> ]</div></center>"
 ;;
 *)
	show_list
 ;;
esac
cl_footer2

