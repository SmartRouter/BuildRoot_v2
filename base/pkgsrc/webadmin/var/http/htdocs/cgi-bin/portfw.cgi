#!/bin/sh
# PORT FORWADING CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 13/10/2003
. /var/http/web-functions
SCRIPT="portfw.cgi"
FILE="/etc/coyote/portforwards"
TMPFILE="/etc/coyote/porttemp"
RELOAD="/etc/rc.d/rc.firewall"
COLOR="row6"
#==================================
output_line() {
  echo "<tr>"
    if [ "$DACTIVE" = "Yes" ]; then
   MyC="row4"
  else
   MyC="row5"
  fi
  echo "<td class=$MyC>$DACTIVE</td>"
  echo "<td class=$COLOR>$DPROTO</small></td>"
  echo "<td class=$COLOR>$DINET_IP</small></td>"
  echo "<td class=$COLOR>$DINET_PORT</small></td>"
  echo "<td class=$COLOR>$DDEST_IP</small></td>"
  echo "<td class=$COLOR>$DDEST_PORT</small></td>"
  echo "<td class=$COLOR>$DDNS</small></td>"
  echo "<td class=$COLOR nowrap>$DCOMMENT</small></td>"
  echo "<td class=$COLOR nowrap>[<a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>$Faf</a>] [<a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>$Fae</a>]</td>"
  echo "</tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
treat_line() {
  if [ "$1" = "auto" ] ; then
    METHOD="A"
    ACTIVE=$2
    PROTO=$3
    INET_IP=""
    if [ "$3" != "tcp" -a "$3" != "udp" ]; then
      DEST_IP=$4
      DNS=$5
      DINET_PORT=""
      DDEST_PORT=""
    else
      DEST_IP=$5
      DNS=$6
      START_PORT=`echo $4 | cut -f 1 -d :`
      END_PORT=`echo $4 | cut -f 2 -d :`
      if [ "$START_PORT" = "$END_PORT" ] ; then DINET_PORT=$START_PORT ; else DINET_PORT=$4 ; fi
      DDEST_PORT=$DINET_PORT
    fi
  else
    METHOD="P"
    INET_IP=""
    ACTIVE=$2
    DEST_IP=$3
    if [ ! -z "$4" ] && [ "$4" != "tcp" -a "$4" != "udp" ]; then
      INET_IP="$4"
      shift
    fi
    PROTO=$4
    START_PORT=$5
    if [ "$6" = "dns" ]; then
      END_PORT=$START_PORT
      DNS=$6
    else
      END_PORT=$6
      DNS=$7
    fi
    if [ -n "$DNS" -a "$DNS" != "dns" ]; then DNS=""; fi
    DINET_PORT=$START_PORT
    DDEST_PORT=$END_PORT
  fi
  DDEST_IP=$DEST_IP
  if [ -z "$INET_IP" ] ; then DINET_IP="Any" ; else DINET_IP="$INET_IP"; fi
  if [ "$PROTO" = "tcp" ] ; then DPROTO="TCP"; elif [ "$PROTO" = "udp" ] ; then DPROTO="UDP"; else DPROTO="$PROTO"; fi
  if [ "$ACTIVE" = "y" ] ; then DACTIVE="Yes"; else DACTIVE="No"; fi
  if [ "$DNS" = "dns" ]  ; then DDNS="Yes"; else DDNS="No"; fi
  COMMENT=`echo $TMPLINE | sed s/.*#//`
  [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
  DCOMMENT=$COMMENT
}
#==================================
multi_line() {
  while [ -n "$1" ] ; do
    if [ "$FIRST" != "S" ] ; then CONFIG_LINE=$CONFIG_LINE"\n" ; fi
    CONFIG_LINE=$CONFIG_LINE"auto Y $2 $1 $FORM_DEST_IP $FORM_DNS $FORM_COMMENT"
    FIRST="N"
    shift
    shift
  done
}
#==================================
mount_configuration() {
  CONFIG_LINE=""
  if [ "$FORM_METHOD" = "A" ]; then
    [ ! -z "$FORM_PROTON" ] && FORM_PROTO="$FORM_PROTON" && FORM_START_PORT="" && FORM_END_PORT=""
    if [ -z "$FORM_START_PORT" ] || [ -z "$FORM_DEST_IP" ] && [ "$FORM_PROTO" = "tcp" -o "$FORM_PROTO" = "udp" ]; then
      echo "<center><div id=alerta>$Paa</div></center><br>"
      return
    elif [ -z "$FORM_PROTON" ] || [ -z "$FORM_DEST_IP" ] && [ "$FORM_PROTO" != "tcp" -a "$FORM_PROTO" != "udp" ]; then
      echo "<center><div id=alerta>$Pab</div></center><br>"
      return
    fi
    if [ ! -z "$FORM_END_PORT" ] && [ "$FORM_START_PORT" -gt "$FORM_END_PORT" ]; then
      echo "<center><div id=alerta>$Pac</div></center><br>"
      return
    fi
    [ ! -z "$FORM_END_PORT" ] && FORM_START_PORT="${FORM_START_PORT}:${FORM_END_PORT}"
    [ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
    FORM_ACTIVE=`echo "$FORM_ACTIVE" | tr [y,n] [Y,N]`
    CONFIG_LINE="auto $FORM_ACTIVE $FORM_PROTO $FORM_START_PORT $FORM_DEST_IP $FORM_DNS $FORM_COMMENT"
  fi
  if [ "$FORM_METHOD" = "P" ]; then
    #if [ -z "$FORM_DEST_IP" -o -z "$FORM_END_PORT" ] ; then
    if [ -z "$FORM_DEST_IP" ] ; then
      echo "<center><div id=alerta>$Pad</div></center><br>"
      return
    fi
    if [ -z "$FORM_START_PORT" ] ; then
      FORM_START_PORT=$FORM_END_PORT
    fi
    if [ "$FORM_DNS" = "dns" ] && [ "$FORM_PROTO" = "" -o "$FORM_START_PORT" = "" -o "$FORM_END_PORT" = "" ]; then
      echo "<center><div id=alerta>$Pae<br>$Paf</div></center><br>"
      FORM_DNS=""
    fi
    [ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
    FORM_ACTIVE=`echo "$FORM_ACTIVE" | tr [y,n] [Y,N]`
    CONFIG_LINE="port $FORM_ACTIVE $FORM_DEST_IP $FORM_INET_IP $FORM_PROTO $FORM_START_PORT $FORM_END_PORT $FORM_DNS $FORM_COMMENT"
  fi
  if [ "$FORM_METHOD" = "W" ]; then
    if [ -z "$FORM_DEST_IP" ]; then
      echo "<center><div id=alerta>$Pag</div></center><br>"
      return
    fi
    [ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
    FIRST="S"
    multi_line $FORM_SERVICE
  fi
}
#==================================
show_list() {
cat << CLEOF
<table class=maintable border=0 width="100%"><tr><th colspan=9>$Pah</th></tr><tr>
<td class=header>$Pai</td><td class=header>$Paj</td><td class=header>$Pak</td><td class=header>$Pal</td>
<td class=header>$Pam</td><td class=header>$Pan</td><td class=header>$Pao</td><td class=header>$Fad</td><td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | while read TMPLINE; do
  LINECOUNT=$(($LINECOUNT+1))
  TMPLINE2=`echo "$TMPLINE" | cut -f 1 -d \# | tr [A-Z] [a-z]`
  case "$TMPLINE2" in
    \#*|"")
      continue ;;
    auto*|port*)
      treat_line $TMPLINE2
      output_line ;;
  esac
done
cat << CLEOF
</table><br>
<table class=maintable><tr><td class=row1><b>$Pap</td><td class=row2></b> [ <a href=$SCRIPT?ACTION=CALL_ADD&METHOD=P><u>$Paq</u></a> &nbsp; | &nbsp;
<a href=$SCRIPT?ACTION=CALL_ADD&METHOD=A><u>$Par</u></a> &nbsp; | &nbsp;
<a href=$SCRIPT?ACTION=CALL_ADD&METHOD=W><u>$Pas</u></a> ]<br></td></tr><tr><td class=row1>
<b>$Pat</td><td class=row2></b> [ <a href=$SCRIPT?ACTION=RELOAD><u>$Pau</u></a> &nbsp; | &nbsp;<a href="editconf.cgi?CONFFILE=/etc/coyote/portforwards&DESCFILE=Port Forwarding Configuration"><u>$Pav</u></a> ]
</td></tr></table>
<br>
CLEOF
}
#==================================
show_form() {
if [ "$METHOD" = "P" ] ; then
  FORMTITLE="$Pax"
else
  FORMTITLE="$Pay"
fi
cat << CLEOF
<form method="POST" action="$SCRIPT"><input type=hidden value="$METHOD" name=METHOD><input type=hidden value="$LINE" name=LINE>
<input type=hidden value="$ACTION" name=ACTION><table class=maintable border="0" width="100%"><tr><th colspan=2>$FORMTITLE</td></tr>
<tr><td class=row1 align=right><b>$Paz</b><br>$Pba</td>
 <td class=row2><input type=radio value=n name=ACTIVE `[ "$ACTIVE" = "n" ] && echo checked`>$Fno &nbsp;<input type=radio value=y name=ACTIVE `[ "$ACTIVE" = "y" ] && echo checked`>$Fye</td></tr>
CLEOF
if [ "$METHOD" = "P" ] ; then
cat << CLEOF
<tr><td class=row1 align=right><b>$Pbb</b><br>$Pbc</td>
 <td class=row2><input type=radio name=PROTO value=tcp `[ "$PROTO" = "tcp" ] && echo checked`>TCP&nbsp;<input type=radio name=PROTO value=udp `[ "$PROTO" = "udp" ] && echo checked`>UDP</td></tr>
<tr><td class=row1 align=right><b>$Pbd</b><br>$Pbe</td><td class=row2><input type=text name=DEST_IP value="$DEST_IP" size=16></td></tr>
<tr><td class=row1 align=right><b>$Pbf ($Fop)</b><br>$Pbg</td><td class=row2><input type=text name=END_PORT value="$END_PORT" size=5></td></tr>
<tr><td class=row1 align=right><b>$Pbh ($Fop)</b><br>$Pbi<br>$Pbj</td><td class=row2><input type=text name=INET_IP value="$INET_IP" size=16></td></tr>
<tr><td class=row1 align=right><b>$Pbk ($Fop)</b><br>$Pbl<br>$Pbm</td><td class=row2><input type=text name=START_PORT value="$START_PORT" size=5></td></tr>
CLEOF
else
[ "$FORM_ACTION" = "CALL_EDIT" -a "$PROTO" != "tcp" -a "$PROTO" != "udp" ] && PROTON="$PROTO"
[ "$FORM_ACTION" = "CALL_ADD" ] &&  PROTO="" && PROTON=""
[ "$START_PORT" = "$END_PORT" ] && END_PORT=""
cat << CLEOF
<tr><td class=row1 align=right><b>$Pbb</b><br>$Pbn</td>
 <td class=row2><input type=radio name=PROTO value=tcp `[ "$PROTO" = "tcp" ] && echo checked`>TCP<input type=radio name=PROTO value=udp `[ "$PROTO" = "udp" ] && echo checked`>UDP&nbsp&nbsp#&nbsp<input type=text name=PROTON value="$PROTON" size=3></td></tr>
<tr><td class=row1 align=right><b>$Pbd</b><br>$Pbo</td><td class=row2><input type=text name=DEST_IP value="$DEST_IP" size=16></td></tr>
<tr><td class=row1 align=right><b>$Pbp</b><br>$Pbq</td><td class=row2><input type=text name=START_PORT value="$START_PORT" size=5></td></tr>
<tr><td class=row1 align=right><b>$Pbr ($Fop)</b><br>$Pbs</td><td class=row2><input type=text name=END_PORT value="$END_PORT" size=5></td></tr>
CLEOF
fi
[ "$DNS" != "dns" ] && DNS=""
cat << CLEOF
<tr><td class=row1 align=right><b>$Pbt ($Frc)</b><br>$Pbu<br>$Pbv</td>
<td class=row2><input type=radio value name=DNS `[ -z "$DNS" ] && echo checked`>$Fno &nbsp;&nbsp<input type=radio value=dns name=DNS `[ -n "$DNS" ] && echo checked`>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Fad ($Fop)</b><br>$Pbx<br>$Pby ($Pbw "Web01 HTTP").</td><td class=row2><input type=text name=COMMENT value="$COMMENT" size=30></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p></form>
CLEOF
}
#==================================
show_wizard() {
cat << CLEOF
<form method="POST" action="$SCRIPT"><input type=hidden value=ADD name=ACTION><input type=hidden value=W name=METHOD><table class=maintable border=0 width="100%"><tr><th colspan=2>$Pbz</th></tr>
<tr><td class=row1 align=right><b>$Pca</b><br>$Pcb</td><td class=row2><select name=SERVICE>
<option value="80 tcp">http - $Pcc</option><option value="443 tcp">https - $Pcd</option>
<option value="20:21 tcp">ftp - $Pce</option><option value="110 tcp">pop3 - $Pcf</option>
<option value="25 tcp">smtp - $Pcg</option><option value="143 tcp">imap - $Pch</option>
<option value="53 udp 53 tcp">dns - $Pci</option><option value="23 tcp">telnet ($Fai)</option>
<option value="113 tcp 113 udp">ident - $Pcj</option><option value="5900 tcp 5800 tcp">VNC - $Pck</option>
<option value="5631 tcp 5632 udp">PCAnyWhere - $Pck</option><option value="4662 tcp 4672 udp">Emule - $Pcl</option>
<option value="4663 tcp 4673 udp">Emule - $Pcm</option><option value="6881:6889 tcp">BitTorrent P2P</option>
</select></td></tr>
<tr><td class=row1 align=right><b>$Pbd</b><br>$Pbe</td><td class=row2><input type=text name=DEST_IP value="$DEST_IP" size=16></td></tr>
<tr><td class=row1 align=right><b>$Fad ($Fop)</b><br>$Pbx<br>$Pdu ($Pbw "Web01 HTTP").</td><td class=row2><input type=text name=COMMENT value="$COMMENT" size=30></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p></form>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Pah - BrazilFW"
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
     echo "<center><div id=back>$Pcn<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Pco</u></a><br><a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br>"
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
     echo "<center><div id=back>$Pcp<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Pco</u></a><br><a href=backup.cgi class=lnk><u>$Wtl</u></a></div></center><br>"
     show_list
     ;;
   "CALL_EDIT")
     TMPLINE=`head -n $FORM_LINE $FILE | tail -n 1`
     TMPLINE2=`echo "$TMPLINE" | cut -f 1 -d \# | tr [A-Z] [a-z]`
     treat_line $TMPLINE2
     ACTION="EDIT"
     LINE=$FORM_LINE
     show_form
     ;;
   "CALL_ADD")
     METHOD=$FORM_METHOD
     ACTION="ADD"
     LINE=0
     ACTIVE="y"
     DEST_IP=""
     INET_IP=""
     START_PORT=""
     END_PORT=""
     PROTO="tcp"
     DNS="dns"
     if [ $FORM_METHOD = "W" ] ; then
       show_wizard
     else
       show_form
     fi
     ;;
   "RELOAD")
     echo "<center><pre>"
     $RELOAD
     echo "</pre></center><center><div id=back><a href=$SCRIPT class=lnk><u>$Fbk</u></a></div></center><br>"
     ;;
   *)
     show_list
     ;;
esac

cl_footer2
