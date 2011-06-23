#!/bin/sh
# QOS classes configuration webadmin script
# Author: Claudio Roberto Cussuol
. /var/http/web-functions
SCRIPT="qosclasses.cgi"
FILE="/etc/coyote/qos.classes"
TMPFILE="/etc/coyote/qostemp"
RELOAD="/etc/rc.d/rc.qos"
COLOR="row6"
#==================================
output_line() {
  echo "<tr>"
  echo "<td class=$COLOR>$DTYPE</td>"
  echo "<td class=$COLOR>$DROOTID</td>"
  echo "<td class=$COLOR>$DCLSID</td>"
  echo "<td class=$COLOR nowrap>$DDOWN_RATE</td>"
  echo "<td class=$COLOR nowrap>$DDOWN_CEIL</td>"
  echo "<td class=$COLOR nowrap>$DUP_RATE</td>"
  echo "<td class=$COLOR nowrap>$DUP_CEIL</td>"
  echo "<td class=$COLOR>$DMATCHIP</td>"
  echo "<td class=$COLOR nowrap>$DCOMMENT</td>"
  echo "<td class=$COLOR nowrap><a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>&nbsp;[$Faf]&nbsp;</a><a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>&nbsp;[$Fae]&nbsp;</a></td></tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
treat_rate() {
  DRATE=
  NRATE=
  SRATE=
  case $1 in
    '$COMP_DOWN')
    	SRATE="$Pha"
    	DRATE=$SRATE ;;
    '$COMP_UP')
    	SRATE="$Phb"
    	DRATE=$SRATE ;;
    '$CLEAR_DOWNSTREAM')
    	SRATE="$Phc"
    	DRATE=$SRATE ;;
    '$CLEAR_UPSTREAM')
    	SRATE="$Phd"
    	DRATE=$SRATE ;;
    *)
        NRATE=$1
	DRATE="$1 kbit/s" ;;
  esac
}
#==================================
treat_line() {
  TYPE=$1
  ROOTID=$2
  CLSID=$3
  DOWN_RATE=$4
  DOWN_CEIL=$5
  UP_RATE=$6
  UP_CEIL=$7
  MATCHIP=$8
  [ "$TYPE" = "define_class_qos" ] && DTYPE=Filtered
  [ "$TYPE" = "define_class_sfq" ] && DTYPE=Simple
  DROOTID=`echo $ROOTID | sed s/\"//g`
  DCLSID=`echo $CLSID | sed s/\"//g`
  treat_rate $DOWN_RATE
  DDOWN_RATE=$DRATE
  NDOWN_RATE=$NRATE
  SDOWN_RATE=$SRATE
  treat_rate $DOWN_CEIL
  DDOWN_CEIL=$DRATE
  NDOWN_CEIL=$NRATE
  SDOWN_CEIL=$SRATE
  treat_rate $UP_RATE
  DUP_RATE=$DRATE
  NUP_RATE=$NRATE
  SUP_RATE=$SRATE
  treat_rate $UP_CEIL
  DUP_CEIL=$DRATE
  NUP_CEIL=$NRATE
  SUP_CEIL=$SRATE
  DMATCHIP=$MATCHIP
  COMMENT=`echo $TMPLINE | sed s/.*#//`
  [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
  DCOMMENT=$COMMENT
}
#==================================
mount_configuration() {
  ROOTID='"'$FORM_ROOTID'"'
  CLSID='"'$FORM_CLSID'"'
  DOWN_RATE=$FORM_NDOWN_RATE
  DOWN_CEIL=$FORM_NDOWN_CEIL
  UP_RATE=$FORM_NUP_RATE
  UP_CEIL=$FORM_NUP_CEIL
  [ -z $DOWN_RATE ] && DOWN_RATE='$'$FORM_SDOWN_RATE
  [ -z $DOWN_CEIL ] && DOWN_CEIL='$'$FORM_SDOWN_CEIL
  [ -z $UP_RATE ] && UP_RATE='$'$FORM_SUP_RATE
  [ -z $UP_CEIL ] && UP_CEIL='$'$FORM_SUP_CEIL
  CONFIG_LINE="$FORM_TYPE $ROOTID $CLSID $DOWN_RATE $DOWN_CEIL $UP_RATE $UP_CEIL $FORM_MATCHIP #$FORM_COMMENT"
}
#==================================
show_list() { #<td align="center" ><b>Line#</td>
cat << CLEOF
<table class=maintable border=0 width="100%"><tr><th colspan=10>$Phe</th></tr>
<tr><td class=header>$Phf</td><td class=header>$Phg</td><td class=header>$Phh</td><td class=header>$Phi</td>
<td class=header>$Phj</td><td class=header>$Phk</td><td class=header>$Phl</td><td class=header>$Phm</td>
<td class=header>$Fad</td><td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | tr [\\] [\|] | while read TMPLINE; do
  LINECOUNT=$(($LINECOUNT+1))
  case "$TMPLINE" in
    \#*|"")
      continue ;;
    define_class_sfq*|define_class_qos*)
      treat_line $TMPLINE
      output_line ;;
  esac
done
cat << CLEOF
</table><br>
<table class=maintable><tr><td class=row1><b>$Pic</td><td class=row2></b>[ &nbsp;<a href=$SCRIPT?ACTION=CALL_ADD><u>$Pfh</u></a>&nbsp; ]</td></tr>
<tr><td class=row1><b>$Pid</b></td><td class=row2>[ &nbsp;<a href=$SCRIPT?ACTION=RELOAD><u>$Pfi</u></a>&nbsp; | &nbsp;<a href="qosstatus.cgi"><u>$Pfj</u></a> &nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/coyote/qos.classes&DESCFILE=QOS Classes File"><u>$Phn</u></a>&nbsp; ]</td></tr>
<tr><td class=row1><b>$Faw</b></td><td class=row2>[&nbsp <a href=qos.cgi><u>$Pgc</u></a>&nbsp; ]</td></tr>
</table></form>
CLEOF
}
#==================================
show_form() {
FORMTITLE="$Phe"
[ -z "$TYPE" ] && TYPE=define_class_qos
[ -z "$DROOTID" ] && DROOTID='1:1'
[ -z "$DOWN_RATE" ] && NDOWN_RATE='' && SDOWN_RATE='Individual Download'
[ -z "$DOWN_CEIL" ] && NDOWN_CEIL='' && SDOWN_CEIL='Total Download'
[ -z "$UP_RATE" ] && NUP_RATE='' && SUP_RATE='Individual Upload'
[ -z "$UP_CEIL" ] && NUP_CEIL='' && SUP_CEIL='Total Upload'
cat << CLEOF
<form method="POST" action="$SCRIPT"><input type=hidden value="$LINE" name=LINE><input type=hidden value="$ACTION" name=ACTION>
<table class=maintable width=100%><tr><th colspan=2>$FORMTITLE</th></tr>
<tr><td class=row1 align=right><b>$Phf</b><br><small>$Pho  $Phq</small></td>
 <td class=row2><input type=radio name=TYPE value=define_class_qos `[ "$TYPE" = "define_class_qos" ] && echo checked`>$Phr
 <input type=radio name=TYPE value=define_class_sfq `[ "$TYPE" = "define_class_sfq" ] && echo checked`>$Phs</td></tr>
<tr><td class=row1 align=right><b>$Phg</b><br><small>$Pht</small></td><td clas=row2><input type=text name=ROOTID value="$DROOTID" size=10></td></tr>
<tr><td class=row1 align=right><b>$Phh</b><br><small>$Phu</small></td><td class=row2><input type=text name=CLSID value="$DCLSID" size=10></td></tr>
<tr><td class=row1 align=right><b>$Phi</b><br><small>$Phv  $Phw</small></td><td class=row2><input type=text name=NDOWN_RATE value="$NDOWN_RATE" size=4>&nbsp; kbits/s $Far<br>
 <select name=SDOWN_RATE><option value></option><option value='COMP_DOWN' `[ "$SDOWN_RATE" = "Individual Download" ] && echo selected`>$Phx</option>
 <option value='CLEAR_DOWNSTREAM' `[ "$SDOWN_RATE" = "Total Download" ] && echo selected`>$Phy</option></select></td></tr>
<tr><td class=row1 align=right><b>$Phj</b><br><small>$Phz  $Phw</small></td><td class=row2><input type=text name=NDOWN_CEIL value="$NDOWN_CEIL" size=4>&nbsp; kbits/s $Far<br>
 <select name=SDOWN_CEIL><option value></option><option value='COMP_DOWN' `[ "$SDOWN_CEIL" = "Individual Download" ] && echo selected`>$Phx</option>
 <option value='CLEAR_DOWNSTREAM' `[ "$SDOWN_CEIL" = "Total Download" ] && echo selected`>$Phy</option></select></td></tr>
<tr><td class=row1 align=right><b>$Phk</b><br><small>$Phv  $Phw</small></td><td class=row2><input type=text name=NUP_RATE value="$NUP_RATE" size=4>&nbsp; kbits/s $Far<br>
 <select name=SUP_RATE><option value></option><option value='COMP_UP' `[ "$SUP_RATE" = "Individual Upload" ] && echo selected`>$Phb</option>
 <option value='CLEAR_UPSTREAM' `[ "$SUP_RATE" = "Total Upload" ] && echo selected`>$Phd</option></select></td></tr>
<tr><td class=row1 align=right><b>$Phl</b><br><small>$Phz  $Phw</small></td><td class=row2><input type=text name=NUP_CEIL value="$NUP_CEIL" size=4>&nbsp; kbits/s $Far<br>
 <select name=SUP_CEIL><option value></option><option value='COMP_UP' `[ "$SUP_CEIL" = "Individual Upload" ] && echo selected`>$Phb</option>
 <option value='CLEAR_UPSTREAM' `[ "$SUP_CEIL" = "Total Upload" ] && echo selected`>$Phd</option></select></td></tr>
<tr><td class=row1 align=right><b>$Pia</b><br><small>$Pie</small></td><td class=row2><input type=text name=MATCHIP value="$MATCHIP" size=20></td></tr>
<tr><td class=row1 align=right><b>$Fad ($Fop)</b><br><small>$Pif</small></td><td class=row2><input type=text name=COMMENT value="$COMMENT" size=30></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p>
</form>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Phe - BrazilFW"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
   mount_configuration
   if [ -n "$CONFIG_LINE" ] ; then
     if [ "$FORM_ACTION" = "ADD" ]; then
        echo -e $CONFIG_LINE >> $FILE
     else
       LINECOUNT=0
       echo -n > $TMPFILE
       cat $FILE | tr [\\] [\|] | while read TMPLINE; do
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
     echo "<center><div id=back>$Pig<br><a href=$SCRIPT?ACTION=RELOAD>$Pih</a><br><a href=backup.cgi>$Wtl</a></div>></center><br>"
   fi
fi

case "$FORM_ACTION" in
  "DELETE")
     LINECOUNT=0
     echo -n > $TMPFILE
     cat $FILE | tr [\\] [\|] | while read TMPLINE; do
       LINECOUNT=$(($LINECOUNT+1))
       if [ "$LINECOUNT" -ne "$FORM_LINE" ] ; then
         echo "$TMPLINE" >> $TMPFILE
       fi
     done
     rm -f $FILE
     mv $TMPFILE $FILE
     touch /tmp/need.save
     echo "<center><div id=back>$Pij<br><a href=$SCRIPT?ACTION=RELOAD>$Pih</a><br><a href=backup.cgi>$Wtl</a></div>></center><br>"
     show_list
     ;;
   "CALL_EDIT")
     TMPLINE=`head -n $FORM_LINE $FILE | tail -n 1`
     treat_line $TMPLINE
     ACTION="EDIT"
     LINE=$FORM_LINE
     show_form
     ;;
   "CALL_ADD")
     METHOD=$FORM_METHOD
     ACTION="ADD"
     LINE=0
     show_form
     ;;
   "RELOAD")
     echo "<br><pre>"
     $RELOAD
     echo "</pre><center><div id=back><a href=$SCRIPT>$Fbk</a></div>></center><br>"
     ;;
   *)
     show_list
     ;;
esac
cl_footer2
