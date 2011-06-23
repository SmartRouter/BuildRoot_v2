#!/bin/sh
# DHCP LEASES AND RESERVATIONS - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 07/03/2004
. /var/http/web-functions
SCRIPT="leases.cgi"
FILE_LEASE="/var/state/dhcp/dhcpd.leases"
TMPFILE_LEASE="/tmp/dhcpd.leases"
FILE="/etc/dhcpd.reservations"
TMPFILE="/tmp/dhcpd.reservations"
RELOAD="/etc/rc.d/rc.dnsmasq"
COLOR="row6"
#==================================
output_line_lease() {
  echo "<tr>"
  echo "<td class=$COLOR>$LDMAC</td>"
  echo "<td class=$COLOR>$LDHOST</td>"
  echo "<td class=$COLOR>$LDIP</td>"
  echo "<td class=$COLOR nowrap><a href=$SCRIPT?ACTION=DELETE_LEASE&LINE=$LINECOUNT>&nbsp;[$Fae]&nbsp;</a>&nbsp;"
  echo "<a href=$SCRIPT?ACTION=ADD_RESERVE&MAC=$LDMAC&IP=$LDIP&HOST=$LDHOST&TIME=infinite>&nbsp;[$Egc]&nbsp;</a></td>"
  echo "</tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
treat_line_lease() {
  LMAC=$2
  LIP=$3
  LHOST=$4
  LDMAC=$LMAC
  LDIP=$LIP
  LDHOST=$LHOST
}
#==================================
show_list_lease() {
cat << CLEOF
<table class=maintable width=100%><tr><th colspan=5>$Ega</th></tr>
<tr><td class=header>MAC</td><td class=header>$Ahs</td><td class=header>IP</td><td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE_LEASE | sed s/\*/\no_name/g | tr [A-Z] [a-z] | while read TMPLINE; do
#cat $FILE_LEASE | while read TMPLINE; do
  LINECOUNT=$(($LINECOUNT+1))
  TMPLINE2=`echo $TMPLINE | cut -f 1 -d \#`
  case "$TMPLINE" in
    \#*|"")
      continue ;;
    *)
      treat_line_lease $TMPLINE2
      output_line_lease ;;
  esac
done
echo "</table><br>"
}
#==================================
output_line() {
  echo "<tr>"
  echo "<td class=$COLOR>$DMAC</td>"
  echo "<td class=$COLOR>$DHOST</td>"
  echo "<td class=$COLOR>$DIP</td>"
  echo "<td class=$COLOR>$DTIME</td>"
  echo "<td class=$COLOR>$DCOMMENT</td>"
  echo "<td class=$COLOR nowrap><a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>&nbsp;[$Faf]&nbsp;</a>&nbsp;<a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>&nbsp;[$Fae]&nbsp;</a></td>"
  echo "</tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
treat_line2() {
  while [ -n "$1" ] ; do
    if [ "`echo $1 | cut -f 1 -d :`" != "$1" ] ; then
      MAC="$1"
    elif [ "`echo $1 | cut -f 1 -d .`" != "$1" ] ; then
      IP="$1"
    elif [ -z "$IP" -a -z "$HOST" ] ; then
      HOST="$1"
    else
      TIME="$1"
    fi
    shift
  done
}
#==================================
treat_line() {
  TLINE=`echo "$1" | cut -f 2 -d = | sed s/\,/\ /g`
  IP=""
  HOST=""
  MAC=""
  TIME=""
  treat_line2 $TLINE
  DIP=$IP
  DMAC=$MAC
  DHOST=$HOST
  DTIME=$TIME
  COMMENT=`echo "$TMPLINE" | sed s/.*#//`
  [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
  DCOMMENT=$COMMENT
}
#==================================
mount_configuration() {
  IP="$FORM_IP"
  MAC=`echo "$FORM_MAC" | tr [A-Z] [a-z]`
  HOST="$FORM_HOST"
  TIME="$FORM_TIME"
  COMMENT="$FORM_COMMENT"
  [ -n "$MAC" ] && MAC=",$MAC"
  [ -n "$HOST" ] && HOST=",$HOST"
  [ -n "$IP" ] && IP=",$IP"
  [ -n "$TIME" ] && TIME=",$TIME"
  [ -n "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
  CONFIG_LINE="$MAC$HOST$IP$TIME $FORM_COMMENT"
  CONFIG_LINE=`echo "$CONFIG_LINE" | sed s/\,/dhcp-host=/`
}
#==================================
show_list() {
cat << CLEOF
<table class=maintable width="100%"><tr><th colspan=6>$Egb</th></tr>
<tr><td class=header>MAC</td><td class=header>$Ahs</td><td class=header>IP</td><td class=header>$Fab</td><td class=header>$Fad</td><td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | while read TMPLINE; do
  LINECOUNT=$(($LINECOUNT+1))
  TMPLINE2=`echo $TMPLINE | cut -f 1 -d \#`
  case "$TMPLINE" in
    \#*|"")
      continue ;;
    dhcp-host=*)
      treat_line $TMPLINE2
      output_line ;;
  esac
done
cat << CLEOF
</table><br>
<table class=maintable><tr><td class=row1><b>$Egd</b></td><td class=row2>[&nbsp <a href=$SCRIPT?ACTION=CALL_ADD><u>$Ege</u></a>&nbsp;&nbsp;
| &nbsp;&nbsp;<a href=$SCRIPT><u>$Fag</u></a> &nbsp; ]</td></tr><tr><td class=row1>
<b>$Egf</b></td><td class=row2> [ &nbsp;<a href=$SCRIPT?ACTION=RELOAD><u>$Egg</u></a>&nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/dhcpd.reservations&DESCFILE=DHCP Reservations"><u>$Egh</u></a> ]</td></tr>
<tr><td class=row1><b>$Faw</b></td>
<td class=row2>[&nbsp <a href=dhcpconf.cgi><u>$Egj</u></a>&nbsp; ]</td></tr>
</table>
<br>
CLEOF
}
#==================================
show_form() {
FORMTITLE="$Egk"
cat << CLEOF
<form method="POST" action="$SCRIPT"><input type=hidden value="$LINE" name=LINE><input type=hidden value="$ACTION" name=ACTION>
<table class=maintable width="100%"><tr><th colspan=2>$FORMTITLE</th></tr>
<tr><td class=row1 align=right><b>$Egl ($Fop)</b><br>$Egm aa:aa:aa:aa:aa:aa .</td><td class=row2><input type=text name=MAC value="$MAC" size=22></td></tr>
<tr><td class=row1 align=right><b>$Ahs ($Fop)</b><br>$Egn</td><td class=row2><input type=text name=HOST value="$HOST" size=22></td></tr>
<tr><td class=row1 align=right><b>$Ego</b><br>$Eop</td><td class=row2><input type=text name=IP value="$IP" size=22></td></tr>
<tr><td class=row1 align=right><b>$Fab ($Fop)</b><br>$Egq</td><td class=row2><input type=text name=TIME value="$TIME" size=22></td></tr>
<tr><td class=row1 align=right><b>$Fad ($Fop)</b><br>$Egr</td><td class=row2><input type=text name=COMMENT value="$COMMENT" size=30></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;&nbsp;<input type=reset value="$Fer"></p>
</form>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Ebg"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
   mount_configuration
   if [ -n "$CONFIG_LINE" ] ; then
     if [ "$FORM_ACTION" = "ADD" ]; then
        echo -e $CONFIG_LINE >> $FILE
     else
       LINECOUNT=0
       echo -n > $TMPFILE
       cat $FILE | while read TMPLINE; do
         LINECOUNT=$(($LINECOUNT+1))
         if [ "$LINECOUNT" -ne "$FORM_LINE" ] ; then
           echo "$TMPLINE" >> $TMPFILE
         else
           echo $CONFIG_LINE >> $TMPFILE
         fi
       done
       rm -f $FILE
       mv $TMPFILE $FILE
       touch /tmp/need.save
     fi
     echo "<center><div id=back>$Egs<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Egt</u></a><br><a href=backup.cgi class=lnk><u>$Fah</u></a></div></center><br>"
   fi
fi
case "$FORM_ACTION" in
  "ADD_RESERVE")
     mount_configuration
     echo -e $CONFIG_LINE >> $FILE
     echo "<center><div id=back>$Egu<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Egt</u></a><br><a href=backup.cgi class=lnk><u>$Fah</u></a></div></center><br>"
     show_list_lease
     show_list
     ;;
  "DELETE_LEASE")
     LINECOUNT=0
     echo -n > $TMPFILE_LEASE
     cat $FILE_LEASE | while read TMPLINE; do
       LINECOUNT=$(($LINECOUNT+1))
       if [ "$LINECOUNT" -ne "$FORM_LINE" ] ; then
         echo "$TMPLINE" >> $TMPFILE_LEASE
       fi
     done
     rm -f $FILE_LEASE
     mv $TMPFILE_LEASE $FILE_LEASE
     touch /tmp/need.save
     echo "<center><div id=back>$Egv<br><a href=$SCRIPT?ACTION=RELOAD><u>$Egt</u></a><br><a href=backup.cgi class=lnk><u>$Fah</u></a></div></center><br>"
     show_list_lease
     show_list
     ;;
  "DELETE")
     LINECOUNT=0
     echo -n > $TMPFILE
     cat $FILE | while read TMPLINE; do
       LINECOUNT=$(($LINECOUNT+1))
       if [ "$LINECOUNT" -ne "$FORM_LINE" ] ; then
         echo "$TMPLINE" >> $TMPFILE
       fi
     done
     rm -f $FILE
     mv $TMPFILE $FILE
     touch /tmp/need.save
     echo "<center><div id=back>$Egx<br><a href=$SCRIPT?ACTION=RELOAD><u>$Egt</u></a><br><a href=backup.cgi class=lnk><u>$Fah</u></a></div></center><br>"
     show_list_lease
     show_list
     ;;
   "CALL_EDIT")
     TMPLINE=`head -n $FORM_LINE $FILE | tail -n 1`
     TMPLINE2=`echo $TMPLINE | cut -f 1 -d \#`
     treat_line $TMPLINE2
     ACTION="EDIT"
     LINE=$FORM_LINE
     show_form
     ;;
   "CALL_ADD")
     ACTION="ADD"
     LINE=0
     show_form
     ;;
   "RELOAD")
     echo "<br><center><pre>"
     $RELOAD
     echo "</pre></center><center><div id=back><a href=$SCRIPT class=lnk><u>$Fbl</u></a></div></center><br>"
    ;;
   *)
     show_list_lease
     show_list
     ;;
esac

cl_footer2
