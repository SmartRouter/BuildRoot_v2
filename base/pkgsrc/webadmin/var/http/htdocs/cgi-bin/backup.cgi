#!/bin/sh
. /var/http/web-functions
cl_header2 "$Wbs - BrazilFW"
echo "<table class=maintable border=0 width=\"100%\"><tr><th>$Wsb</th></tr><tr><td><pre>"
/usr/sbin/lrcfg.back
echo "</pre></td></tr></table>"
cl_footer2
