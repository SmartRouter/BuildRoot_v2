#!/bin/sh
# hangup-ppp.cgi
. /var/http/web-functions
. /etc/coyote/coyote.conf
cl_header2 "SmartRouter Hangup PPP Connection"
Cmd="/usr/sbin/ppp.hangup"
echo "<table class=maintable width=100%><tr><th>Hangup PPP Connection<b></th></tr><tr><td><br><pre>"
$Cmd
echo "</pre></td></tr></table>"
cl_footer2
