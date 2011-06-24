#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf

main_form(){
init_form
 echo "<div align=\"center\">"
 init_table "maintable"
	add_title "$Wcp"
	form_info_item "$Wnp:" "" "<input type=password name=NEWPASS1 size=20>"
	form_info_item "$Fcf $Wnp:" "" "<input type=password name=NEWPASS2 size=20>"
 end_table
 echo "</div>"
end_form
}

cl_header2 "$Msp - SmartRouter"
if ! [ "$FORM_OKBTN" = "$Fsb" ]; then
 main_form
 cl_footer2
 exit
fi
if [ -z "$FORM_NEWPASS1" ]; then
 echo "<center><div id=alerta>$Caa</div></center>"
 main_form
 cl_footer2
 exit
fi
if ! [ "$FORM_NEWPASS1" = "$FORM_NEWPASS2" ]; then
 echo "<center><div id=alerta>$Cab</div></center>"
 main_form
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
# Update the SmartRouter Configuration file entry
ADMIN_AUTH=`echo "${NEWPASS}" | cut -b 5-`
cl_rebuildconf
# Set the web administrator password
echo "root:${NEWPASS}" > /var/http/htdocs/cgi-bin/.htpasswd
echo "<center><div id=alerta>$Wsu</div></center>"
cl_footer2
