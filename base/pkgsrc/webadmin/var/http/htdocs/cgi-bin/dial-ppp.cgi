#!/bin/sh
# dial-ppp.cgi
. /var/http/web-functions
. /etc/coyote/coyote.conf
cl_header2 "SmartRouter Dial PPP Connection."
Cmd="/usr/sbin/ppp.dial"
echo "<table class=maintable><th colspan=2>Dial PPP Connection - $PPP_ISP</th></tr>"
echo "<tr><td><pre>"
$Cmd
echo "</pre></td></tr></table>"
cl_footer2
