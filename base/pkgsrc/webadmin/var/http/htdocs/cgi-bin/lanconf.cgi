#!/bin/sh

. /var/http/web-functions
. /etc/coyote/coyote.conf
. /tmp/netsubsys.state

SCRIPT="lanconf.cgi"

mount_configuration_1(){
 IF_LOCAL=$FORM_IF_LOCAL
 LOCAL_IPADDR=$FORM_IPADDR
 LOCAL_IPADDR2=$FORM_IPADDR2
 LOCAL_IPADDR3=$FORM_IPADDR3
 LOCAL_NETMASK=$FORM_NETMASK
 LOCAL_NETMASK2=$FORM_NETMASK2
 LOCAL_NETMASK3=$FORM_NETMASK3
 commit "LAN1"
}
mount_configuration_2(){
 IF_LOCAL2=$FORM_IF_LOCAL2
 LOCAL2_IPADDR=$FORM_LOCAL2_IPADDR
 LOCAL2_NETMASK=$FORM_LOCAL2_NETMASK
 commit "LAN2"
}
mount_configuration_3(){
 IF_LOCAL3=$FORM_IF_LOCAL3
 LOCAL3_IPADDR=$FORM_LOCAL3_IPADDR
 LOCAL3_NETMASK=$FORM_LOCAL3_NETMASK
 commit "LAN3"
}
mount_configuration_4(){
 IF_LOCAL4=$FORM_IF_LOCAL4
 LOCAL4_IPADDR=$FORM_LOCAL4_IPADDR
 LOCAL4_NETMASK=$FORM_LOCAL4_NETMASK
 commit "LAN4"
}
mount_configuration_W(){
 IF_WLAN=$FORM_IF_WLAN
 WLAN_IPADDR=$FORM_WLAN_IPADDR
 WLAN_NETMASK=$FORM_WLAN_NETMASK
 commit "WLAN"
}
mount_configuration_D(){
 [ -z "$FORM_IF_DMZ" ] && IF_DMZ="" || IF_DMZ=$FORM_IF_DMZ
 DMZ_IPADDR=$FORM_DIPADDR
 DMZ_IPADDR2=$FORM_DIPADDR2
 DMZ_IPADDR3=$FORM_DIPADDR3
 DMZ_NETMASK=$FORM_DNETMASK
 DMZ_NETMASK2=$FORM_DNETMASK2
 DMZ_NETMASK3=$FORM_DNETMASK3
 commit "DMZ"
}

commit(){
 cl_rebuildconf
. /usr/sbin/write_state.sh
 alert_lan $1
}

alert_lan(){
echo "<center><div id=alerta>$Lyn<br>
<a href=$SCRIPT?ACTION=$1 class=lnk><u>$Egj</u></a><br>
<a href=backup.cgi class=lnk><u>$Wtc</u></a></div></center><br><br>"
}

show_form_head(){
 init_table "maintable"
 init_add_control "$Lyf"
	add_control "$SCRIPT?ACTION=LAN1" "$Psc"
	add_control "$SCRIPT?ACTION=LAN2" "$Ptg"
	add_control "$SCRIPT?ACTION=LAN3" "$Pty"
	add_control "$SCRIPT?ACTION=LAN4" "$Ptz"
	add_control "$SCRIPT?ACTION=WLAN" "$Pth"
	add_control "$SCRIPT?ACTION=DMZ" "$Mdz"
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
 add_title "$Lyf"
	form_info_item "$Psc" "" "$(input_text "IF_LOCAL" "${IF_LOCAL}" "5")"
	form_info_item "$Lpi<br>$Wed $Anm" "" "$(input_text "IPADDR" "${LOCAL_IPADDR}" "20")<br>$(input_text "NETMASK" "${LOCAL_NETMASK}" "20")"
	form_info_item "($Wop) $Lpj<br>$Wed $Anm" "" "$(input_text "IPADDR2" "${LOCAL_IPADDR2}" "20")<br>$(input_text "NETMASK2" "${LOCAL_NETMASK2}" "20")"
	form_info_item "($Wop) $Lpk<br>$Wed $Anm" "" "$(input_text "IPADDR3" "${LOCAL_IPADDR3}" "20")<br>$(input_text "NETMASK3" "${LOCAL_NETMASK3}" "20")"
show_form_end "LAN1"
}

show_form_2(){
show_form_head
 add_title "$Pte"
	form_info_item "$Ptg" "" "$(input_text "IF_LOCAL2" "${IF_LOCAL2}" "5")"
	form_info_item "$Lpi<br> $Wed $Anm" "" "$(input_text "LOCAL2_IPADDR" "${LOCAL2_IPADDR}" "20")<br>$(input_text "LOCAL2_NETMASK" "${LOCAL2_NETMASK}" "20")" 
show_form_end "LAN2"
}

show_form_3(){
show_form_head
 add_title "$Ptv"
 	form_info_item "$Pty" "" "$(input_text "IF_LOCAL3" "${IF_LOCAL3}" "5")"
	form_info_item "$Lpi<br> $Wed $Anm" "" "$(input_text "LOCAL3_IPADDR" "${LOCAL3_IPADDR}" "20")<br>$(input_text "LOCAL3_NETMASK" "${LOCAL3_NETMASK}" "20")" 
show_form_end "LAN3"
}

show_form_4(){
show_form_head
 add_title "$Ptx"
	form_info_item "$Ptz" "" "$(input_text "IF_LOCAL4" "${IF_LOCAL4}" "5")"
	form_info_item "$Lpi<br> $Wed $Anm" "" "$(input_text "LOCAL4_IPADDR" "${LOCAL4_IPADDR}" "20")<br>$(input_text "LOCAL4_NETMASK" "${LOCAL4_NETMASK}" "20")"
show_form_end "LAN4"
}

show_form_W(){
show_form_head
 add_title "$Ptf"
	form_info_item "$Pth" "" "$(input_text "IF_WLAN" "${IF_WLAN}" "5")"
	form_info_item "$Lpi<br> $Wed $Anm" "" "$(input_text "WLAN_IPADDR" "${WLAN_IPADDR}" "20")<br>$(input_text "WLAN_NETMASK" "${WLAN_NETMASK}" "20")"
show_form_end "WLAN"
}
show_form_D(){
show_form_head
 add_title "$Mdz"
	form_info_item "$Pse" "" "$(input_text "IF_DMZ" "${IF_DMZ}" "5")"
	form_info_item "$Lpi<br>$Wed $Anm" "" "$(input_text "DIPADDR" "${DMZ_IPADDR}" "20")<br>$(input_text "DNETMASK" "${DMZ_NETMASK}" "20")"
	form_info_item "($Wop) $Lpj<br>$Wed $Anm" "" "$(input_text "DIPADDR2" "${DMZ_IPADDR2}" "20")<br>$(input_text "DNETMASK2" "${DMZ_NETMASK2}" "20")"
	form_info_item "($Wop) $Lpk<br>$Wed $Anm" "" "$(input_text "DIPADDR3" "${DMZ_IPADDR3}" "20")<br>$(input_text "DNETMASK3" "${DMZ_NETMASK3}" "20")"
show_form_end "DMZ"
}

cl_header2 "$Lyf"

case "$FORM_OKBTN" in
 "LAN1")
 if [ -z "$FORM_IPADDR" ] || [ -z "$FORM_NETMASK" ]; then
	echo "<center><div id=alerta>$Lym</div></center>"
	cl_footer2
	exit
 fi
	mount_configuration_1
 ;;
 "LAN2") mount_configuration_2 ;;
 "LAN3") mount_configuration_3 ;;
 "LAN4") mount_configuration_4 ;;
 "WLAN") mount_configuration_W ;;
 "DMZ") mount_configuration_D ;;
 *)  
	case "$FORM_ACTION" in
	 "LAN1") show_form_1 ;;
	 "LAN2") show_form_2 ;;
	 "LAN3") show_form_3 ;;
	 "LAN4") show_form_4 ;;
	 "WLAN") show_form_W ;;
	 "DMZ") show_form_D ;;
	 *)	show_form_1 ;;
	esac
 ;;
esac

cl_footer2
