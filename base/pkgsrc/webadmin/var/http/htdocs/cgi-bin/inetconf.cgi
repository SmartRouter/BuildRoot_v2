#!/bin/sh
# Revision by BFW user "marcos do vale" - 03/04/2008
# Build new cgi with ethernet, pppoe and ppp-conf.cgi

. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state

SCRIPT="inetconf.cgi"
mount_configuration_1() {
case $INETTYPE in
 "ETHERNET_DHCP")
	DHCPHOSTNAME=$FORM_DHCPHOSTNAME
	IPADDR=
	IPADDR2=
	IPADDR3=
	NETMASK=
	GATEWAY=
	MAC_SPOOFING=$FORM_MAC_SPOOFING
 ;;
 "ETHERNET_STATIC")
	IPADDR=$FORM_IPADDR
	IPADDR2=$FORM_IPADDR2
	IPADDR3=$FORM_IPADDR3
	NETMASK=$FORM_NETMASK
	NETMASK2=$FORM_NETMASK2
	NETMASK3=$FORM_NETMASK3
	GATEWAY=$FORM_GATEWAY
	MAC_SPOOFING=$FORM_MAC_SPOOFING
 ;;
 "PPPOE")
	[ "$FORM_DEMANDMODE" = "NO" ] && PPPOE_IDLE=NO || PPPOE_IDLE=$FORM_DEMANDTIME
	PPPOE_USERNAME=$FORM_USERNAME
	PPPOE_PASSWORD=$FORM_PASSWORD1
	IPADDR=
	IPADDR2=
	IPADDR3=
	NETMASK=
	GATEWAY=
	MAC_SPOOFING=
 ;;
 "PPP")
	[ "$FORM_DEMANDMODE" = "NO" ] && PPP_DEMANDDIAL=NO || PPP_DEMANDDIAL=$FORM_IDLETIME
	PPP_USERNAME=$FORM_USERNAME
	PPP_PASSWORD=$FORM_PASSWORD1
	PPP_CHATLOGIN=$FORM_CHATLOGIN
	PPP_PHONENUM=$FORM_PHONENUM
	PPP_INITSTR=$FORM_MODEMINIT
	PPP_MODEMTTY=$FORM_MODEMDEV
	PPP_PORTSPEED=$FORM_PORTSPEED
	[ "$FORM_STATIC" = "NO" ] && { PPP_STATICIP="NO";
	PPP_LOCALREMOTE=$FORM_LOCALREMOTE; } || \
	{ PPP_STATICIP=$FORM_STATICIP;
	PPP_LOCALREMOTE=; }
	PPP_CONFIG_OTF=YES
	[ -z "$PPP_USERNAME" -o -z "$PPP_PASSWORD" ] && echo "<center><div id=back>$Pmh<br><i>$Pmi</i></div></center><br>"
	[ -z "$PPP_PHONENUM" ] && echo "<center><div id=back>$Pmj<br><i>$Pmk</i></div></center><br>"
	[ -z "$PPP_MODEMTTY" ] && echo "<center><div id=back>$Pml<br><i>$Pmm</i></div></center><br>"
	[ -z "$PPP_LOCALREMOTE" ] && echo "<center><div id=back>$Pmn<br><i>$Pmo</i></div></center><br>"
 ;;
esac
IF_INET=$FORM_IF_INET
commit
alert_inet "WAN1"
}
mount_configuration_2(){
IF_INET2=$FORM_IF_INET2
INET2_IPADDR=$FORM_INET2_IPADDR
INET2_NETMASK=$FORM_INET2_NETMASK
INET2_GATEWAY=$FORM_INET2_GATEWAY
commit
alert_inet "WAN2"
}
mount_configuration_3(){
IF_INET3=$FORM_IF_INET3
INET3_IPADDR=$FORM_INET3_IPADDR
INET3_NETMASK=$FORM_INET3_NETMASK
INET3_GATEWAY=$FORM_INET3_GATEWAY
commit
alert_inet "WAN3"
}
mount_configuration_4(){
IF_INET4=$FORM_IF_INET4
INET4_IPADDR=$FORM_INET4_IPADDR
INET4_NETMASK=$FORM_INET4_NETMASK
INET4_GATEWAY=$FORM_INET4_GATEWAY
commit
alert_inet "WAN4"
}
mount_configuration_D(){
DOMAINNAME=$FORM_DOMAINNAME
DNS1=$FORM_DNS1
DNS2=$FORM_DNS2
DNS3=$FORM_DNS3
commit
alert_inet "DNS"
}

commit(){
cl_rebuildconf
. /usr/sbin/write_state.sh
}
alert_inet(){
echo "<center><div id=alerta>$Wsv<br>
<a href=$SCRIPT?ACTION=$1 class=lnk><u>$Egj</u></a><br>
<a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br><br>"
}

show_form_head(){
init_table "$SCRIPT"
 init_add_control "$Eia"
	add_control "$SCRIPT?ACTION=WAN1" "$Ptk"
	add_control "$SCRIPT?ACTION=WAN2" "$Ptl"
	add_control "$SCRIPT?ACTION=WAN3" "$Ptm"
	add_control "$SCRIPT?ACTION=WAN4" "$Ptn"
	add_control "$SCRIPT?ACTION=DNS" "DNS"
 end_add_control
end_table
init_form "$SCRIPT"
init_main_table
}

show_form_end(){
end_table
 echo "<p align=center><input type=submit value=\"$1\" name=OKBTN>&nbsp;<input type=reset value=\"$Fer\"></p></form>"
}

show_form_1(){
show_form_head
add_title "$Eia"
 form_info_item "$Icc" "" "$(init_combobox "INETTYPE") \
				$(add_item_combobox "ETHERNET_DHCP" "DHCP" "`[ "$INETTYPE" = "ETHERNET_DHCP" ] && echo selected`") \
				$(add_item_combobox "ETHERNET_STATIC" "STATIC" "`[ "$INETTYPE" = "ETHERNET_STATIC" ] && echo selected`") \
				$(add_item_combobox "PPPOE" "PPPOE" "`[ "$INETTYPE" = "PPPOE" ] && echo selected`") \
				$(add_item_combobox "PPP" "PPP" "`[ "$INETTYPE" = "PPP" ] && echo selected`")
			  $(end_combobox)"
add_title "$Ptk"
 case $INETTYPE in
	ETHERNET_DHCP)
	 form_info_item "$Psd" "" "$(input_text "IF_INET" "${IF_INET}" "5")"
	 form_info_item "$Ema $Emb" "" "$(input_text "DHCPHOSTNAME" "${DHCPHOSTNAME}" "20")"
	 form_info_item "$Efn" "$Euo" "$(input_text "MAC_SPOOFING" "${MAC_SPOOFING}" "20")"
	;;
	ETHERNET_STATIC)
	 form_info_item "$Psd" "" "$(input_text "IF_INET" "${IF_INET}" "5")"
	 form_info_item "$Lpi<br>$Wed $Anm" "" "$(input_text "IPADDR" "${IPADDR}" "20")<br>$(input_text "NETMASK" "${NETMASK}" "20")"
	 form_info_item "$Lpj<br>$Wed $Anm" "" "$(input_text "IPADDR2" "${IPADDR2}" "20")<br>$(input_text "NETMASK2" "${NETMASK2}" "20")"
	 form_info_item "$Lpk<br>$Wed $Anm" "" "$(input_text "IPADDR3" "${IPADDR3}" "20")<br>$(input_text "NETMASK3" "${NETMASK3}" "20")"
	 form_info_item "$Edg" "" "$(input_text "GATEWAY" "${GATEWAY}" "20")"
	 form_info_item "$Efn" "$Euo" "$(input_text "MAC_SPOOFING" "${MAC_SPOOFING}" "20")"
	;;
	PPPOE)
	 if [ "$PPPOE_IDLE" = "NO" ]; then
		CHK1=checked
		CHK2=
		IDLE=
	 else
		CHK1=
		CHK2=checked
		IDLE=$PPPOE_IDLE
	 fi
	 form_info_item "$Psd" "" "$(input_text "IF_INET" "${IF_INET}" "5")"
	 form_info_item "PPPoE $Ius" "" "$(input_text "USERNAME" "${PPPOE_USERNAME}" "20")"
	 form_info_item "PPPoE $Ips" "" "<input type=password name=PASSWORD1 value=\"${PPPOE_PASSWORD}\" size=20"
	 form_info_item "$Ioc" "$Iot" "$(input_radio "DEMANDMODE" "NO" "$Ikc" "${CHK1}")<br> \
	 			       $(input_radio "DEMANDMODE" "YES" "$Iuc" "${CHK2}")<br> \
	 			       $Itm $(input_text "DEMANDTIME" "${IDLE}" "4") $Wsc"
	;;
	PPP)
	 if [ "$PPP_DEMANDDIAL" = "NO" ]; then
		CHK1=checked
		CHK2=
		IDLE=
	 else
		CHK1=
		CHK2=checked
		IDLE=$PPP_DEMANDDIAL
	 fi
	 if [ "$PPP_CHATLOGIN" = "YES" ]; then
		CHK4=checked
		CHK3=
	 else
		CHK4=
		CHK3=checked
	 fi
	 if [ "$PPP_STATICIP" = "NO" ]; then
		CHK5=checked
		CHK6=
		STATICIP=
	 else
		CHK5=
		CHK6=checked
		STATICIP=$PPP_STATICIP
	 fi
	 form_info_item "$Pli" "$Plj" "$(input_text "MODEMDEV" "${PPP_MODEMTTY}" "16")"
	 form_info_item "$Plk" "$Plm" "$(input_text "PORTSPEED" "${PPP_PORTSPEED}" "16")"
	 form_info_item "$Pln" "$Plo 'ATZ' $Plp 'AT&FS11=55' $Plq" "$(input_text "MODEMINIT" "${PPP_INITSTR}" "16")"
	 form_info_item "$Plr" "$Pls" "$(input_text "PHONENUM" "${PPP_PHONENUM}" "16")"
	 form_info_item "$Ius" "$Plt" "$(input_text "USERNAME" "${PPP_USERNAME}" "16")"
	 form_info_item "$Ips" "$Plu" "<input type=password name=PASSWORD1 size=16 value=\"$PPP_PASSWORD\">"
	 form_info_item "$Plb" "$Plc $Pld" "$(input_radio "DEMANDMODE" "NO" "$Ple" "${CHK1}")<br> \
	 				    $(input_radio "DEMANDMODE" "YES" "$Plf" "${CHK2}")<br> \
	 				    $Plg $(input_text "IDLETIME" "${IDLE}" "4") $Plh"
	 form_info_item "$Plw" "$Plv ($Plx)" "$(input_radio "CHATLOGIN" "YES" "$Fye" "${CHK4}") \
	 				      $(input_radio "CHATLOGIN" "NO" "$Fno" "${CHK3}")"
	 form_info_item "$Pmb" "$Pmc" "$(input_radio "STATIC" "YES" "$Fye ($Pmd)<br>$Pme" "${CHK6}") \
	 			       $(input_text "STATICIP" "${STATICIP}" "16")<br> \
	 			       $(input_radio "STATIC" "NO" "$Fno ($Pmf)<br>$Pmg" "${CHK5}") \
	 			       $(input_text "LOCALREMOTE" "${PPP_LOCALREMOTE}" "16")"
	;;
 esac
show_form_end "WAN1"
}
show_form_2(){
show_form_head
add_title "$Ptl"
 form_info_item "$Psd" "" "$(input_text "IF_INET2" "${IF_INET2}" "5")"
 form_info_item "$Lpi,<br>$Anm<br>$Wed $Edg" "" "$(input_text "INET2_IPADDR" "${INET2_IPADDR}" "20")<br>$(input_text "INET2_NETMASK" "${INET2_NETMASK}" "20")<br>$(input_text "INET2_GATEWAY" "${INET2_GATEWAY}" "20")"
show_form_end "WAN2"
}
show_form_3(){
show_form_head
add_title "$Ptm"
 form_info_item "$Psd" "" "$(input_text "IF_INET3" "${IF_INET3}" "5")"
 form_info_item "$Lpi,<br>$Anm<br>$Wed $Edg" "" "$(input_text "INET3_IPADDR" "${INET3_IPADDR}" "20")<br>$(input_text "INET3_NETMASK" "${INET3_NETMASK}" "20")<br>$(input_text "INET3_GATEWAY" "${INET3_GATEWAY}" "20")"
show_form_end "WAN3"
}
show_form_4(){
show_form_head
add_title "$Ptn"
 form_info_item "$Psd" "" "$(input_text "IF_INET4" "${IF_INET4}" "5")"
 form_info_item "$Lpi,<br>$Anm<br>$Wed $Edg" "" "$(input_text "INET4_IPADDR" "${INET4_IPADDR}" "20")<br>$(input_text "INET4_NETMASK" "${INET4_NETMASK}" "20")<br>$(input_text "INET4_GATEWAY" "${INET4_GATEWAY}" "20")"
show_form_end "WAN4"
}
show_form_D(){
show_form_head
add_title "DNS"
 form_info_item "$Afs $Ids" "" "$(input_text "DNS1" "${DNS1}" "20")"
 form_info_item "$Afs $Ids" "" "$(input_text "DNS2" "${DNS2}" "20")"
 form_info_item "$Afs $Ids" "" "$(input_text "DNS3" "${DNS3}" "20")"
 form_info_item "$Edn" "" "$(input_text "DOMAINNAME" "${DOMAINNAME}" "20")"
show_form_end "DNS"
}

cl_header2 "$Ecf"
case "$FORM_OKBTN" in
 "WAN1") INETTYPE=$FORM_INETTYPE
	  mount_configuration_1 
		 ;;
 "WAN2") mount_configuration_2 ;;
 "WAN3") mount_configuration_3 ;;
 "WAN4") mount_configuration_4 ;;
 "DNS")	mount_configuration_D ;;
 *)  
	case "$FORM_ACTION" in
	 "WAN1") show_form_1 ;;
	 "WAN2") show_form_2 ;;
	 "WAN3") show_form_3 ;;
	 "WAN4") show_form_4 ;;
	 "DNS") show_form_D ;;
	 *)	show_form_1 ;;
	esac
 ;;
esac
cl_footer2

