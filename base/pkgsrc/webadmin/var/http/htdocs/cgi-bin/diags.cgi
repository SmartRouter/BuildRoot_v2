#!/bin/sh
# Source the Web Functions
. /var/http/web-functions

add_link(){
echo "<li><a href=\"/cgi-bin/diags.cgi?COMMAND=$2\">$1</a></li>"
}

cl_header2 "$Mdt - SmartRouter"
if [ -n "$FORM_COMMAND" ] ; then
 COMMAND=$FORM_COMMAND
 echo "<table class=maintable><tr><td nowrap>"
	if [ -n "$FORM_PARAMNAME" ] ; then
	 echo "<center><form method=POST action=/cgi-bin/diags.cgi>"
	 echo "$FORM_PARAMNAME"
	 echo "&nbsp;:&nbsp;"
	 echo "<input type=text size=30 name=PARAM value=\"$FORM_PARAM\">&nbsp;&nbsp;"
	 echo "<input type=submit value=&nbsp;$Feo&nbsp;>"
	 echo "<input type=hidden name=COMMAND value=\"$FORM_COMMAND\">"
	 echo "<input type=hidden name=PARAMNAME value=\"$FORM_PARAMNAME\"></form></center>"
	 echo "</td></tr><tr><td nowrap>"
	 COMMAND=`echo $COMMAND | sed s/MARK_param_MARK/$FORM_PARAM/`
	fi
 echo "<pre>"
 [ -n "$FORM_PARAM" -o -z "$FORM_PARAMNAME" ] && $COMMAND
 echo "</pre></td></tr></table>"
else 
init_table "maintable"
add_title "$Mdt"
echo "<tr><td><br><ol>"
 add_link "$Pka" "logread"
 add_link "$Pkb" "/usr/sbin/showcfg -w"
 add_link "$Pkc" "ps"
 add_link "PING" "ping -c 4 MARK_param_MARK&PARAMNAME=IP Number or Host Name"
 add_link "$Pkd" "nslookup MARK_param_MARK&PARAMNAME=Host Name"
 add_link "$Pke" "/sbin/ifconfig -a"
 add_link "$Pkf" "/usr/sbin/dns.test"
 add_link "$Pkg" "/usr/sbin/gateway.test"
 add_link "$Pkh" "/usr/sbin/iptables -L -n -v"
 add_link "$Pkh - NAT" "/usr/sbin/iptables -L -t nat -n -v"
 add_link "$Pkh - MANGLE" "/usr/sbin/iptables -L -t mangle -n -v"
 add_link "$Pki" "dmesg"
 add_link "$Pkj" "lsmod"
 add_link "$Pkk" "route"
 add_link "$Pkl" "cat /proc/meminfo"
 add_link "$Pkm" "df -h"
 add_link "$Pkn" "cat /proc/net/arp"
 add_link "$Pko" "cat /proc/net/ip_conntrack"
 add_link "$Psb" "cat /proc/pci"
 add_link "$Pue" "/usr/sbin/lsnet"
 add_link "$Puf" "/sbin/lshw -disable ide -html"
 add_link "$Pug" "/usr/sbin/changeboot -info"
 add_link "$Puh" "/usr/sbin/changeboot -showdevice"
 add_link "$Pui" "/usr/sbin/detecthds"
echo "</ol></td></tr>"
end_table
fi
cl_footer2
