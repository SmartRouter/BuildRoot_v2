#!/bin/sh
# Subnet Configuration Webadmin Script
# Author: Claudio Roberto Cussuol
# Changed to support subnet QOS in others LAN interfaces
# by BFW user "maeliseu" - Revision by BFW user "marcos do vale" - 08/04/2008
# Edit - Fábio Leandro Janiszevski - fabiosammy - fabiosammy@gmail.com - 31/01/2010      

. /var/http/web-functions
. /etc/coyote/coyote.conf
VERIFLOCAL2="teste"
VERIFLOCAL3="$IF_LOCAL3"
VERIFLOCAL4="$IF_LOCAL4"

SCRIPT="subnet.cgi"
FILE="/etc/coyote/subnet.cfg"
RELOAD="/etc/rc.d/rc.subnet"

list_lan() {
 [ ! -z $IF_LOCAL2 ] && echo "<option value=LAN2 `[ "$LAN" = "LAN2" ] && echo selected`>LAN2</option>"
 [ ! -z $IF_LOCAL3 ] && echo "<option value=LAN3 `[ "$LAN" = "LAN3" ] && echo selected`>LAN3</option>"
 [ ! -z $IF_LOCAL4 ] && echo "<option value=LAN4 `[ "$LAN" = "LAN4" ] && echo selected`>LAN4</option>" 
 [ ! -z $IF_WLAN ] && echo "<option value=WLAN `[ "$LAN" = "WLAN" ] && echo selected`>WLAN</option>" 
 [ ! -z $IF_DMZ ] && echo "<option value=DMZ `[ "$LAN" = "DMZ" ] && echo selected`>DMZ</option>" 
}
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
show_list() { 
 init_table "maintable"
 init_add_control "$Pid"
 add_control "$SCRIPT?ACTION=CALL_ADD" "$Psl"
 add_control "editconf.cgi?CONFFILE=$FILE&DESCFILE=Subnet Configuration File" "$Psm"
 add_control "$SCRIPT?ACTION=RELOAD" "Reload"
 end_add_control
 end_table
 echo "<br>"
 init_main_table
 add_title "$Psg" "14"
 header_table "$Faj" "$Psh" "$Aip" "$Anm" "$Psi" "$Psj" "$Phi" "$Phj" "$Phk" "$Phl" "LAN" "LAN ID" "CONN LIMIT" "$Fad"
 LINECOUNT=0
 awk -vFye=$Fye -vFno=$Fno -vPha=${Pha// /_} -vPhb=${Phb// /_} -vPhc=${Phc// /_} -vPhd=${Phd// /_} '{
	if ( substr($11,1,1) == "#" ){
	 LAN="LAN1";
	 LAN_ID=$3;
	 CONLIMIT=0;
	 COMMENT = substr($11,2)" "$12" "$13" "$14" "$15" "$16" "$17" "$18" "$19" "$20" "$21" "$22" "$23" "$24" "$25" "$26" "$27" "$28" "$29;   
	} else {
	 LAN=$12
	 LAN_ID=$13
	 CONLIMIT=$14;
	}
	if ( substr($14,1,1) == "#" ){
	 COMMENT = substr($14,2)" "$15" "$16" "$17" "$18" "$19" "$20" "$21" "$22" "$23" "$24" "$25" "$26" "$27" "$28" "$29;
	 CONLIMIT=0;
	} else {
	 COMMENT = substr($15,2)" "$16" "$17" "$18" "$19" "$20" "$21" "$22" "$23" "$24" "$25" "$26" "$27" "$28" "$29;
	 CONLIMIT=$14;
	}
	{ if ( $2 == "y" ) { ACTIVE=Fye } else if ( $2 == "n" ) { ACTIVE=Fno } }
	{ if ( $6 == "y" ) { DHCP=Fye } else if ( $6 == "n" ) { DHCP=Fno } }
	{ if ( $7 == "y" ) { QOS=Fye } else if ( $7 == "n" ) { QOS=Fno } }
	{ if ( $8 == "$COMP_DOWN" ) { DOWN_RATE = Pha } else if ( $8 == "$CLEAR_DOWNSTREAM" ) { DOWN_RATE = Phc } else { DOWN_RATE = $8"_kbits/s" } }
	{ if ( $9 == "$CLEAR_DOWNSTREAM" ) { DOWN_CEIL = Phc } else if ( $9 == "$COMP_DOWN" ) { DOWN_CEIL = Pha } else { DOWN_CEIL = $9"_kbits/s" } }
	{ if ( $10 == "$COMP_UP" ) { UP_RATE = Phb } else if ( $10 == "$CLEAR_UPSTREAM" ) { UP_RATE = Phd } else { UP_RATE = $10"_kbits/s" } }
	{ if ( $11 == "$CLEAR_UPSTREAM" ) { UP_CEIL = Phd } else if ( $11 == "$COMP_UP" ) { UP_CEIL = Phb } else { UP_CEIL = $11"_kbits/s" } }
	}
	{print $1" "ACTIVE" "$3" "$4" "$5" "DHCP" "QOS" "DOWN_RATE" "DOWN_CEIL" "UP_RATE" "UP_CEIL" "LAN" "LAN_ID" "CONLIMIT" "COMMENT}' $FILE | 
	while read FIRST DACTIVE ID IP MASK DDHCP DQOS DDOWN_RATE DDOWN_CEIL DUP_RATE DUP_CEIL LAN LAN_ID CONLIMIT DCOMMENT ; do
	 LINECOUNT=$(($LINECOUNT+1))
	 find_lan $LAN
	 case "$FIRST" in
		subnet*) output_line "$DACTIVE" "$ID" "$IP" "$MASK" "$DDHCP" "$DQOS" "${DDOWN_RATE//_/ }" "${DDOWN_CEIL//_/ }" "${DUP_RATE//_/ }" "${DUP_CEIL//_/ }" "$LAN" "$LAN_ID" "$CONLIMIT" "$DCOMMENT";;
	 esac
 done
 end_table
}
#==================================
show_form() {
 if [ -z "$ID" ]; then
	LASTLINE=`grep subnet $FILE | tail -n 1`
	[ -n "$LASTLINE" ] && treat_line $LASTLINE
	ID=$(($LASTID+1))
	IP=
 fi
 CONLIMIT=0
 [ -z "$DOWN_RATE" ] && NDOWN_RATE='' && SDOWN_RATE='Individual Download'
 [ -z "$DOWN_CEIL" ] && NDOWN_CEIL='' && SDOWN_CEIL='Total Download'
 [ -z "$UP_RATE" ] && NUP_RATE='' && SUP_RATE='Individual Upload'
 [ -z "$UP_CEIL" ] && NUP_CEIL='' && SUP_CEIL='Total Upload'
 init_form
 init_main_table
 add_title "$Psg"
 form_info_item "$Paz" "$Pba" "$(input_radio "ACTIVE" "n" "$Fno" "`[ "$ACTIVE" = "n" ] && echo checked`")$(input_radio "ACTIVE" "y" "$Fye" "`[ "$ACTIVE" != "n" ] && echo checked`")"
 form_info_item "$Psh" "$Psn" "$(input_text "ID" "$ID" "5")"
 form_info_item "$Aip" "$Pso" "$(input_text "IP" "$IP" "20")"
 form_info_item "$Anm" "$Psp" "$(input_text "MASK" "$MASK" "20")"
 form_info_item "$Psi" "$Psq" "$(input_radio "DHCP" "n" "$Fno" "`[ "$DHCP" = "n" ] && echo checked`") $(input_radio "DHCP" "y" "$Fye" "`[ "$DHCP" != "n" ] && echo checked`")"
 form_info_item "$Psj" "$Psr" "$(input_radio "QOS" "n" "$Fno" "`[ "$QOS" = "n" ] && echo checked`") $(input_radio "QOS" "y" "$Fye" "`[ "$QOS" != "n" ] && echo checked`")"
 form_info_item "$Phi" "$Phv  $Phw" "$(input_text "NDOWN_RATE" "$NDOWN_RATE" "4") kbits/s $Far<br> $(init_combobox "SDOWN_RATE") $(add_item_combobox "" "" "") $(add_item_combobox "'COMP_DOWN'" "$Phx" "`[ "$SDOWN_RATE" = \"Individual Download\" ] && echo selected`")$(add_item_combobox "'CLEAR_DOWNSTREAM'" "$Phy" "`[ "$SDOWN_RATE" = \"Total Download\" ] && echo selected`") $(end_combobox)" 
 form_info_item "$Phj" "$Phz  $Phw" "$(input_text "NDOWN_CEIL" "$NDOWN_CEIL" "4") kbits/s $Far<br> $(init_combobox "SDOWN_CEIL") $(add_item_combobox "" "" "") $(add_item_combobox "'COMP_DOWN'" "$Phx" "`[ "$SDOWN_CEIL" = \"Individual Download\" ] && echo selected`")$(add_item_combobox "'CLEAR_DOWNSTREAM'" "$Phy" "`[ "$SDOWN_CEIL" = \"Total Download\" ] && echo selected`") $(end_combobox)" 
 form_info_item "$Phk" "$Phv  $Phw" "$(input_text "NUP_RATE" "$NUP_RATE" "4") kbits/s $Far<br> $(init_combobox "SUP_RATE") $(add_item_combobox "" "" "") $(add_item_combobox "'COMP_UP'" "$Phb" "`[ "$SUP_RATE" = \"Individual Upload\" ] && echo selected`")$(add_item_combobox "'CLEAR_UPSTREAM'" "$Phd" "`[ "$SUP_RATE" = \"Total Upload\" ] && echo selected`") $(end_combobox)" 
 form_info_item "$Phl" "$Phz  $Phw" "$(input_text "NUP_CEIL" "$NUP_CEIL" "4") kbits/s $Far<br> $(init_combobox "SUP_CEIL") $(add_item_combobox "" "" "") $(add_item_combobox "'COMP_UP'" "$Phb" "`[ "$SUP_CEIL" = \"Individual Upload\" ] && echo selected`")$(add_item_combobox "'CLEAR_UPSTREAM'" "$Phd" "`[ "$SUP_CEIL" = \"Total Upload\" ] && echo selected`") $(end_combobox)" 
 form_info_item "LAN" " " "$(init_combobox "LAN") $(add_item_combobox "LAN1" "LAN1" "`[ "$LAN" = "LAN1" ] && echo selected`") $(list_lan) $(end_combobox)"
 form_info_item "ID da LAN" " " "$(input_text "LAN_ID" "$LAN_ID" "5")"
 form_info_item "CONLIMIT" " " "$(input_text "CONLIMIT" "$CONLIMIT" "5")"
 form_info_item "$Fad ($Fop)" "$Pss" "$(input_text "COMMENT" "$COMMENT" "30")"
 end_table
 end_form
}
#==================================
# MAIN ROUTINE
cl_header2 "$Psg - SmartRouter"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 mount_configuration
 if [ -n "$CONFIG_LINE" ]; then
	[ "$FORM_ACTION" = "ADD" ] && addline "$CONFIG_LINE" $FILE || changeline $FORM_LINE "$CONFIG_LINE" $FILE
	alert "$Pst" "$Psv"
 fi
fi

case "$FORM_ACTION" in
 "DELETE")
	deleteline "$FORM_LINE" $FILE
	alert "$Psu" "$Psv"
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
 "RELOAD") command_reload;;
 *) show_list;;
esac
cl_footer2
