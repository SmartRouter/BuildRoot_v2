#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state

SCRIPT="dhcpconf.cgi"
RELOAD="/etc/rc.d/rc.dnsmasq"
[ -z "$DNS_CACHE" ] && DNS_CACHE="150"
[ -z "$DNS_TTL" ] && DNS_TTL="60"
[ -z "$DHCPD_LMAX" ] && DHCPD_LMAX="150"
#==================================
mount_configuration() {
 if [ "$FORM_DHCPSERVER" = "YES" ]; then
	if [ -z "$FORM_DHCPD_START_IP" ] || [ -z "$FORM_DHCPD_END_IP" ]; then
	 echo "<center><div id=alerta>$Wth</div></center>"
	 cl_footer2
	 exit
	fi
 fi
 DHCPSERVER=$FORM_DHCPSERVER
 DHCPD_START_IP=$FORM_DHCPD_START_IP
 DHCPD_END_IP=$FORM_DHCPD_END_IP
 DHCPD_SUBNET=$FORM_DHCPD_SUBNET
 DHCPD_ROUTER=$FORM_DHCPD_ROUTER
 DHCPD_LEASE=$FORM_DHCPD_LEASE
 DHCPD_DOMAIN=$FORM_DHCPD_DOMAIN
 DHCPD_DNS1=$FORM_DHCPD_DNS1
 DHCPD_DNS2=$FORM_DHCPD_DNS2
 DHCPD_DNS3=$FORM_DHCPD_DNS3
 DHCPD_WINS1=$FORM_DHCPD_WINS1
 DHCPD_WINS2=$FORM_DHCPD_WINS2
 USE_DNS_CACHE=$FORM_DNSCACHE
 DNS_CACHE=$FORM_DNS_CACHE
 DNS_TTL=$FORM_DNS_TTL
 DHCPD_LMAX=$FORM_DHCPD_LMAX
 DHCPD_INAMES=$FORM_DHCPD_INAMES
 DHCPD_UCLIENT=$FORM_DHCPD_UCLIENT
 cl_rebuildconf
 echo "<br><pre>"
 $RELOAD
 echo "<pre><br>"
 echo "<center><div id=alerta>$Wta<br><b>$Wtl</b><br><a href=dhcpconf.cgi>[ $Fbk ]</a></div></center>"
 cl_footer2
 exit
}
#==================================
show_form() {
 [ "$DHCPSERVER" = "YES" ] && { CHK1= ; CHK2=checked; } || { CHK1=checked; CK2= ; }
 [ "$USE_DNS_CACHE" = "YES" ] && { CHK3= ; CHK4=checked; } || { CHK3=checked; CHK4= ; }
 [ "$DHCPD_INAMES" = "YES" ] && { CHK5= ; CHK6=checked; } || { CHK5=checked; CHK6= ; }
 [ "$DHCPD_UCLIENT" = "YES" ] && { CHK7= ; CHK8=checked; } || { CHK7=checked; CHK8= ; }
 init_table "maintable"
 init_add_control "$Egf"
 add_control "$SCRIPT?ACTION=RELOAD" "$Egg"
 add_control "editconf.cgi?CONFFILE=/etc/dnsmasq.conf.template&DESCFILE=DHCP Custom Configuration" "$Psa"
 end_add_control
 return_page "$Ebd" "localhosts.cgi" "$Ebe"
 return_page "$Ebf" "leases.cgi" "$Ebg"
 end_table
 echo "<br>"
 init_form
 init_main_table
 add_title "$Adc - $Fcg"
 form_info_item "$Eed" "$Ecd ($Frc)" "$(input_radio "DNSCACHE" "NO" "$Fno" "$CHK3") $(input_radio "DNSCACHE" "YES" "$Fye" "$CHK4")"
 form_info_item "Cache Size ($Frq)" "Specify the size of the cache in entries. The default is 150, the hard limit is 10000 and 0 disables caching." "$(input_text "DNS_CACHE" "$DNS_CACHE" "5")"
 form_info_item "Local TTL ($Frq)" "Specify time-to-live in seconds for replies from /etc/hosts." "$(input_text "DNS_TTL" "$DNS_TTL" "5")"
 add_title "$Ads - $Fcg"
 form_info_item "$Eds" "$Eha ($Frc)" "$(input_radio "DHCPSERVER" "NO" "$Fno" "${CHK1}") $(input_radio "DHCPSERVER" "YES" "$Fye" "${CHK2}")"
 form_info_item "Lease Limit ($Frq)" "Set the limit on DHCP leases, the default is 150." "$(input_text "DHCPD_LMAX" "$DHCPD_LMAX" "5")"
 form_info_item "Ignore Clients Names" "Ignore hostnames provided by DHCP clients." "$(input_radio "DHCPD_INAMES" "NO" "$Fno" "${CHK5}") $(input_radio "DHCPD_INAMES" "YES" "$Fye" "${CHK6}")"
 form_info_item "Block Unknow Clients" "Don't do DHCP to a unknow client (without ethernet address reserved)." "$(input_radio "DHCPD_UCLIENT" "NO" "$Fno" "${CHK7}") $(input_radio "DHCPD_UCLIENT" "YES" "$Fye" "${CHK8}")"
 add_title "$Ecz"
 form_info_item "$Esa ($Frq)" "$Efs" "$(input_text "DHCPD_START_IP" "${DHCPD_START_IP}" "20")"
 form_info_item "$Eei ($Frq)" "$Els" "$(input_text "DHCPD_END_IP" "${DHCPD_END_IP}" "20")"
 form_info_item "$Elt ($Fop)" "$Ebl" "$(input_text "DHCPD_LEASE" "${DHCPD_LEASE}" "20")"
 form_info_item "$Ert ($Fop)" "$Ebk ($Frc)" "$(input_text "DHCPD_ROUTER" "${DHCPD_ROUTER}" "20")"
 form_info_item "$Esn ($Fop)" "$Esm ($Frc)" "$(input_text "DHCPD_SUBNET" "${DHCPD_SUBNET}" "20")"
 form_info_item "$Edm ($Fop)" "$Eso ($Frc)" "$(input_text "DHCPD_DOMAIN" "${DHCPD_DOMAIN}" "20")"
 form_info_item "$Esp ($Fop)" "$Esr<br>$Ess ($Fop)" "$(input_text "DHCPD_DNS1" "${DHCPD_DNS1}" "20")<br>$(input_text "DHCPD_DNS2" "${DHCPD_DNS2}" "20")<br>$(input_text "DHCPD_DNS3" "${DHCPD_DNS3}" "20")"
 form_info_item "$Est ($Fop)" "$Eba<br>$Ebc" "$(input_text "DHCPD_WINS1" "${DHCPD_WINS1}" "20")<br>$(input_text "DHCPD_WINS2" "${DHCPD_WINS2}" "20")<br>$(input_text "DHCPD_WINS3" "${DHCPD_WINS3}" "20")"
 end_table
 end_form
}
#==================================
# MAIN ROUTINE
cl_header2 "$Mdh - SmartRouter"
[ "$FORM_OKBTN" = "$Fsb" ] && mount_configuration
[ "$FORM_ACTION" = "RELOAD" ] && command_reload || show_form
cl_footer2
