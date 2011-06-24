#!/bin/sh
# QOS filter configuration webadmin script
# Author: Dolly <dolly@czi.cz>
# based on portforwards script
# 	Claudio Roberto Cussuol <claudio_cl@rictec.com.br>
# 	Steve Eisner <seisner@comcast.net>
. /var/http/web-functions
SCRIPT="qosfilter.cgi"
FILE="/etc/coyote/qos.filters"
TMPFILE="/etc/coyote/qostemp"
RELOAD="/etc/rc.d/rc.qos"
COLOR="row6"
#==================================
output_line() {
  echo "<tr>"
  if [ "$ACTIVE" = "Y" ]; then
   echo "<td class=row4 align=center><small><b>$Fye</b></small></td>"
  else
   echo "<td class=row5 align=center><small><b>$Fno</b></small></td>"
  fi
  if [ "$TYPE" = "fast" ]; then
   echo "<td class=row4 align=center><small><b>$Fas</b></small></td>"
  else
   echo "<td class=row5 align=center><small><b>$Fat</b></small></td>"
  fi
  echo "<td class=$COLOR>$DPROTO</td>"
  echo "<td class=$COLOR>$DREMP</td>"
  echo "<td class=$COLOR>$DREMM</td>"
  echo "<td class=$COLOR>$DANDOR</td>"
  echo "<td class=$COLOR>$DLOCP</td>"
  echo "<td class=$COLOR>$DLOCM</td>"
  echo "<td class=$COLOR nowrap>$DCOMMENT</td>"
  echo "<td class=$COLOR nowrap><a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>&nbsp;[$Faf]&nbsp;</a><a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>&nbsp;[$Fae]&nbsp;</a></td>"
  echo "</tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
treat_line() {
  TYPE=$1
  ACTIVE=$2
  PROTO=$3
  REMOTE_PORT=$4
  REMOTE_MASK=$5
  ANDOR=$6
  LOCAL_PORT=$7
  LOCAL_MASK=$8
  DPROTO=`echo $PROTO | tr [a-z] [A-Z]`
  DANDOR=`echo $ANDOR | tr [a-z] [A-Z]`
  if [ "$REMOTE_PORT" = 0 ]; then
	DREMP="-"
	DREMM="-"
  else
	DREMP=$REMOTE_PORT
 	DREMM=`echo $REMOTE_MASK | tr [a-z] [A-Z]`
  	[ "$DREMM" = "FFFF" ] && DREMM="Single port"
  	[ "$DREMM" = "0" ] && DREMM="All"
  fi
  if [ "$LOCAL_PORT" = 0 ]; then
	DLOCP="-"
	DLOCM="-"
  else
	DLOCP=$LOCAL_PORT
 	DLOCM=`echo $LOCAL_MASK | tr [a-z] [A-Z]`
  	[ "$DLOCM" = "FFFF" ] && DLOCM="Single port"
  	[ "$DLOCM" = "0" ] && DLOCM="All"
  fi
  [ "$DLOCP" = "-" -o "$DREMP" = "-" ] && DANDOR="-"
  COMMENT=`echo $TMPLINE | sed s/.*#//`
  [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
  DCOMMENT=$COMMENT
}
#==================================
mount_configuration() {
  CONFIG_LINE=""
  if [ "$FORM_TYPE" = "fast" -o "$FORM_TYPE" = "slow" ]; then
    [ -z "$FORM_PROTO" ] && [ -z "$FORM_PROTOA" ] && FORM_PROTO="all"
    [ ! -z "$FORM_PROTOA" ] && FORM_PROTO="$FORM_PROTOA"

    [ -z "$FORM_REMOTE_MASKA" ] && [ -z "$FORM_REMOTE_MASK" ] && FORM_REMOTE_MASK="0"
    [ ! -z "$FORM_REMOTE_MASKA" ] && FORM_REMOTE_MASK="$FORM_REMOTE_MASKA"

    if [ -z "$FORM_REMOTE_PORTA" ] && [ -z "$FORM_REMOTE_PORT" ]; then
	FORM_REMOTE_PORT="0"
     	FORM_REMOTE_MASK="0"
    fi
    [ ! -z "$FORM_REMOTE_PORTA" ] && FORM_REMOTE_PORT="$FORM_REMOTE_PORTA"
    [ "$FORM_REMOTE_MASK" = "0" ] && FORM_REMOTE_PORT="0"
    [ "$FORM_REMOTE_PORT" = "0" ] && FORM_REMOTE_MASK="0"

    [ -z "$FORM_LOCAL_MASKA" ] && [ -z "$FORM_LOCAL_MASK" ] && FORM_LOCAL_MASK="0"
    [ ! -z "$FORM_LOCAL_MASKA" ] && FORM_LOCAL_MASK="$FORM_LOCAL_MASKA"
    if [ -z "$FORM_LOCAL_PORTA" ] && [ -z "$FORM_LOCAL_PORT" ]; then
    	FORM_LOCAL_PORT="0"
    	FORM_LOCAL_MASK="0"
    fi
    [ ! -z "$FORM_LOCAL_PORTA" ] && FORM_LOCAL_PORT="$FORM_LOCAL_PORTA"
    [ "$FORM_LOCAL_MASK" = "0" ] && FORM_LOCAL_PORT="0"
    [ "$FORM_LOCAL_PORT" = "0" ] && FORM_LOCAL_MASK="0"

    [ -z "$FORM_ANDOR" ] && FORM_ANDOR="and"
    if [ "$FORM_LOCAL_PORT" = 0 -a "$FORM_REMOTE_PORT" = 0 ]; then
	FORM_ANDOR="and"
    fi
    [ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
    CONFIG_LINE="$FORM_TYPE $FORM_ACTIVE $FORM_PROTO $FORM_REMOTE_PORT $FORM_REMOTE_MASK $FORM_ANDOR $FORM_LOCAL_PORT $FORM_LOCAL_MASK $FORM_COMMENT"
  fi
}
#==================================
show_list() { #<td align="center" ><b>Line#</td>
cat << CLEOF
<table class=maintable width=100%><tr><th colspan=10>$Pfu</th></tr><tr>
<td class=header>$Faj</td><td class=header>$Fau</td><td class=header>$Paj</td><td class=header>$Pfv</td>
<td class=header>$Pfw</td><td class=header>$Pfx</td><td class=header>$Pfy</td><td class=header>$Pfw</td>
<td class=header>$Fad</td><td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | while read TMPLINE; do
  LINECOUNT=$(($LINECOUNT+1))
  case "$TMPLINE" in
    \#*|"")
      continue ;;
    slow*|fast*)
      treat_line $TMPLINE
      output_line ;;
  esac
done
cat << CLEOF
</table><br>
<table class=maintable><tr><td class=row1>
<b>$Pga</td><td class=row2></b>[ &nbsp;<a href=$SCRIPT?ACTION=CALL_ADD><u>$Pfz</u></a>&nbsp; ]</td></tr>
<tr><td class=row1><b>$Pid</b></td><td class=row2>[ &nbsp;<a href=$SCRIPT?ACTION=RELOAD><u>$Pfi</u></a>&nbsp; | &nbsp;
<a href="qosstatus.cgi"><u>$Pfj</u></a>&nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/coyote/qos.filters&DESCFILE=QOS Filter Rules File"><u>$Pgb</u></a>&nbsp; ]</td></tr>
<tr><td class=row1><b>$Faw</b></td><td class=row2>[&nbsp <a href=qos.cgi><u>$Pgc</u></a>&nbsp; ]</td></tr>
</table></form>
CLEOF
}
#==================================
show_form() {
FORMTITLE="$Pfu"
[ "$LOCAL_PORT" = "0" ] && LOCAL_PORT=
[ "$REMOTE_PORT" = "0" ] && REMOTE_PORT=
[ "$LOCAL_MASK" = "0" ] && LOCAL_MASK=
[ "$REMOTE_MASK" = "0" ] && REMOTE_MASK=
cat << CLEOF
<form method="POST" action="$SCRIPT"><input type=hidden value="$LINE" name=LINE><input type=hidden value="$ACTION" name=ACTION>
<table class=maintable border=0 width="100%"><tr><th colspan=2>$FORMTITLE</th></tr>
<tr><td class=row1 align=right><b>$Paz</b><br>$Pba</td>
      <td class=row2>
        <input type=radio value=N name=ACTIVE `[ "$ACTIVE" = "N" ] && echo checked`>$Fno &nbsp;
        <input type=radio value=Y name=ACTIVE `[ "$ACTIVE" = "Y" ] && echo checked`>$Fye
      </td>
    </tr>
    <tr>
      <td class=row1 align=right><b>$Pgd</b><br>
      $Pge
      </td>
      <td class=row2>
        <input type=radio name=TYPE value=fast `[ "$TYPE" = "fast" ] && echo checked`>$Fas &nbsp;
        <input type=radio name=TYPE value=slow `[ "$TYPE" = "slow" ] && echo checked`>$Fat
      </td>
    </tr>
    <tr>
      <td class=row1 align=right><b>$Pgf ($Fop)</b>
      <br>$Pgg
      </td>
      <td class=row2>
        <input type=text name=PROTO value="$PROTO" size=5>&nbsp; $Far &nbsp;
        <select name=PROTOA>
          <option value></option>
          <option value="all">$Fav</option>
          <option value="tcp">TCP</option>
          <option value="udp">UDP</option>
          <option value="icmp">ICMP</option>
        </select>
      </td>
    </tr>
    <tr>
      <td class=row1 align=right><b>$Pgh ($Fop)</b>
      <br>$Pgi</td>
      <td class=row2>
        <input type=text name=REMOTE_PORT value="$REMOTE_PORT" size=22>&nbsp; $Far &nbsp;
        <select name=REMOTE_PORTA>
          <option value></option>
          <option value="0">$Fav</option>
        </select>
      </td>
    </tr>
    <tr>
      <td class=row1 align=right><b>$Pgj ($Fop)</b>
      <br>$Pgk</td>
      <td class=row2>
        <input type=text name=REMOTE_MASK value="$REMOTE_MASK" size=22>&nbsp; $Far &nbsp;
        <select name=REMOTE_MASKA>
          <option value></option>
          <option value="ffff">$Pgl</option>
          <option value="fffc">4   $Pgm</option>
          <option value="fff8">8   $Pgm</option>
          <option value="fff0">16  $Pgm</option>
          <option value="ffe0">32  $Pgm</option>
          <option value="ffc0">64  $Pgm</option>
          <option value="ff80">128 $Pgm</option>
          <option value="ff00">256 $Pgm</option>
        </select>
      </td>
    </tr>
    <tr>
      <td class=row1 align=right><b>$Pgn</b>
      <br>$Pgo<br>$Pgp</td>
      <td class=row2>
        <input type=radio name=ANDOR value="and" `[ "$ANDOR" = "and" ] && echo checked`>$Pgq<br>
        <input type=radio name=ANDOR value="or" `[ "$ANDOR" = "or" ] && echo checked`>$Pgr
      </td>
    </tr>

    <tr>
      <td class=row1 align=right><b>$Pfy ($Fop)</b>
      <br>$Pgs</td>
      <td class=row2>
        <input type=text name=LOCAL_PORT value="$LOCAL_PORT" size=22>&nbsp; $Far &nbsp;
        <select name=LOCAL_PORTA>
          <option value></option>
          <option value="0">$Fav</option>
        </select>
      </td>
    </tr>
    <tr>
      <td class=row1 align=right><b>$Pgt ($Fop)</b>
      <br>$Pgu</td>
      <td class=row2>
        <input type=text name=LOCAL_MASK value="$LOCAL_MASK" size=22>&nbsp; $Far &nbsp;
        <select name=LOCAL_MASKA>
          <option value></option>
          <option value="ffff">$Pgl</option>
          <option value="fffc">4   $Pgm</option>
          <option value="fff8">8   $Pgm</option>
          <option value="fff0">16  $Pgm</option>
          <option value="ffe0">32  $Pgm</option>
          <option value="ffc0">64  $Pgm</option>
          <option value="ff80">128 $Pgm</option>
          <option value="ff00">256 $Pgm</option>
        </select>
      </td>
    </tr>
    <tr>
      <td class=row1 align=right><b>$Fad ($Fop)</b>
      <br>$Pgv
      </td>
      <td class=row2>
        <input type=text name=COMMENT value="$COMMENT" size=30>
      </td>
    </tr>
  </table>
  <p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p>
</form>
</center>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Pfu - SmartRouter"
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
     echo "<center><div id=back>$Pgw<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Pfs</u></a><br><a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br>"
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
     echo "<center><div id=back>$Pgx<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Pfs</u></a><br><a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br>"
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
     ACTIVE="N"
     LINE=0
     TYPE="slow"
     PROTO=""
     REMOTE_PORT=""
     REMOTE_MASK=""
     ANDOR="and"
     LOCAL_PORT=""
     LOCAL_MASK=""
     show_form
     ;;
   "RELOAD")
     echo "<br><pre>"
     $RELOAD
     echo "</pre><center><div id=back><a href=$SCRIPT class=lnk><u>$Fbk</u></a></div></center><br>"
     ;;
   *)
     show_list
     ;;
esac

cl_footer2
