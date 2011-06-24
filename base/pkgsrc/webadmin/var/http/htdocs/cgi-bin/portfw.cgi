#!/bin/sh
# PORT FORWADING CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 13/10/2003
# Edit - Fábio Leandro Janiszevski - fabiosammy - fabiosammy@gmail.com - 31/01/2010
. /var/http/web-functions
SCRIPT="portfw.cgi"
FILE="/etc/coyote/portforwards"
TMPFILE="/etc/coyote/porttemp"
RELOAD="/etc/rc.d/rc.firewall"
#==================================
treat_line() {
 if [ "$1" = "auto" ] ; then
	METHOD="A"
	ACTIVE=$2
	PROTO=$3
	INET_IP=""
	if [ "$3" != "tcp" -a "$3" != "udp" ]; then
	 DEST_IP=$4
	 DNS=$5
	 DINET_PORT=""
	 DDEST_PORT=""
	else
	 DEST_IP=$5
	 DNS=$6
	 START_PORT=`echo $4 | cut -f 1 -d :`
	 END_PORT=`echo $4 | cut -f 2 -d :`
	 [ "$START_PORT" = "$END_PORT" ] && DINET_PORT=$START_PORT || DINET_PORT=$4
	 DDEST_PORT=$DINET_PORT
	fi
 else
	METHOD="P"
	INET_IP=""
	ACTIVE=$2
	DEST_IP=$3
	if [ ! -z "$4" ] && [ "$4" != "tcp" -a "$4" != "udp" ]; then
	 INET_IP="$4"
	 shift
	fi
	PROTO=$4
	START_PORT=$5
	if [ "$6" = "dns" ]; then
	 END_PORT=$START_PORT
	 DNS=$6
	else
	 END_PORT=$6
	 DNS=$7
	fi
	[ -n "$DNS" -a "$DNS" != "dns" ] && DNS=""
	DINET_PORT=$START_PORT
	DDEST_PORT=$END_PORT
 fi
 DDEST_IP=$DEST_IP
 [ -z "$INET_IP" ] && DINET_IP="Any" || DINET_IP="$INET_IP"
 if [ "$PROTO" = "tcp" ] ; then DPROTO="TCP"; elif [ "$PROTO" = "udp" ] ; then DPROTO="UDP"; else DPROTO="$PROTO"; fi
 [ "$ACTIVE" = "y" ] && DACTIVE="Yes" || DACTIVE="No"
 [ "$DNS" = "dns" ] && DDNS="Yes" || DDNS="No"
 COMMENT=`echo $TMPLINE | sed s/.*#//`
 [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
 DCOMMENT=$COMMENT
}
#==================================
multi_line() {
 while [ -n "$1" ] ; do
	[ "$FIRST" != "S" ] && CONFIG_LINE=$CONFIG_LINE"\n"
	CONFIG_LINE=$CONFIG_LINE"auto Y $2 $1 $FORM_DEST_IP $FORM_DNS $FORM_COMMENT"
	FIRST="N"
	shift
	shift
 done
}
#==================================
mount_configuration() {
 CONFIG_LINE=""
 if [ "$FORM_METHOD" = "A" ]; then
	[ ! -z "$FORM_PROTON" ] && FORM_PROTO="$FORM_PROTON" && FORM_START_PORT="" && FORM_END_PORT=""
	if [ -z "$FORM_START_PORT" ] || [ -z "$FORM_DEST_IP" ] && [ "$FORM_PROTO" = "tcp" -o "$FORM_PROTO" = "udp" ]; then
	 echo "<center><div id=alerta>$Paa</div></center><br>"
	 return
	elif [ -z "$FORM_PROTON" ] || [ -z "$FORM_DEST_IP" ] && [ "$FORM_PROTO" != "tcp" -a "$FORM_PROTO" != "udp" ]; then
	 echo "<center><div id=alerta>$Pab</div></center><br>"
	 return
	fi
	if [ ! -z "$FORM_END_PORT" ] && [ "$FORM_START_PORT" -gt "$FORM_END_PORT" ]; then
	 echo "<center><div id=alerta>$Pac</div></center><br>"
	 return
	fi
	[ ! -z "$FORM_END_PORT" ] && FORM_START_PORT="${FORM_START_PORT}:${FORM_END_PORT}"
	[ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
	FORM_ACTIVE=`echo "$FORM_ACTIVE" | tr [y,n] [Y,N]`
	CONFIG_LINE="auto $FORM_ACTIVE $FORM_PROTO $FORM_START_PORT $FORM_DEST_IP $FORM_DNS $FORM_COMMENT"
 fi
 if [ "$FORM_METHOD" = "P" ]; then
	#if [ -z "$FORM_DEST_IP" -o -z "$FORM_END_PORT" ] ; then
	if [ -z "$FORM_DEST_IP" ]; then
	 echo "<center><div id=alerta>$Pad</div></center><br>"
	 return
	fi
	[ -z "$FORM_START_PORT" ] && FORM_START_PORT=$FORM_END_PORT
	if [ "$FORM_DNS" = "dns" ] && [ "$FORM_PROTO" = "" -o "$FORM_START_PORT" = "" -o "$FORM_END_PORT" = "" ]; then
	 echo "<center><div id=alerta>$Pae<br>$Paf</div></center><br>"
	 FORM_DNS=""
	fi
	[ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
	FORM_ACTIVE=`echo "$FORM_ACTIVE" | tr [y,n] [Y,N]`
	CONFIG_LINE="port $FORM_ACTIVE $FORM_DEST_IP $FORM_INET_IP $FORM_PROTO $FORM_START_PORT $FORM_END_PORT $FORM_DNS $FORM_COMMENT"
 fi
 if [ "$FORM_METHOD" = "W" ]; then
	if [ -z "$FORM_DEST_IP" ]; then
	 echo "<center><div id=alerta>$Pag</div></center><br>"
	 return
	fi
	[ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
	FIRST="S"
	multi_line $FORM_SERVICE
 fi
}
#==================================
show_list() {
 init_table "maintable"
 init_add_control "$Pap"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=P" "$Paq"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=A" "$Par"
 add_control "$SCRIPT?ACTION=CALL_ADD&METHOD=W" "$Pas"
 end_add_control
 init_add_control "$Pat"
 add_control "$SCRIPT?ACTION=RELOAD" "$Pau"
 add_control "editconf.cgi?CONFFILE=/etc/coyote/portforwards&DESCFILE=Port Forwarding Configuration" "$Pav"
 end_add_control
 end_table
 echo "<br>"
 init_main_table
 add_title "$Pah" "8"
 header_table "$Pai" "$Paj" "$Pak" "$Pal" "$Pam" "$Pan" "$Pao" "$Fad"
 LINECOUNT=0
 VAZ="VAZIOVAZIOVAZIOVAZIO"
 awk -vVAZ=$VAZ -vFno=$Fno -vFye=$Fye '{
	PROTO=VAZ; INET_IP=VAZ; DEST_IP=VAZ; DNS=VAZ; DINET_PORT=VAZ; DDEST_PORT=VAZ; DINET_IP=VAZ;
	{ if ( $2 == "N" ) { ACTIVE=Fno } else if ( $2 == "Y" ) { ACTIVE=Fye } }
 if ( $1 == "auto" ) {
	PROTO=$3;
	INET_IP=VAZ;
	if ( $3 != "tcp" && $3 != "udp" ){
	 DEST_IP=$4;
	 DNS=$5;
	 DINET_PORT=VAZ;
	 DDEST_PORT=VAZ;
	} else {
	 DEST_IP=$5;
	 DNS=$6;
	 search=":";
	 n=split($4,array,search)
	 { if ( array[1] == array[2] ) { DINET_PORT=array[1] } else { DINET_PORT=$4 } }
	 DDEST_PORT=DINET_PORT;
	}
 } else {
	INET_IP=VAZ;
	DEST_IP=$3;
	if ( ( $4 != "" ) && $4 != "tcp" && $4 != "udp" ){
	 INET_IP=$4;
	 PROTO=$5;
	 DINET_PORT=$6;
	 { if ( $7 == "dns" ){ DDEST_PORT=$6; DNS=$7; } else { DDEST_PORT=$7; DNS=$8; } }
	} else {
	 PROTO=$4;
	 DINET_PORT=$5;
	 { if ( $6 == "dns" ){ DDEST_PORT=$5; DNS=$6; } else { DDEST_PORT=$6; DNS=$7; } }
	}
	{ if ( DNS != "dns" && DNS != VAZ ) { DNS=VAZ; } }
 }
 DDEST_IP=DEST_IP;
 { if ( INET_IP == VAZ ) { DINET_IP="Any" } else { DINET_IP=INET_IP } }
 { if ( PROTO == "tcp" ) { DPROTO="TCP" } else if ( PROTO == "udp" ) { DPROTO="UDP" } else { DPROTO=PROTO } }
 { if ( DNS == "dns" ) { DDNS=Fye } else { DDNS=Fno } }
 COMMENT=$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "$10" "$11" "$12" "$13" "$14" "$15" "$16" "$17" "$18" "$19" "$20" "$21" "$22" "$23" "$24;
 search="#";
 n=split(COMMENT,array,search);
 COMMENT=array[2];
 }
 {print $1" "ACTIVE" "DPROTO" "DINET_IP" "DINET_PORT" "DDEST_IP" "DDEST_PORT" "DDNS" "COMMENT}' $FILE |
 while read FIRST DACTIVE DPROTO DINET_IP DINET_PORT DDEST_IP DDEST_PORT DDNS DCOMMENT; do
	LINECOUNT=$(($LINECOUNT+1))
	case "$FIRST" in
	 auto*|port*)
		output_line "$DACTIVE" "$DPROTO" "${DINET_IP//$VAZ/}" "${DINET_PORT//$VAZ/}" "${DDEST_IP//$VAZ/}" "${DDEST_PORT//$VAZ/}" "$DDNS" "$DCOMMENT"
	 ;;
	esac
 done
 end_table
}
#==================================
show_form() {
 init_form
 input_hidden "METHOD" "$METHOD"
 init_main_table
 [ "$METHOD" = "P" ] && add_title "$Pax" || add_title "$Pay"
 form_info_item "$Paz" "$Pba" "$(input_radio "ACTIVE" "n" "$Fno" "`[ "$ACTIVE" = "n" ] && echo checked`") $(input_radio "ACTIVE" "y" "$Fye" "`[ "$ACTIVE" = "y" ] && echo checked`")"
 if [ "$METHOD" = "P" ] ; then
	form_info_item "$Pbb" "$Pbc" "$(input_radio "PROTO" "tcp" "TCP" "`[ "$PROTO" = "tcp" ] && echo checked`") $(input_radio "PROTO" "udp" "UDP" "`[ "$PROTO" = "udp" ] && echo checked`")"
	form_info_item "$Pbd" "$Pbe" "$(input_text "DEST_IP" "$DEST_IP" "16")"
	form_info_item "$Pbf ($Fop)" "$Pbg" "$(input_text "END_PORT" "$END_PORT" "5")"
	form_info_item "$Pbh ($Fop)" "$Pbi<br>$Pbj" "$(input_text "INET_IP" "$INET_IP" "16")"
	form_info_item "$Pbk ($Fop)" "$Pbi<br>$Pbm" "$(input_text "START_PORT" "$START_PORT" "5")"
 else
	[ "$FORM_ACTION" = "CALL_EDIT" -a "$PROTO" != "tcp" -a "$PROTO" != "udp" ] && PROTON="$PROTO"
	[ "$FORM_ACTION" = "CALL_ADD" ] &&  PROTO="" && PROTON=""
	[ "$START_PORT" = "$END_PORT" ] && END_PORT=""
	form_info_item "$Pbb" "$Pbn" "$(input_radio "PROTO" "tcp" "TCP" "`[ "$PROTO" = "tcp" ] && echo checked`") $(input_radio "PROTO" "udp" "UDP" "`[ "$PROTO" = "udp" ] && echo checked`") # $(input_text "PROTON" "$PROTON" "3")"
	form_info_item "$Pbd" "$Pbo" "$(input_text "DEST_IP" "$DEST_IP" "16")"
	form_info_item "$Pbp" "$Pbq" "$(input_text "START_PORT" "$START_PORT" "5")"
	form_info_item "$Pbr ($Fop)" "$Pbs" "$(input_text "END_PORT" "$END_PORT" "5")"
 fi
 [ "$DNS" != "dns" ] && DNS=""
 form_info_item "$Pbt ($Frc)" "$Pbu<br>$Pbv" "$(input_radio "DNS" "" "$Fno" "`[ -z "$DNS" ] && echo checked`") $(input_radio "DNS" "dns" "$Fye" "`[ -n "$DNS" ] && echo checked`")"
 form_info_item "$Fad ($Fop)" "$Pbx<br>$Pby ($Pbw \"Web01 HTTP\")." "$(input_text "COMMENT" "$COMMENT" "30")"
 end_table
 end_form
}
#==================================
show_wizard() {
 init_form
 input_hidden "METHOD" "W"
 init_main_table
 add_title "$Pbz"
 form_info_item "$Pca" "$Pcb" "$(init_combobox "SERVICE")
 $(add_item_combobox "80 tcp" "http - $Pcc")
 $(add_item_combobox "443 tcp" "https - $Pcd")
 $(add_item_combobox "20:21 tcp" "ftp - $Pce")
 $(add_item_combobox "110 tcp" "pop3 - $Pcf")
 $(add_item_combobox "25 tcp" "smtp - $Pcg")
 $(add_item_combobox "53 udp 53 tcp" "dns - $Pci")
 $(add_item_combobox "23 tcp" "telnet - ($Fail)")
 $(add_item_combobox "113 tcp 113 udp" "ident - $Pcj")
 $(add_item_combobox "5900 tcp 5800 tcp" "VNC - $Pck")
 $(add_item_combobox "5631 tcp 5632 udp" "PCAnyWhere - $Pck")
 $(add_item_combobox "4662 tcp 4672 udp" "Emule - $Pcl")
 $(add_item_combobox "4663 tcp 4673 udp" "Emule - $Pcm")
 $(add_item_combobox "6881:6889 tcp" "BitTorrent P2P")
 $(end_combobox)"
 form_info_item "$Pbd" "$Pbe" "$(input_text "DEST_IP" "$DEST_IP" "16")"
 form_info_item "$Fad ($Fop)" "$Pbx<br>$Pdu ($Pbw \"Web01 HTTP\")." "$(input_text "COMMENT" "$COMMENT" "30")"
 end_table
 end_form
}
#==================================
# MAIN ROUTINE
cl_header2 "$Pah - SmartRouter"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 mount_configuration
 if [ -n "$CONFIG_LINE" ] ; then
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
	ACTIVE="y"
	DEST_IP=""
	INET_IP=""
	START_PORT=""
	END_PORT=""
	PROTO="tcp"
	DNS="dns"
	[ $FORM_METHOD = "W" ] && show_wizard || show_form
 ;;
 "RELOAD") command_reload;;
 *) show_list;;
esac

cl_footer2
