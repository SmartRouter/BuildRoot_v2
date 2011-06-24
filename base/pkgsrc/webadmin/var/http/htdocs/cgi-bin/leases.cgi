#!/bin/sh
# DHCP LEASES AND RESERVATIONS - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 07/03/2004
. /var/http/web-functions
SCRIPT="leases.cgi"
FILE_LEASE="/var/state/dhcp/dhcpd.leases"
TMPFILE_LEASE="/tmp/dhcpd.leases"
FILE="/etc/dhcpd.reservations"
TMPFILE="/tmp/dhcpd.reservations"
RELOAD="/etc/rc.d/rc.dnsmasq"
#==================================
output_line_lease() {
 [ "$COLOR" = "row8" -o "$COLOR" = "" ] && COLOR="row6" || COLOR="row8"
 echo "   <tr>"
 for argnum in $(seq 1 $#); do
	eval $(echo "items_value=\$$argnum")
	items_value="$(echo "$items_value")"
	echo "      <td class=\"$COLOR\">$items_value</td>"
 done
 echo "      <td class=\"$COLOR\" nowrap><a href=$SCRIPT?ACTION=ADD_RESERVE&MAC=$LDMAC&IP=$LDIP&HOST=$LDHOST&TIME=infinite>&nbsp;[$Egc]&nbsp;</a>&nbsp;<a href=$SCRIPT?ACTION=DELETE_LEASE&LINE=$LINECOUNT>&nbsp;[$Fae]&nbsp;</a></td>"
 echo "   </tr>"
}
#==================================
treat_line_lease() {
 LMONTH=$2
 LDAY=$3
 LTIME=$4
 LYEAR=$6
}
#==================================
show_list_lease() {
 init_main_table
 add_title "$Ega" "5"
 header_table "Lease Expire" "MAC" "$Ahs" "IP"
 LINECOUNT=0
 sort $FILE_LEASE | sed s/\*/\no_name/g | tr [A-Z] [a-z] | while read LDTIME LDMAC LDIP LDHOST TRASH; do
	LINECOUNT=$(($LINECOUNT+1))
	TMPTIME="`date -D %s -d $LDTIME`"
	treat_line_lease $TMPTIME
	output_line_lease "$LDAY/$LMONTH/$LYEAR $LTIME" "$LDMAC" "$LDHOST" "$LDIP"
 done
 end_table
 echo "<br>"
}
#==================================
show_control() {
 init_table "maintable"
 init_add_control "$Egd"
 add_control "$SCRIPT?ACTION=CALL_ADD" "$Ege"
 add_control "$SCRIPT" "$Fag"
 end_add_control
 init_add_control "$Egf"
 add_control "$SCRIPT?ACTION=RELOAD" "$Egg"
 add_control "editconf.cgi?CONFFILE=/etc/dhcpd.reservations&DESCFILE=DHCP Reservations" "$Egh"
 end_add_control
 return_page "$Faw" "dhcpconf.cgi" "$Egj"
 end_table
 echo "<br>"
}
#==================================
treat_line2() {
 while [ -n "$1" ]; do
	if [ "`echo $1 | cut -f 1 -d :`" != "$1" ]; then
	 MAC="$1"
	elif [ "`echo $1 | cut -f 1 -d .`" != "$1" ]; then
	 IP="$1"
	elif [ -z "$IP" -a -z "$HOST" ] ; then
	 HOST="$1"
	else
	 TIME="$1"
	fi
	shift
 done
}
#==================================
treat_line() {
 TLINE=`echo "$1" | cut -f 2 -d = | sed s/\,/\ /g`
 IP=""
 HOST=""
 MAC=""
 TIME=""
 treat_line2 $TLINE
 DIP=$IP
 DMAC=$MAC
 DHOST=$HOST
 DTIME=$TIME
 COMMENT=`echo "$TMPLINE" | sed s/.*#//`
 [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
 DCOMMENT=$COMMENT
}
#==================================
mount_configuration() {
 IP="$FORM_IP"
 MAC=`echo "$FORM_MAC" | tr [A-Z] [a-z]`
 HOST="$FORM_HOST"
 TIME="$FORM_TIME"
 COMMENT="$FORM_COMMENT"
 [ -n "$MAC" ] && MAC=",$MAC"
 [ -n "$HOST" ] && HOST=",$HOST"
 [ -n "$IP" ] && IP=",$IP"
 [ -n "$TIME" ] && TIME=",$TIME"
 [ -n "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
 CONFIG_LINE="$MAC$HOST$IP$TIME $FORM_COMMENT"
 CONFIG_LINE=`echo "$CONFIG_LINE" | sed s/\,/dhcp-host=/`
}
#==================================
show_list() {
 init_main_table
 add_title "$Egb" "5"
 header_table "MAC" "$Ahs" "IP" "$Fab" "$Fad"
 VAZ="VAZIOVAZIOVAZIOVAZIO"
 LINECOUNT=0
 awk -vVAZ="$VAZ" '{
	if ( "$1" !~ /^#/ ){
	 INICIO=substr($1,11); MAC=VAZ; HOST=VAZ; IP=VAZ; TIME=VAZ; COMMENT=VAZ;
	 { if ( $2 != "" ) { COMMENT = substr($2,2)" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "$10" "$11" "$12" "$13 } }
	 search=","; n=split(INICIO,array,search);
	 { if ( substr(array[1],3,1) == ":" ) { MAC=array[1] } }
	 if ( MAC == VAZ ){
		if ( array[1] ~ /\./ ){ IP=array[1]; if ( array[2] != "" ) { TIME=array[2] }
		} else { IP=array[2]; HOST=array[1]; if ( array[3] != "" ) { TIME=array[3] } }
	 } else { 
		if ( array[2] ~ /\./ ){ IP=array[2]; if ( MAC == VAZ ) { HOST=array[1] } if ( array[3] != "" ) { TIME=array[3] }
		} else { IP=array[3]; HOST=array[2]; if ( array[4] != "" ) { TIME=array[4] } }
	 }
	}
 }{print $1" "MAC" "HOST" "IP" "TIME" "COMMENT}' $FILE | while read UMA MAC HOST IP TIME COMMENT; do
	LINECOUNT=$(($LINECOUNT+1))
	case "$UMA" in
	 dhcp-host=*) output_line "${MAC/$VAZ/}" "${HOST/$VAZ/}" "${IP/$VAZ/}" "${TIME/$VAZ/}" "${COMMENT/$VAZ/}";;
	esac
 done
 end_table
}
#==================================
show_form() {
 init_form
 init_main_table
 add_title "$Egk"
 form_info_item "$Egl ($Fop)" "$Egm aa:aa:aa:aa:aa:aa ." "$(input_text "MAC" "$MAC" "22")"
 form_info_item "$Ahs ($Fop)" "$Egn" "$(input_text "HOST" "$HOST" "22")"
 form_info_item "$Ego" "$Eop" "$(input_text "IP" "$IP" "22")"
 form_info_item "$Fab ($Fop)" "$Egq" "$(input_text "TIME" "$TIME" "22")"
 form_info_item "$Fad ($Fop)" "$Egr" "$(input_text "COMMENT" "$COMMENT" "30")"
 end_table
 end_form
}
#==================================
# MAIN ROUTINE
cl_header2 "$Ebg"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
	mount_configuration
	if [ -n "$CONFIG_LINE" ] ; then
	 [ "$FORM_ACTION" = "ADD" ] && addline "$CONFIG_LINE" $FILE || changeline $FORM_LINE "$CONFIG_LINE" $FILE
	 alert "$Egs" "$Egt"
	fi
fi
case "$FORM_ACTION" in
 "ADD_RESERVE")
	mount_configuration
	addline "$CONFIG_LINE" $FILE
	alert "$Egu" "$Egt"
	show_control
	show_list_lease
	show_list
 ;;
 "DELETE_LEASE")
	deleteline "$FORM_LINE" $FILE_LEASE
	alert "$Egv" "$Egt"
	show_control
	show_list_lease
	show_list
 ;;
 "DELETE")
	deleteline "$FORM_LINE" $FILE
	alert "$Egx" "$Egt" 
	show_control
	show_list_lease
	show_list
 ;;
 "CALL_EDIT")
	TMPLINE=`head -n $FORM_LINE $FILE | tail -n 1`
	TMPLINE2=`echo $TMPLINE | cut -f 1 -d \#`
	treat_line $TMPLINE2
	ACTION="EDIT"
	LINE=$FORM_LINE
	show_form
 ;;
 "CALL_ADD")
	ACTION="ADD"
	LINE=0
	show_form
 ;;
 "RELOAD") command_reload;;
 *)
	show_control
	show_list_lease
	show_list
 ;;
esac

cl_footer2
