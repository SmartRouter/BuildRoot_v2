#!/bin/sh
# CRON CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 05/15/2005
. /var/http/web-functions
. /etc/coyote/coyote.conf
SCRIPT="cron.cgi"
FILE="/var/spool/cron/crontabs/root"
TMPFILE="/tmp/cron"
RELOAD="/usr/sbin/cron.reload"
COLOR="row6"
if [ "$ENABLE_CRON" = "YES" ] ; then
  ENABLE_CRON_YES='checked'
else
  ENABLE_CRON_NO='checked'
fi
#==================================
output_line() {
  echo "<tr>"
  echo "<td class=$COLOR>$DMIN</td>"
  echo "<td class=$COLOR>$DHOR</td>"
  echo "<td class=$COLOR>$DDAY</td>"
  echo "<td class=$COLOR>$DMON</td>"
  echo "<td class=$COLOR>$DWEK</td>"
  echo "<td class=$COLOR nowrap>$SCR</td>"
  echo "<td class=$COLOR nowrap>"
  echo "&nbsp;[<a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>$Faf</a>]&nbsp;"
  echo "&nbsp;[<a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>$Fae</a>]&nbsp;"
  echo "</td></tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
treat_line() {
  MIN=$1
  shift
  HOR=$1
  shift
  DAY=$1
  shift
  MON=$1
  shift
  WEK=$1
  shift
  SCR=$@

  DMIN="$MIN"
  [ "$MIN" = 'all' ] && DMIN="$Pqk"
  DHOR="$HOR"
  [ "$HOR" = 'all' ] && DHOR="$Pqk"
  DDAY="$DAY"
  [ "$DAY" = 'all' ] && DDAY="$Pqk"
  DMON="$MON"
  [ "$MON" = 'all' ] && DMON="$Pqk"
  DWEK="$WEK"
  [ "$WEK" = 'all' ] && DWEK="$Pqk"

  FMIN="$MIN"
  [ "$MIN" = 'all' ] && FMIN=""
  FHOR="$HOR"
  [ "$HOR" = 'all' ] && FHOR=""
  FDAY="$DAY"
  [ "$DAY" = 'all' ] && FDAY=""
  FMON="$MON"
  [ "$MON" = 'all' ] && FMON=""
  FWEK="$WEK"
  [ "$WEK" = 'all' ] && FWEK=""
}
#==================================
mount_configuration() {
  MIN="$FORM_MIN"
  HOR="$FORM_HOR"
  DAY="$FORM_DAY"
  MON="$FORM_MON"
  WEK="$FORM_WEK"
  SCR="$FORM_SCR"
  [ -z "$MIN" ] && MIN='XaXlXlX'
  [ -z "$HOR" ] && HOR='XaXlXlX'
  [ -z "$DAY" ] && DAY='XaXlXlX'
  [ -z "$MON" ] && MON='XaXlXlX'
  [ -z "$WEK" ] && WEK='XaXlXlX'
  CONFIG_LINE="$MIN $HOR $DAY $MON $WEK $SCR"
}
#==================================
show_list() {
cat << CLEOF
<form method="POST" action="/cgi-bin/adminconf.cgi"><table class=maintable border=0 width="100%"><tr><th colspan=2>$Pjv</th></tr>
<tr><td width="50%" class=row1 align=right><b>$Ban</b></td><td class=row2><input type=radio value name=ENABLE_CRON ${ENABLE_CRON_NO}>$Fno &nbsp;<input type=radio value=YES name=ENABLE_CRON ${ENABLE_CRON_YES}>$Fye</td></tr></table>
<p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p></form>
CLEOF
cat << CLEOF
<table class=maintable border=0 width="100%"><tr><th colspan=7>$Msg</td></tr><tr class=row7>
<td class=header>$Pqa</td><td class=header>$Pqb</td><td class=header><b>$Pqc</td><td class=header>$Pqd</td>
<td class=header>$Pqe</td><td class=header>$Pqf</td><td class=header><b>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | sed s/\*/\all/g | while read TMPLINE; do
  LINECOUNT=$(($LINECOUNT+1))
  TMPLINE2=`echo $TMPLINE | cut -f 1 -d \#`
  case "$TMPLINE" in
    \#*|"")
      continue ;;
    *)
      treat_line $TMPLINE2
      output_line ;;
  esac
done
echo "</table><br>"
cat << CLEOF
<table class=maintable><tr><td><b>$Pqi</b></td><td>[&nbsp <a href=$SCRIPT?ACTION=CALL_ADD><u>$Pqj</u></a>&nbsp; ]</td></tr><tr><td>
<b>$Pat</b></td><td>[ &nbsp;<a href=$SCRIPT?ACTION=RELOAD><u>$Pqg</u></a>&nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=$FILE&DESCFILE=$Pjv"><u>$Pqh</u></a> ]</td></tr>
</table>
<br>
CLEOF
}
#==================================
show_form() {
FORMTITLE="$Msg"
cat << CLEOF
<form method="POST" action="$SCRIPT"><input type=hidden value="$LINE" name=LINE>
<input type=hidden value="$ACTION" name=ACTION><table class=maintable border=0 width="100%">
<tr><th colspan=2>$FORMTITLE</th></tr>
<tr><td width="100%" colspan=2 class=row3 align=center><b>$Pql<b></td></tr>
<tr><td align=right class=row1><b>$Pqa</b><br>$Pqm</td><td class=row2><input type=text name=MIN value="$FMIN" size=22></td></tr>
<tr><td align=right class=row1><b>$Pqb</b><br>$Pqn</td><td class=row2><input type=text name=HOR value="$FHOR" size=22></td></tr>
<tr><td align=right class=row1><b>$Pqc</b><br>$Pqo</td><td class=row2><input type=text name=DAY value="$FDAY" size=22></td></tr>
<tr><td align=right class=row1><b>$Pqd</b><br>$Pqp</td><td class=row2><input type=text name=MON value="$FMON" size=22></td></tr>
<tr><td align=right class=row1><b>$Pqe</b><br>$Pqq</td><td class=row2><input type=text name=WEK value="$FWEK" size=22></td></tr>
<tr><td align=right class=row1><b>$Pqf</b><br>$Pqr</td><td class=row2><input type=text name=SCR value="$SCR" size=40></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;&nbsp;<input type=reset  value="$Fer"></p></form>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Msg"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
   mount_configuration
   if [ -n "$CONFIG_LINE" ] ; then
     if [ "$FORM_ACTION" = "ADD" ]; then
        cp $FILE $TMPFILE
        echo -e $CONFIG_LINE >> $TMPFILE
        cat $TMPFILE | sed s/\XaXlXlX/\*/g > $FILE
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
       cat $TMPFILE | sed s/\XaXlXlX/\*/g > $FILE
       touch /tmp/need.save
     fi
     echo "<center><div id=back>$Pqs<br><a href=$SCRIPT?ACTION=RELOAD><u>$Pqu</u></a><br><a href=backup.cgi><u>$Fah</u></a></div></center>"
   fi
fi

case "$FORM_ACTION" in
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
     echo "<center><div id=back>$Pqt<br><a href=$SCRIPT?ACTION=RELOAD><u>$Pqu</u></a><br><a href=backup.cgi><u>$Fah</u></a></div></center>"
     show_list
     ;;
   "CALL_EDIT")
     TMPLINE=`head -n $FORM_LINE $FILE | tail -n 1 | sed s/\*/\all/g`
     treat_line $TMPLINE
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
     echo "<br><pre>"
     $RELOAD
     echo "</pre><center><div id=back><a href=$SCRIPT class=links><u>$Fbl</u></a></div></center>"
     ;;
   *)
     show_list
     ;;
esac

cl_footer2
