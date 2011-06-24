#!/bin/sh
# LOCAL HOSTS CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 06/03/2004
# Edit - Fábio Leandro Janiszevski - fabiosammy - fabiosammy@gmail.com - 29/01/2010

. /etc/coyote/coyote.conf
. /var/http/web-functions

if [ "$INETTYPE" = "ETHERNET_DHCP" ] ; then
 [ -e "/etc/dhcpc/$IF_INET.info" ] && . /etc/dhcpc/$IF_INET.info
fi
[ -z "$DOMAINNAME" -a -n "$dhcp_domain" ] && DOMAINNAME="$dhcp_domain"
[ -z "$DOMAINNAME" -a -n "$DHCPD_DOMAIN" ] && DOMAINNAME="$DHCPD_DOMAIN"
[ -z "$DOMAINNAME" ] && DOMAINNAME="localdomain"

SCRIPT="localhosts.cgi"
FILE="/etc/hosts.dns"
TMPFILE="/tmp/hosts.dns"
RELOAD="/etc/rc.d/./rc.dnsmasq"

#==================================
treat_line() {
 IP=$1
 HOSTF=$2
 HOST=$3
 if [ -z "$3" ]; then
	[ "`echo $HOSTF | cut -f 1 -d .`" = "$HOSTF" ] && { HOST=$HOSTF; HOSTF=""; }
 fi
 DIP=$IP
 DHOSTF=$HOSTF
 DHOST=$HOST
 COMMENT=`echo "$TMPLINE" | sed s/.*#//`
 [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
 DCOMMENT=$COMMENT
}
#==================================
mount_configuration() {
 IP="$FORM_IP"
 HOSTF="$FORM_HOSTF"
 HOST="$FORM_HOST"
 COMMENT="$FORM_COMMENT"
 if [ -z "$HOSTF" -o -z "$HOST" ]; then
	TMPPAR="$HOSTF$HOST"
	[ "`echo $TMPPAR | cut -f 1 -d .`" = "$TMPPAR" ] && { HOST="$TMPPAR"; HOSTF=""; } || { HOST=""; HOSTF="$TMPPAR"; }
 fi
 [ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
 CONFIG_LINE="$IP $HOSTF $HOST $FORM_COMMENT"
}
#==================================
show_list() {
 init_table "maintable"
 add_new "$Lcc" "$Lcd"
 init_add_control "$Lce"
 add_control "$SCRIPT?ACTION=RELOAD" "$Egg"
 add_control "editconf.cgi?CONFFILE=/etc/hosts.dns&DESCFILE=Local Hosts File" "$Lcf"
 end_add_control
 return_page "$Faw" "dhcpconf.cgi" "$Egj"
 end_table
 echo "<br>"
 init_main_table
 add_title "$Lca" "4"
 header_table "IP" "$Lcb" "$Faz" "$Fad"
 LINECOUNT=0
 awk '{
	if ( $4 ~ /^#/ ){
	 COMMENT = substr($4,2)" "$5" "$6" "$7" "$8" "$9" "$10" "$11" "$12;
	 HOSTF = $2
	 HOST = $3
	} else if ( $3 ~ /^#/ ){
	 COMMENT = substr($3,2)" "$4" "$5" "$6" "$7" "$8" "$9" "$10" "$11;
	 HOSTF = "\."
	 HOST = $2
	} else if ( $2 !~ /\./ ){
	 COMMENT = "\."
	 HOST = $2
	 HOSTF = "\."
	} else {
	 COMMENT = substr($4,2)" "$5" "$6" "$7" "$8" "$9" "$10" "$11" "$12;
	 HOSTF = $2
	 HOST = $3
	}
 }{print $1" "HOSTF" "HOST" "COMMENT}' $FILE | while read IP HOSTF HOST COMMENT; do
	LINECOUNT=$(($LINECOUNT+1))
	case "$IP" in
	 \#*|"") continue;;
	 *)
		[ "$HOSTF" = "." ] && HOSTF=""
		[ "$COMMENT" = "." ] && COMMENT=""
		output_line "$IP" "$HOSTF" "$HOST" "$COMMENT"
	 ;;
	esac
 done
 end_table
}
#==================================
show_form() {
 init_form
 init_main_table
 add_title "$Lcg"
 form_info_item "$Ego" "$Lch" "$(input_text "IP" "$IP" "22")"
 form_info_item "$Ahs" "$Lci" "$(input_text "HOST" "$HOST" "22")"
 form_info_item "$Lcj ($Fop)" "$Lck" "$(input_text "HOSTF" "$HOSTF" "22")"
 form_info_item "$Fad ($Fop)" "$Lcl" "$(input_text "COMMENT" "$COMMENT" "30")"
 end_table
 end_form
}
#==================================
# MAIN ROUTINE
cl_header2 "$Lca"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 mount_configuration
 if [ -n "$CONFIG_LINE" ]; then
	[ "$FORM_ACTION" = "ADD" ] && addline "$CONFIG_LINE" $FILE || changeline $FORM_LINE "$CONFIG_LINE" $FILE
	alert "$Lcm" "$Egt"
 fi
fi

case "$FORM_ACTION" in
 "DELETE")
	deleteline "$FORM_LINE" $FILE
	alert "$Lcn" "$Egt"
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
 *) show_list;;
esac
cl_footer2
