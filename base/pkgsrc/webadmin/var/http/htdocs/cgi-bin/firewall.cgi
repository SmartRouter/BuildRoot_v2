#!/bin/sh
# ACCESS CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# Steve Eisner - seisner@comcast.net
# 2/12/2003
. /var/http/web-functions
SCRIPT="firewall.cgi"
FILE="/etc/coyote/firewall"
TMPFILE="/etc/coyote/acctemp"
RELOAD="/etc/rc.d/./rc.firewall"
#==================================
set_address() {
 PP="$1"
 NOT=`echo "$PP" | cut -c -3`
 [ "$NOT" = "not" ] && PP=`echo "$PP" | cut -c 5-` || NOT=""
 TAG=`echo "$PP" | cut -c -3`
 if [ "$TAG" = mac ]; then
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
 if [ "$PROTO" != "tcp" -a "$PROTO" != "udp" -a "$PROTO" != "all" -a "$PROTO" != "icmp" ]; then
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
 while [ -n "$1" ]; do
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
	if [ "$FORM_SRC" = "ip" -a "$FORM_SRC" = "mac" -a -z "$FORM_SRC_IP" ]; then
	 echo "<center><div id=alerta>$Pda</div></center>"
	 return
	fi
	if [ "$FORM_SRC" != "ip" ]; then
	 if [ "$FORM_SRC" = "mac" ]; then
		FORM_SRC_IP="mac:$FORM_SRC_IP"
	 else
		FORM_SRC_IP="$FORM_SRC"
	 fi
	fi
	[ "$FORM_SRC_NOT" = "not" -a "$FORM_SRC_IP" != "any" ] && FORM_SRC_IP="not:$FORM_SRC_IP"
	if [ "$FORM_DEST" = "ip" -a "$FORM_DEST" = "mac" -a -z "$FORM_DEST_IP" ]; then
	 echo "<center><div id=alerta>$Pdb</div></center>"
	 return
	fi
	if [ "$FORM_DEST" != "ip" ]; then
	 if [ "$FORM_DEST" = "mac" ]; then
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
 init_table "maintable"
 init_add_control "$Pde"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=A" "$Pdf"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=F" "$Pdg"
 end_add_control
 init_add_control "$Egf"
 add_control "$SCRIPT?ACTION=RELOAD" "$Pau"
 add_control "editconf.cgi?CONFFILE=/etc/coyote/firewall&DESCFILE=Firewall Configuration" "$Pav"
 add_control "editconf.cgi?CONFFILE=/etc/coyote/firewall.local&DESCFILE=Custom Firewall Rules" "$Pdh"
 end_add_control
 end_table
 echo "<br>"
 init_main_table
 add_title "$Pdd" "9"
 header_table "$Faj" "$Fak" "$Fal" "$Paj" "$Fam" "$Fao" "$Fan" "$Fao" "$Fad"
 LINECOUNT=0
 VAZ="VAZIOVAZIOVAZIO"
 awk -vFye=$Fye -vFno=$Fno -vVAZ=$VAZ -F"#" '{
    COMMENT=$2; LINHA=$1; search=" "; n=split(LINHA,array,search);
	TYPE=array[1];
	{ if ( array[2] == "Y" ) { DACTIVE=Fye } else { DACTIVE=Fno } }
    { if ( array[8] == "" ) { array8=VAZ } else { array8=array[8] } }
    }
	{print TYPE" "DACTIVE" "array[3]" "array[4]" "array[5]" "array[6]" "array[7]" "array8" "COMMENT}' $FILE | while read TYPE ACTIVE RULE PROTO P5 P6 P7 P8 COMMENT; do
	LINECOUNT=$(($LINECOUNT+1))
	case "$TYPE" in
	 admin*|access*)
 [ "$P8" = "$VAZ" ] && P8="" || P8=$P8

 set_address "$P5"
 [ -n "$NOT" ] && DNOT="Not " || DNOT=""
 desc_tag "$TAG"
 [ "$TAG" = "IP" ] && DTAG=""
 DSRC="$DNOT $DTAG $ADDRESS"

 set_address "$P6"
 [ -n "$NOT" ] && NOT="Not " || NOT=""
 desc_tag "$TAG"
 [ "$TAG" = "IP" ] && DTAG=""
 DDEST="$DNOT $DTAG $ADDRESS"

 PORT_NOT=`echo "$P7" | cut -c -3`
 [ "$PORT_NOT" = "not" ] && P7=`echo "$P7" | cut -c 5-` || PORT_NOT=""
 [ -n "$PORT_NOT" ] && DPORT_NOT="Not " || DPORT_NOT=""
 DPORT=$DPORT_NOT`echo $P7 | tr [a-z] [A-Z]`

 SPORT_NOT=`echo "$P8" | cut -c -3`
 [ "$SPORT_NOT" = "not" ] && P8=`echo "$P8" | cut -c 5-` || SPORT_NOT=""
 [ -n "$SPORT_NOT" ] && SRPORT_NOT="Not " || SRPORT_NOT=""
 SRPORT=$SRPORT_NOT`echo $P8 | tr [a-z] [A-Z]`

		output_line "$ACTIVE" "`echo $TYPE | tr [a] [A]`" "`echo $RULE | tr [p,d] [P,D]`" "`echo $PROTO | tr [a-z] [A-Z]`" "$DSRC" "$SRPORT" "$DDEST" "$DPORT" "$COMMENT"
        ;;
	esac
 done
 end_table
}
#==================================
print_option () {
 if [ -n "$2" ]; then
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
 echo "<center>"
 init_form
 input_hidden "METHOD" "$METHOD"
 init_main_table
 [ "$METHOD" = "A" ] && add_title "$Pdi" || add_title "$Pdj"
 form_info_item "$Paz" "$Pba" "$(input_radio "ACTIVE" "n" "$Fno" "`[ "$ACTIVE" = "n" ] && echo checked`") $(input_radio "ACTIVE" "y" "$Fye" "`[ "$ACTIVE" != "n" ] && echo checked`")"
 form_info_item "$Fal" "$Pdk" "$(input_radio "RULE" "permit" "$Fap" "`[ "$RULE" = "permit" ] && echo checked`") $(input_radio "RULE" "deny" "$Faq" "`[ "$RULE" = "deny" ] && echo checked`")<br>$(input_text "RULET" "$RULET" "17")"
 form_info_item "$Paj" "$Pbn" "$(init_combobox "PROTOA") $(add_item_combobox "" "" "") $(add_item_combobox "all" "ALL" "`[ "$PROTO" = "all" ] && echo selected`") $(add_item_combobox "tcp" "TCP" "`[ "$PROTO" = "tcp" ] && echo selected`") $(add_item_combobox "udp" "UDP" "`[ "$PROTO" = "udp" ] && echo selected`") $(add_item_combobox "icmp" "ICMP" "`[ "$PROTO" = "icmp" ] && echo selected`") $(end_combobox) $Far $(input_text "PROTO" "$PROTON" "5")"
 form_info_item "$Pdl" "$Pdm<br>$Pdn" "$(input_checkbox "SRC_NOT" "not" "Not" "`[ -n "$SRC_NOT" ] && echo " checked"`") `address_options SRC`<br> $(input_text "SRC_IP" "$SRC_IP" "22")"
 form_info_item "$Pbp" " " "$(input_checkbox "SPORT_NOT" "not" "Not" "`[ -n "$SPORT_NOT" ] && echo " checked"`")<br>$(input_text "SSTART_PORT" "$SSTART_PORT" "22")"
 form_info_item "$Pbr ($Fop)" " " "$(input_text "SEND_PORT" "$SEND_PORT" "22")"
 form_info_item "$Pdo" "$Pdp<br>$Pdq" "$(input_checkbox "DEST_NOT" "not" "Not" "`[ -n "$DEST_NOT" ] && echo " checked"`") `address_options DEST`<br> $(input_text "DEST_IP" "$DEST_IP" "22")"
 form_info_item "$Pbp" "$Pdr" "$(input_checkbox "PORT_NOT" "not" "Not" "`[ -n "$PORT_NOT" ] && echo " checked"`")<br>$(input_text "START_PORT" "$START_PORT" "22")"
 form_info_item "$Pbr ($Fop)" "$Pbs" "$(input_text "END_PORT" "$END_PORT" "22")"
 form_info_item "$Fad ($Fop)" "$Pbt<br>$Pbu ($Pbw \"Web01 HTTP\")." "$(input_text "COMMENT" "$COMMENT" "30")"
 end_table
 end_form
}
#==================================
# MAIN ROUTINE
cl_header2 "$Pdd - BrazilFW"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 mount_configuration
 if [ -n "$CONFIG_LINE" ]; then
	[ "$FORM_ACTION" = "ADD" ] && addline "$CONFIG_LINE" $FILE || changeline $FORM_LINE "$CONFIG_LINE" $FILE
	alert "$Pcn" "$Pco"
 fi
fi

case "$FORM_ACTION" in
 "DELETE")
	deleteline "$FORM_LINE" $FILE
	alert "$Pcp" "$Pco"
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
 "RELOAD") command_reload;;
 *) show_list;;
esac

cl_footer2

