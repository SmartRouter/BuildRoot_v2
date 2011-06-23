#!/bin/sh
. /var/http/web-functions
cl_header2 "$Mpc - BrazilFW"
case "$FORM_OKBTN" in
	"$Wqo")
		echo "$Wrb ...<br>"
                echo "</body></html>"
		/usr/sbin/hangup.and.reboot
		exit 0
		;;
	"$Wso")
		echo "$Wpo ...<br></body></html>"
		/sbin/poweroff
		exit 0
		;;
	*)
if [ -r /tmp/need.save ]; then
	WARN_MSG="<center><b>$Wtd $Wsi</b></center>"
else
	WARN_MSG=
fi
cat << CLEOF
<center><form method="POST" action="/cgi-bin/reboot.cgi">${WARN_MSG}<br>
<table class=maintable border=0 width=400>
<tr><th>$Mpc - BrazilFW</th></tr>
<tr><td id=row4 align=center><b>$Wte</b> - $Wak - <b>$Wte</b></td></tr>
<tr><td align=center><input type=submit value="$Wqo" name=OKBTN> <input type=submit value="$Wso" name=OKBTN></td></tr>
</table></form></center>
CLEOF
	;;
esac

cl_footer2
