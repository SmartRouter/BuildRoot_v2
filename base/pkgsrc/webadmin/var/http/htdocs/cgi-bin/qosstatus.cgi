#!/bin/sh
# QOS status webadmin script
# Author: Dolly <dolly@czi.cz> 
. /var/http/web-functions
. /etc/qos.config
. /etc/coyote/coyote.conf
[ -e /tmp/netsubsys.state ] && . /tmp/netsubsys.state
INETIF=$IF_INET
if [ "$INETTYPE" = "PPP" -o "$INETTYPE" = "PPPOE" ]; then
   INETIF=ppp0
fi
cl_header2 "$Pik - SmartRouter"
echo "<table class=maintable width=100%><tr><th><b>$Pff</b></th></tr><tr><td class=row1><pre>"
echo "$Pil $QOS_TYPE"
if [ "$QOS_TYPE" != "DISABLED" -a "$QOS_TYPE" != "" ]; then
echo
echo "Downstream : ${QOS_DOWNSTREAM} kbit/s"
echo "Upstream   : ${QOS_UPSTREAM} kbit/s"
if [ "$QOS_TYPE" != "SUBNET" -a "$QOS_TYPE" != "CUSTOM" ]; then
echo
echo "$Pim ${QOS_HIGH_PRI_PER}%"
echo "$Pin ${QOS_NORM_PRI_PER}%"
echo "$Pio ${QOS_SLOW_PRI_PER}%"
echo ""
echo "$Pip ${QOS_UPFW_STREAM}%"
fi
echo ""
echo "$Piq ${QOS_DOWNSTREAM_JUNK}%"
echo "$Pir ${QOS_UPSTREAM_JUNK}%"
echo "</pre>"
if [ "$QOS_TYPE" = "COYOTE_DEFAULT" ]; then
echo "<b>Transffered data statistics</b><br><br>"
echo "<table border="0" cellspacing="1" width=100%><tr>"
echo "<td colspan=2 class=row6><b>$Pit</b></td></tr><tr>"
echo "<td class=row2 width=50%><b>$Piu<br>$Piw<br>$Piv</b></td>"
echo "<td class=row3><pre>"
/usr/sbin/tc -s qdisc show dev $IFINET | sed -n -e "/sfq 10[0,1,2]:/{n;p;}"
echo "</pre></td>"
echo "</tr></table>"
echo "<br>"
echo "<table border=0 cellspacing=1 width=100%><tr>"
echo "<td colspan=2 class=row6><b>$Pix</b></td></tr><tr>"
echo "<td class=row2 width=50%><b>$Piu<br>$Piw<br>$Piv</b></td>"
echo "<td class=row3><pre>"
/usr/sbin/tc -s qdisc show dev $IF_LOCAL | sed -n -e "/sfq 10[0,1,2]:/{n;p;}"
echo "</pre></td>"
echo "</tr></table>"
echo "<br>"
echo "<table border=0 cellspacing=1 width=100%><tr>"
echo "<td colspan=2 class=row6><b>$Piy</b></td></tr>"
echo "<tr><td class=row2 width=50%><b>$Piz</b></td>"
echo "<td class=row3><pre>"
/usr/sbin/tc -s class show dev $INETIF | sed -n -e "/htb 1:89/{n;p;}"
echo "</pre></td></tr>"
echo "<tr><td class=row2><b>$Pza</b></td>"
echo "<td class=row3><pre>"
/usr/sbin/tc -s class show dev $INETIF | sed -n -e "/htb 1:90/{n;p;}"
echo "</pre></td></tr>"
echo "</table>"
echo "<br>"
echo "<table border=0 cellspacing=1 width=100%><tr>"
echo "<td colspan=2 class=row6><b>$Pzb</b></td></tr>"
echo "<tr><td class=row2 width=50%><b>$Pzc</b></td>"
echo "<td class=row3><pre>"
/usr/sbin/tc -s class show dev $IF_LOCAL | sed -n -e "/htb 1:2/{n;p;}"
echo "</pre></td></tr>"
echo "<tr><td class=row2><b>$Pza</b></td>"
echo "<td class=row3><pre>"
/usr/sbin/tc -s class show dev $IF_LOCAL | sed -n -e "/htb 1:90/{n;p;}"
echo "</pre></td></tr>"
echo "</table>"
echo "<br>"
fi
 echo "<b>$Pzd</b>"
 echo "<pre>"
/usr/sbin/tc -s class show dev $IF_LOCAL
 echo "</pre>"
 echo "<b>$Pze</b>"
 echo "<pre>"
/usr/sbin/tc -s class show dev $INETIF
 echo "</pre>"
else
 echo "$Pzf"
fi
echo "</pre>"
echo "</td></tr></table>"
cl_footer2