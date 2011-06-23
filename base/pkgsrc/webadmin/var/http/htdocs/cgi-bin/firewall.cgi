#!/bin/sh
# ACCESS CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# Steve Eisner - seisner@comcast.net
# 2/12/2003
. /var/http/web-functions
SCRIPT="firewall.cgi"
FILE="/etc/coyote/firewall"
TMPFILE="/etc/coyote/acctemp"
RELOAD="/etc/rc.d/rc.firewall"
COLOR="row6"
#==================================
output_line() {
 [ "$DACTIVE" = "Yes" ] && MyC="row4" || MyC="row5"
cat << CLEOF
<tr><td class=$MyC>$DACTIVE</td>
<td class=$COLOR>$DTYPE</td>
<td class=$COLOR>$DRULE</td>
<td class=$COLOR>$DPROTO</td>
<td class=$COLOR>$DSRC</td>
<td class=$COLOR>$SRPORT</td>
<td class=$COLOR>$DDEST</td>
<td class=$COLOR>$DPORT</td>
<td class=$COLOR nowrap>$DCOMMENT</td>
<td class=$COLOR nowrap>[<a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>Edit</a>] [<a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>Delete</a>]</td></tr>
CLEOF
 [ "$COLOR" = "row6" ] && COLOR="row8" || COLOR="row6"
}
#==================================
set_address() {
 PP="$1"
 NOT=`echo "$PP" | cut -c -3`
 [ "$NOT" = "not" ] && PP=`echo "$PP" | cut -c 5-` || NOT=""
 TAG=`echo "$PP" | cut -c -3`
 if [ "$TAG" = mac ] ; then
	PP=`echo "$PP" | cut -c 5-`
	ADDRESS="$PP"
 else
	TAG="$PP"
	case $PP in
	 lan|lan2|lan3|lan-if|lan-net|lan2-net|lan3-net) ADDRESS="";;
	 int|int2|int3|int-if|int-net|int2-net|int3-net) ADDRESS="";;
	 wan2|wan2-if|wan2-net|wan3|wan3-if|wan3-net|wan4|wan4-if|wan4-net) ADDRESS="";;
	 dmz|dmz2|dmz3|dmz-if|dmz-net|dmz2-net|dmz3-net) ADDRESS="";;
	 local2|local2-if|local2-net|local3|local3-if|local3-net|local4|local4-if|local4-net|wlan|wlan-if|wlan-net) ADDRESS="";;
	 any|all)  ADDRESS="";;
	 *) ADDRESS="$PP"; TAG="ip"; return 0; ;;
	esac
 fi
}
#==================================
desc_tag() {
 case "$1" in
	any)        DTAG="Any" ;;
	ip)         DTAG="IP or Host Name" ;;
	mac)        DTAG="MAC" ;;
	lan-net)    DTAG="Local Network" ;;
	lan-if)     DTAG="Local Interface" ;;
	lan)        DTAG="Local IP Address" ;;
	lan2-net)   DTAG="Local 2nd Network" ;;
	lan2)       DTAG="Local 2nd IP Address" ;;
	lan3-net)   DTAG="Local 3rd Network" ;;
	lan3)       DTAG="Local 3rd IP Address" ;;
	int-net)    DTAG="Internet" ;;
	int-if)     DTAG="Internet Interface" ;;
	int)        DTAG="Internet IP Address" ;;
	int2-net)   DTAG="Internet 2nd Network" ;;
	int2)       DTAG="Internet 2nd IP Address" ;;
	int3-net)   DTAG="Internet 3rd Network" ;;
	int3)       DTAG="Internet 3rd IP Address" ;;
	wan2-net)   DTAG="WAN2 Network" ;;
	wan2-if)    DTAG="WAN2 Interface" ;;
	wan2)       DTAG="WAN2 IP Address" ;;
	wan3-net)   DTAG="WAN3 Network" ;;
	wan3-if)    DTAG="WAN3 Interface" ;;
	wan3)       DTAG="WAN3 IP Address" ;;
	wan4-net)   DTAG="WAN4 Network" ;;
	wan4-if)    DTAG="WAN4 Interface" ;;
	wan4)       DTAG="WAN4 IP Address" ;;
	dmz-net)    DTAG="DMZ Network" ;;
	dmz-if)     DTAG="DMZ Interface" ;;
	dmz)        DTAG="DMZ IP Address" ;;
	dmz2-net)   DTAG="DMZ Second Network" ;;
	dmz2)       DTAG="DMZ Second IP Address" ;;
	dmz3-net)   DTAG="DMZ Third Network" ;;
	dmz3)       DTAG="DMZ Third IP Address" ;;
	local2-net) DTAG="LAN2 Network" ;;
	local2-if)  DTAG="LAN2 Interface" ;;
	local2)     DTAG="LAN2 IP Address" ;;
	local3-net) DTAG="LAN3 Network" ;;
	local3-if)  DTAG="LAN3 Interface" ;;
	local3)     DTAG="LAN3 IP Address" ;;
	local4-net) DTAG="LAN4 Network" ;;
	local4-if)  DTAG="LAN4 Interface" ;;
	local4)     DTAG="LAN4 IP Address" ;;
	wlan-net)   DTAG="WLAN Network" ;;
	wlan-if)    DTAG="WLAN Interface" ;;
	wlan)       DTAG="WLAN IP Address" ;;
 esac
}
#==================================
treat_line() {
 TYPE=$1
 [ "$TYPE" = "admin" ] && METHOD="A" || METHOD="F"
 DTYPE=`echo $TYPE | tr [a] [A]`
 ACTIVE=$2
 [ "$ACTIVE" = "y" ] && DACTIVE="Yes" || DACTIVE="No"
 RULE=$3
 [ "$RULE" != "permit" -a "$RULE" != "deny" ] && RULET="$RULE"
 DRULE=`echo $RULE | tr [p,d] [P,D]`
 PROTO=$4
 DPROTO=`echo $PROTO | tr [a-z] [A-Z]`
 if [ "$PROTO" != "tcp" -a "$PROTO" != "udp" -a "$PROTO" != "all" -a "$PROTO" != "icmp" ] ; then
	PROTON="$PROTO"
	PROTO=""
 fi

 SRC_IP=$5
 set_address "$SRC_IP"
 SRC_NOT="$NOT"
 SRC_TAG="$TAG"
 SRC_IP="$ADDRESS"
 [ -n "$NOT" ] && DNOT="Not " || DNOT=""
 desc_tag "$TAG"
 [ "$TAG" = "IP" ] && DTAG=""
 DSRC="$DNOT $DTAG $ADDRESS"

 DEST_IP=$6
 set_address "$DEST_IP"
 DEST_NOT="$NOT"
 DEST_TAG="$TAG"
 DEST_IP="$ADDRESS"
 [ -n "$NOT" ] && DNOT="Not " || DNOT=""
 desc_tag "$TAG"
 [ "$TAG" = "IP" ] && DTAG=""
 DDEST="$DNOT $DTAG $ADDRESS"

 P7="$7"
 PORT_NOT=`echo "$P7" | cut -c -3`
 [ "$PORT_NOT" = "not" ] && P7=`echo "$P7" | cut -c 5-` || PORT_NOT=""
 [ -n "$PORT_NOT" ] && DPORT_NOT="Not " || DPORT_NOT=""
 DPORT=$DPORT_NOT`echo $P7 | tr [a-z] [A-Z]`
 START_PORT=`echo $P7 | cut -f 1 -d :`
 END_PORT=`echo $P7 | cut -f 2 -d :`
 [ "$START_PORT" = "$END_PORT" ] && END_PORT=""

 P8="$8"
 SPORT_NOT=`echo "$P8" | cut -c -3`
 [ "$SPORT_NOT" = "not" ] && P8=`echo "$P8" | cut -c 5-` || SPORT_NOT=""
 [ -n "$SPORT_NOT" ] && SRPORT_NOT="Not " || SRPORT_NOT=""
 SRPORT=$SRPORT_NOT`echo $P8 | tr [a-z] [A-Z]`
 SSTART_PORT=`echo $P8 | cut -f 1 -d :`
 SEND_PORT=`echo $P8 | cut -f 2 -d :`
 [ "$SSTART_PORT" = "$SEND_PORT" ] && SEND_PORT=""

 COMMENT=`echo $TMPLINE | sed s/.*#//`
 [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
 DCOMMENT=$COMMENT
}
#==================================
multi_line() {
 while [ -n "$1" ] ; do
	[ "$FIRST" != "S" ] && CONFIG_LINE=$CONFIG_LINE"\n"
	CONFIG_LINE=$CONFIG_LINE"access Y permit $2 $FORM_SRC_IP $FORM_DEST_IP $1 $FORM_COMMENT"
	FIRST="N"
	shift
	shift
 done
}
#==================================
mount_configuration() {
 CONFIG_LINE=""
 if [ "$FORM_METHOD" = "A" -o "$FORM_METHOD" = "F" ]; then
	FORM_ACTIVE=`echo "$FORM_ACTIVE" | tr [y,n] [Y,N]`
	[ -z "$FORM_RULET" ] && [ -z "$FORM_RULE" ] && FORM_RULE="DROP"
	[ ! -z "$FORM_RULET" ] && FORM_RULE="$FORM_RULET"
	[ -z "$FORM_PROTOA" ] && [ -z "$FORM_PROTO" ] && FORM_PROTO="all"
	[ ! -z "$FORM_PROTOA" ] && FORM_PROTO="$FORM_PROTOA"
	[ "$FORM_PROTO" != "tcp" ] && [ "$FORM_PROTO" != "udp" ] && [ "$FORM_PROTO" != "icmp" ] && FORM_START_PORT="" && FORM_END_PORT="" && FORM_PORT_NOT=""
	if [ "$FORM_SRC" = "ip" -a "$FORM_SRC" = "mac" -a -z "$FORM_SRC_IP" ] ; then
	 echo "<center><div id=alerta>$Pda</div></center>"
	 return
	fi
	if [ "$FORM_SRC" != "ip" ] ; then
	 if [ "$FORM_SRC" = "mac" ] ; then
		FORM_SRC_IP="mac:$FORM_SRC_IP"
	 else
		FORM_SRC_IP="$FORM_SRC"
	 fi
	fi
	[ "$FORM_SRC_NOT" = "not" -a "$FORM_SRC_IP" != "any" ] && FORM_SRC_IP="not:$FORM_SRC_IP"
	if [ "$FORM_DEST" = "ip" -a "$FORM_DEST" = "mac" -a -z "$FORM_DEST_IP" ] ; then
	 echo "<center><div id=alerta>$Pdb</div></center>"
	 return
	fi
	if [ "$FORM_DEST" != "ip" ] ; then
	 if [ "$FORM_DEST" = "mac" ] ; then
		FORM_DEST_IP="mac:$FORM_DEST_IP"
	 else
		FORM_DEST_IP="$FORM_DEST"
	 fi
	fi
	[ "$FORM_DEST_NOT" = "not" -a "$FORM_DEST_IP" != "any" ] && FORM_DEST_IP="not:$FORM_DEST_IP"
	[ -z "$FORM_START_PORT" ] && FORM_START_PORT="all"
	if [ ! -z "$FORM_END_PORT" ] && [ "$FORM_START_PORT" -gt "$FORM_END_PORT" ]; then
	 echo "<center><div id=alerta>$Pdc</div></center>"
	 return
	fi
	[ ! -z "$FORM_END_PORT" ] && FORM_START_PORT="${FORM_START_PORT}:${FORM_END_PORT}"
	[ ! -z "$FORM_PORT_NOT" ] && FORM_START_PORT="not:$FORM_START_PORT"
	[ -z "$FORM_SSTART_PORT" ] && FORM_SSTART_PORT="all"
	if [ ! -z "$FORM_SEND_PORT" ] && [ "$FORM_SSTART_PORT" -gt "$FORM_SEND_PORT" ]; then
	 echo "<center><div id=alerta>$Pdc</div></center>"
	 return
	fi
	[ ! -z "$FORM_SEND_PORT" ] && FORM_SSTART_PORT="${FORM_SSTART_PORT}:${FORM_SEND_PORT}"
	[ ! -z "$FORM_SPORT_NOT" ] && FORM_SSTART_PORT="not:$FORM_SSTART_PORT"
	[ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
	[ "$FORM_METHOD" = "A" ] && CONFIG_LINE="admin $FORM_ACTIVE $FORM_RULE $FORM_PROTO $FORM_SRC_IP $FORM_DEST_IP $FORM_START_PORT $FORM_SSTART_PORT $FORM_COMMENT"
	[ "$FORM_METHOD" = "F" ] && CONFIG_LINE="access $FORM_ACTIVE $FORM_RULE $FORM_PROTO $FORM_SRC_IP $FORM_DEST_IP $FORM_START_PORT $FORM_SSTART_PORT $FORM_COMMENT"
 fi
}
#==================================
show_list() {
#<td align="center" ><b>Line#</td>
cat << CLEOF
<table class=maintable border=0 width=100%>
<tr><th colspan=10>$Pdd</th></tr>
<tr>
<td class=header>$Faj</td>
<td class=header>$Fak</td>
<td class=header>$Fal</td>
<td class=header>$Paj</td>
<td class=header nowrap>$Fam</td>
<td class=header nowrap>$Fao</td>
<td class=header nowrap>$Fan</td>
<td class=header nowrap>$Fao</td>
<td class=header>$Fad</td>
<td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | while read TMPLINE; do
 LINECOUNT=$(($LINECOUNT+1))
 TMPLINE2=`echo "$TMPLINE" | cut -f 1 -d \# | tr [A-Z] [a-z]`
 case "$TMPLINE2" in
	\#*|"") continue ;;
	admin*|access*) treat_line $TMPLINE2; output_line; ;;
 esac
done
cat << CLEOF
</table><br>
<table class=maintable><tr><td>
<b>$Pde</td><td></b>[ <a href=$SCRIPT?ACTION=CALL_ADD&METHOD=A><u>$Pdf</u></a> &nbsp; | &nbsp;
<a href=$SCRIPT?ACTION=CALL_ADD&METHOD=F><u>$Pdg</u></a> ]<br></td></tr><tr><td>
<b>$Egf</td><td></b> [ <a href=$SCRIPT?ACTION=RELOAD> <u>$Pau</u></a> &nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/coyote/firewall&DESCFILE=Firewall Configuration"><u>$Pav</u></a> &nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/coyote/firewall.local&DESCFILE=Custom Firewall Rules"><u>$Pdh</u></a> ]
</td></tr></table>
<br>
CLEOF
}
#==================================
print_option () {
 if [ -n "$2" ] ; then
	desc_tag "$1"
	echo -n "<option value=$1"
	[ "$1" = "$SEL_TAG" ] && echo -n " selected"
	echo ">$DTAG</option>"
 fi
}
#==================================
address_options () {
 echo "<select name="$1">"
 [ "$1" = "SRC" ] &&	SEL_TAG="$SRC_TAG" || SEL_TAG="$DEST_TAG"
 print_option any		"forced"
 print_option ip		"forced"
 print_option mac		"forced"
 print_option lan-net	"$LOCAL_IPADDR"
 print_option lan-if		"$LOCAL_IPADDR"
 print_option lan		"$LOCAL_IPADDR"
 print_option lan2-net	"$LOCAL_IPADDR2"
 print_option lan2		"$LOCAL_IPADDR2"
 print_option lan3-net	"$LOCAL_IPADDR3"
 print_option lan3		"$LOCAL_IPADDR3"
 print_option int-net	"forced"
 print_option int-if		"forced"
 print_option int		"forced"
 print_option int2-net	"$IPADDR2"
 print_option int2		"$IPADDR2"
 print_option int3-net	"$IPADDR3"
 print_option int3		"$IPADDR3"
 print_option wan2-net	"$INET2_IPADDR"
 print_option wan2-if	"$INET2_IPADDR"
 print_option wan2		"$INET2_IPADDR"
 print_option wan3-net	"$INET3_IPADDR"
 print_option wan3-if	"$INET3_IPADDR"
 print_option wan3		"$INET3_IPADDR"
 print_option wan4-net	"$INET4_IPADDR"
 print_option wan4-if	"$INET4_IPADDR"
 print_option wan4		"$INET4_IPADDR"
 print_option dmz-net	"$DMZ_IPADDR"
 print_option dmz-if		"$DMZ_IPADDR"
 print_option dmz		"$DMZ_IPADDR"
 print_option dmz2-net	"$DMZ_IPADDR2"
 print_option dmz2		"$DMZ_IPADDR2"
 print_option dmz3-net	"$DMZ_IPADDR3"
 print_option dmz3		"$DMZ_IPADDR3"
 print_option local2-net	"$LOCAL2_IPADDR"
 print_option local2-if	"$LOCAL2_IPADDR"
 print_option local2		"$LOCAL2_IPADDR"
 print_option local3-net	"$LOCAL3_IPADDR"
 print_option local3-if	"$LOCAL3_IPADDR"
 print_option local3		"$LOCAL3_IPADDR"
 print_option local4-net	"$LOCAL4_IPADDR"
 print_option local4-if	"$LOCAL4_IPADDR"
 print_option local4		"$LOCAL4_IPADDR"
 print_option wlan-net	"$WLAN_IPADDR"
 print_option wlan-if	"$WLAN_IPADDR"
 print_option wlan		"$WLAN_IPADDR"
 echo "</select>"
}
#==================================
show_form() {
 [ "$METHOD" = "A" ] && FORMTITLE="$Pdi"|| FORMTITLE="$Pdj"
cat << CLEOF
<center>
<form method="POST" action="$SCRIPT"><input type=hidden value="$METHOD" name=METHOD><input type=hidden value="$LINE" name=LINE><input type=hidden value="$ACTION" name=ACTION>
<table  class=maintable border=0 width="100%"><tr><th colspan=2>$FORMTITLE</td></tr>
<tr><td class=row1 align=right><b>$Paz</b><br>$Pba</td>
  <td class=row2><input type=radio value=n name=ACTIVE `[ "$ACTIVE" = "n" ] && echo checked`>$Fno &nbsp;<input type=radio value=y name=ACTIVE `[ "$ACTIVE" != "n" ] && echo checked`>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Fal</b><br>$Pdk</td>
  <td class=row2><input type=radio name=RULE value=permit `[ "$RULE" = "permit" ] && echo checked`>$Fap &nbsp;<input type=radio name=RULE value=deny `[ "$RULE" = "deny" ] && echo checked`>$Faq<br>
  <input type=text name=RULET value="$RULET" size=17></td></tr>
<tr><td class=row1 align=right><b>$Paj</b><br>$Pbn</td>
  <td class=row2><select name=PROTOA><option value></option>
	<option value=all `[ "$PROTO" = "all" ] && echo selected`>ALL</option>
	<option value=tcp `[ "$PROTO" = "tcp" ] && echo selected`>TCP</option>
	<option value=udp `[ "$PROTO" = "udp" ] && echo selected`>UDP</option>
	<option value=icmp `[ "$PROTO" = "icmp" ] && echo selected`>ICMP</option>
	</select>&nbsp; $Far &nbsp;<input type=text name=PROTO value="$PROTON" size=5></td></tr>
<tr><td class=row1 align=right><b>$Pdl</b><br>$Pdm<br>$Pdn</td>
 <td class=row2><input value=not name=SRC_NOT type=checkbox `[ -n "$SRC_NOT" ] && echo " checked"`>Not</input></br>
        `address_options SRC`
        <br><input type=text name=SRC_IP value="$SRC_IP" size=22></td></tr>

<tr><td class=row1 align=right><b>$Pbp</b></td>
  <td class=row2><input value=not name=SPORT_NOT type=checkbox `[ -n "$SPORT_NOT" ] && echo " checked"`>Not</input></br>
	<input type=text name=SSTART_PORT value="$SSTART_PORT" size=22></td></tr>
<tr><td align=right class=row1><b>$Pbr ($Fop)</b></td>
 <td class=row2><input type=text name=SEND_PORT value="$SEND_PORT" size=22></td></tr>

<tr><td class=row1 align=right><b>$Pdo</b><br>$Pdp<br>$Pdq</td>
 <td class=row2><input value=not name=DEST_NOT type=checkbox `[ -n "$DEST_NOT" ] && echo " checked"`>Not</input></br>
        `address_options DEST`
        <br><input type=text name=DEST_IP value="$DEST_IP" size=22></td></tr>

<tr><td class=row1 align=right><b>$Pbp</b><br>$Pdr</td>
 <td class=row2><input value=not name=PORT_NOT type=checkbox `[ -n "$PORT_NOT" ] && echo " checked"`>Not</input></br>
        <input type=text name=START_PORT value="$START_PORT" size=22></td></tr>
<tr><td align=right class=row1><b>$Pbr ($Fop)</b><br>$Pbs</td>
 <td class=row2><input type=text name=END_PORT value="$END_PORT" size=22></td></tr>

<tr><td align=right class=row1><b>$Fad ($Fop)</b><br>$Pbt<br>$Pbu ($Pbw "Web01 HTTP").</td>
 <td class=row2><input type=text name=COMMENT value="$COMMENT" size=30></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;&nbsp;<input type=reset value="$Fer"></p>
</form></center>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Pdd - BrazilFW"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 mount_configuration
 if [ -n "$CONFIG_LINE" ] ; then
	if [ "$FORM_ACTION" = "ADD" ]; then
	 echo -e $CONFIG_LINE >> $FILE
	else
	 LINECOUNT=0
	 echo -n > $TMPFILE
	 cat $FILE | while read TMPLINE; do
		LINECOUNT=$(($LINECOUNT+1))
		if [ "$LINECOUNT" -ne "$FORM_LINE" ] ; then
		 echo "$TMPLINE" >> $TMPFILE
		else
		 echo $CONFIG_LINE >> $TMPFILE
		fi
	 done
	 rm -f $FILE
	 mv $TMPFILE $FILE
	 touch /tmp/need.save
	fi
	echo "<center><div id=back>$Pcn<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Pco</u></a><br><a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br>"
 fi
fi

case "$FORM_ACTION" in
 "DELETE")
	LINECOUNT=0
	echo -n > $TMPFILE
	cat $FILE | while read TMPLINE; do
	 LINECOUNT=$(($LINECOUNT+1))
	 [ "$LINECOUNT" -ne "$FORM_LINE" ] && echo "$TMPLINE" >> $TMPFILE
	done
	rm -f $FILE
	mv $TMPFILE $FILE
	touch /tmp/need.save
	echo "<center><div id=back>$Pcp<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Pco</u></a><br><a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br>"
	show_list
 ;;
 "CALL_EDIT")
	TMPLINE=`head -n $FORM_LINE $FILE | tail -n 1`
	TMPLINE2=`echo "$TMPLINE" | cut -f 1 -d \# | tr [A-Z] [a-z]`
	treat_line $TMPLINE2
	ACTION="EDIT"
	LINE=$FORM_LINE
	show_form
 ;;
 "CALL_ADD")
	METHOD=$FORM_METHOD
	ACTION="ADD"
	LINE=0
	ACTIVE="Y"
	RULE="permit"
	PROTO=""
	SRC_IP=""
	DEST_IP=""
	START_PORT=""
	END_PORT=""
	SSTART_PORT=""
	SEND_PORT=""
	show_form
 ;;
 "RELOAD")
	echo "<br><pre>"
	$RELOAD
	echo "</pre><center><div id=back><a href=$SCRIPT class=lnk><u>$Fbk</u></a></div></center><br>"
 ;;
 *) show_list ;;
esac

cl_footer2

