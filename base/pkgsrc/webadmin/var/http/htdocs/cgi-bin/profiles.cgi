#!/bin/sh
# CONFIGURATION PROFILES - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
. /var/http/web-functions
. /etc/coyote/coyote.conf
SCRIPT="profiles.cgi"
COLOR="row6"
#==================================
output_line() {
  echo "<tr><td class=$COLOR>"$DNAME"</td>"
  echo "<td class=$COLOR nowrap><a href=$SCRIPT?ACTION=LOAD&NAME=$DNAME>&nbsp;[$Pra]&nbsp;</a>"
  echo "<a href=$SCRIPT?ACTION=SAVE&NAME=$DNAME>&nbsp;[$Prc]&nbsp;</a><a href=$SCRIPT?ACTION=DELETE&NAME=$DNAME>&nbsp;[$Fae]&nbsp;</a></td>"
  echo "</tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
show_list() {
cat << CLEOF
<table class=maintable border=0 width="100%"><tr><th colspan=7>$Msh</th></tr><tr><td class=header>$Prd</td><td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
/usr/sbin/profile.list | while read TMPLINE; do
  DNAME="$TMPLINE"
  output_line
done
cat << CLEOF
</table><br><table class=maintable><tr><td class=row1><b>$Pid</b></td><td class=row2>[&nbsp <a href=$SCRIPT?ACTION=SAVE_AS><u>$Prb</u></a>&nbsp; ]</td></tr></table>
<br>
CLEOF
}
#==================================
show_form() {
FORMTITLE="$Msg"
cat << CLEOF
<form method="GET" action="$SCRIPT">
<table class=maintable><tr><td class=row1><input type=hidden value=SAVE name=ACTION><b>$Prk<br>$Prl</b><br></td></tr>
<tr><td class=row2><input type=text size=40 name=NAME>&nbsp;&nbsp;</td></tr></table><br><input type=submit value=&nbsp;$Fsv&nbsp;></form>
CLEOF
}
#==================================
ask_confirmation() {
cat << CLEOF
<CENTER><div id=back><br>
<form method="GET" action="$SCRIPT"><input type=hidden value="$FORM_ACTION" name=ACTION><input type=hidden value="$FORM_NAME" name=NAME>
<b>$Prd:</b> $FORM_NAME<br><br>
CLEOF
[ "$FORM_ACTION" = "DELETE" ] && echo "$Prj"
[ "$FORM_ACTION" = "SAVE" ]   && echo "$Prh"
[ "$FORM_ACTION" = "LOAD" ]   && echo "$Pre<br>$Prf"
cat << CLEOF
<br><br><input type=submit name=CONF value=$Fye><input type=submit name=CONF value=$Fno></FORM></div></CENTER><br>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Msh"
if [ "$FORM_CONF" = "$Fno" ] ; then
  FORM_ACTION="NONE"
  FORM_NAME=""
fi
case "$FORM_ACTION" in
  "DELETE")
     if [ "$FORM_CONF" = "$Fye" ] ; then
       echo "<center><pre>"
       /usr/sbin/profile.delete -y $FORM_NAME
       touch /tmp/need.save
       echo "</pre><div id=back><a href=$SCRIPT class=lnk>$Fbk</a></div></center><br>"
     else
       ask_confirmation
     fi
     ;;
   "SAVE_AS")
     show_form
     ;;
   "SAVE")
     if [ "$FORM_CONF" = "$Fye" ] ; then
       echo "<center><pre>"
       /usr/sbin/profile.save -y $FORM_NAME
       touch /tmp/need.save
       echo "</pre><div id=back><a href=$SCRIPT class=lnk>$Fbk</a></div></center><br>"
     else
       ask_confirmation
     fi
     ;;
   "LOAD")
     if [ "$FORM_CONF" = "$Fye" ] ; then
       echo "<center><pre>"
       /usr/sbin/profile.load -y $FORM_NAME
       touch /tmp/need.save
       echo "</pre><div id=back><a href=$SCRIPT class=lnk>$Fbk</a></div></center><br>"
     else
       ask_confirmation
     fi
     ;;
   *)
     show_list
     ;;
esac
cl_footer2
