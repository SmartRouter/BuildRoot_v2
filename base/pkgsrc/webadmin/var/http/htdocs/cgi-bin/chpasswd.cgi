#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
cl_header2 "$Msp - BrazilFW"
if ! [ "$FORM_OKBTN" = "$Fsb" ]; then
cat << CLEOF
<form method="POST" action="/cgi-bin/chpasswd.cgi">
<table class=maintable border=0><tr><th colspan=2>$Wcp</th></tr>
<tr><td class=row1 align=right><b>$Wnp:</b></td><td class=row2><input type=password name=NEWPASS1 size=20></td></tr>
<tr><td class=row1 align=right><b>$Fcf $Wnp:</b></td><td class=row2><input type=password name=NEWPASS2 size=20></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p></form>
CLEOF
cl_footer2
exit
fi
if [ -z "$FORM_NEWPASS1" ]; then
        echo "<center><div id=alerta>$Caa</div></center>"
	cl_footer2
	exit
fi
if ! [ "$FORM_NEWPASS1" = "$FORM_NEWPASS2" ]; then
        echo "<center><div id=alerta>$Cab</div></center>"
	cl_footer2
	exit
fi
> /tmp/shadow.tmp
chmod 600 /tmp/shadow.tmp
NEWPASS="`/usr/bin/cryptpw $FORM_NEWPASS1`"
echo "root:${NEWPASS}:10091:0:99999:7:::" >> /tmp/shadow.tmp
cat /etc/shadow | while read PWDENT; do
	USERNAME=`echo "$PWDENT" | cut -f 1 -d ":"`
	if ! [ "$USERNAME" = "root" ]; then
		echo "$PWDENT" >> /tmp/shadow.tmp
	fi
done
cp /tmp/shadow.tmp /etc/shadow
chmod 600 /etc/shadow
rm /tmp/shadow.tmp
# Update the BrazilFW Configuration file entry
ADMIN_AUTH=`echo "${NEWPASS}" | cut -b 5-`
cl_rebuildconf
# Set the web administrator password
echo "root:${NEWPASS}" > /var/http/htdocs/cgi-bin/.htpasswd
echo "<center><div id=alerta>$Wsu</div></center>"
cl_footer2
