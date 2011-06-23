#!/bin/sh
# SIMPLIFIED FIREWALL CONFIGURATION
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 11/09/2004
. /var/http/web-functions
. /etc/coyote/coyote.conf
SCRIPT="sfirewall.cgi"
FILE="/etc/coyote/firewall"
TMPFILE="/etc/coyote/acctemp"
RELOAD="/etc/rc.d/rc.firewall"
COLOR="row6"
IP_BLACK_LIST=/tmp/sfw_ip_black_list
IP_WHITE_LIST=/tmp/sfw_ip_white_list
PORT_BLACK_LIST=/tmp/sfw_port_black_list
PORT_WHITE_LIST=/tmp/sfw_port_white_list
MAC_BLACK_LIST=/tmp/sfw_mac_black_list
MAC_WHITE_LIST=/tmp/sfw_mac_white_list
PROTOCOLS_LIST=/tmp/sfw_protocols_list
IP_MAC_LIST=/tmp/sfw_ip_mac_list
echo -n > $IP_BLACK_LIST
echo -n > $IP_WHITE_LIST
echo -n > $PORT_BLACK_LIST
echo -n > $PORT_WHITE_LIST
echo -n > $MAC_BLACK_LIST
echo -n > $MAC_WHITE_LIST
echo -n > $PROTOCOLS_LIST
echo -n > $IP_MAC_LIST
cl_header2 "$Msf - BrazilFW"
if [ "$FORM_ACTION" = "RELOAD" ]; then
   echo "<pre>"
   $RELOAD
   echo "</pre><center><div id=back><a href=$SCRIPT class=links>$Fbk</a></div></center><br>"
   cl_footer2
   exit 0
fi

if [ "$FORM_OKBTN" = "$Fsb" ]; then
  echo -n > $TMPFILE
  cat $FILE | while read TMPLINE; do
    case "$TMPLINE" in
      block_ip*|allow_ip*|block_mac*|allow_mac*|block_port*|allow_port*|block_protocol*|match_ip_mac*)
        continue ;;
      *)
        echo $TMPLINE >> $TMPFILE
    esac
  done

  echo "$FORM_IP_BLACK_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo block_ip $TMPLINE >> $TMPFILE
  done
  echo "$FORM_IP_WHITE_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo allow_ip $TMPLINE >> $TMPFILE
  done
  echo "$FORM_PORT_BLACK_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo block_port $TMPLINE >> $TMPFILE
  done
  echo "$FORM_PORT_WHITE_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo allow_port $TMPLINE >> $TMPFILE
  done
  echo "$FORM_MAC_BLACK_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo block_mac $TMPLINE >> $TMPFILE
  done
  echo "$FORM_MAC_WHITE_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo allow_mac $TMPLINE >> $TMPFILE
  done
  echo "$FORM_PROTOCOLS_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo block_protocol $TMPLINE >> $TMPFILE
  done
  echo "$FORM_IP_MAC_LIST" | while read TMPLINE; do
    [ -n "$TMPLINE" ] && echo match_ip_mac $TMPLINE >> $TMPFILE
  done

  rm -f $FILE
  mv $TMPFILE $FILE

  DEFAULT_USERS_FILTER=$FORM_DEFAULT_USERS_FILTER
  DEFAULT_SERVICES_FILTER=$FORM_DEFAULT_SERVICES_FILTER
  cl_rebuildconf
  echo "<center><div id=back>$Pcn<br><a href=$SCRIPT?ACTION=RELOAD>$Pco</a><br><a href=backup.cgi>$Wtl</a></div></center><br>"
fi

treat_line()
{
  case $1 in
    block_ip)       echo $2 >> $IP_BLACK_LIST ;;
    allow_ip)       echo $2 >> $IP_WHITE_LIST ;;
    block_mac)      echo $2 >> $MAC_BLACK_LIST ;;
    allow_mac)      echo $2 >> $MAC_WHITE_LIST ;;
    block_port)     echo $2 $3 >> $PORT_BLACK_LIST ;;
    allow_port)     echo $2 $3 >> $PORT_WHITE_LIST ;;
    block_protocol) echo $2 >> $PROTOCOLS_LIST ;;
    match_ip_mac)   echo $2 $3 >> $IP_MAC_LIST ;;
  esac
}

cat $FILE | while read TMPLINE; do
  LINECOUNT=$(($LINECOUNT+1))
  TMPLINE2=`echo "$TMPLINE" | cut -f 1 -d \# | tr [A-Z] [a-z]`
  case "$TMPLINE2" in 
    block_ip*|allow_ip*|block_mac*|allow_mac*|block_port*|allow_port*|block_protocol*|match_ip_mac*)
      treat_line $TMPLINE2 ;;
  esac
done

cat << CLEOF
<form method="POST" action="$SCRIPT"><table class=maintable border=0 width=100%><tr><th colspan=4>$Pna</th></tr>
<tr><td width="50%" colspan=2 class=row1><input type=radio value=ALLOW_ALL name=DEFAULT_USERS_FILTER `[ "$DEFAULT_USERS_FILTER" != "BLOCK_ALL" ] && echo -n checked` ><b>$Pnd</b></td>
    <td width="50%" colspan=2 class=row2><input type=radio value=BLOCK_ALL name=DEFAULT_USERS_FILTER `[ "$DEFAULT_USERS_FILTER"  = "BLOCK_ALL" ] && echo -n checked` ><b>$Pne</b></td>
</tr>
<tr><td width="25%" class=row1 align=left valign=top><b>$Pnj</b><br>$Pnm  $Pnl<br>192.168.0.2<br>10.0.0.2</td>
    <td width="25%" class=row1><textarea rows=7 cols=20 name=IP_BLACK_LIST wrap=off>`cat $IP_BLACK_LIST`</textarea></td>
    <td width="25%" class=row2 align=left valign=top><b>$Pnk</b><br>$Pnn  $Pnl<br>192.168.0.2<br>10.0.0.2</td>
    <td width="25%" class=row2><textarea rows=7 cols=20 name=IP_WHITE_LIST wrap=off>`cat $IP_WHITE_LIST`</textarea></td>
</tr>
<tr>
    <td class=row1 align=left valign=top>$Pno $Pnl<br>00:0a:02:0b:03:0c<br>01:0d:03:0e:00:0f</td>
    <td class=row1><textarea rows=7 cols=20 name=MAC_BLACK_LIST wrap=off>`cat $MAC_BLACK_LIST`</textarea></td>
    <td class=row2 align=left valign=top>$Pnp $Pnl<br>00:0a:02:0b:03:0c<br>01:0d:03:0d:00:0f</td>
    <td class=row2><textarea rows=7 cols=20 name="MAC_WHITE_LIST" wrap=off>`cat $MAC_WHITE_LIST`</textarea></td>
</tr>
<tr><td colspan=2 class=row2 align=left valign=top><b>$Pts</b><br>$Ptt<br>192.168.0.10 01:0d:03:0e:00:0f<br>192.168.0.11 01:0d:03:0e:dd:ff<br><br>$Ptu</td>
    <td colspan=2 class=row2><textarea rows=7 cols=44 name=IP_MAC_LIST wrap=off>`cat $IP_MAC_LIST`</textarea></td>
</tr>
<tr><th colspan=4 class=row3>$Pnb</td></tr>
<tr><td colspan=2 class=row1><input type=radio value=ALLOW_ALL name=DEFAULT_SERVICES_FILTER `[ "$DEFAULT_SERVICES_FILTER" != "BLOCK_ALL" ] && echo -n checked` ><b>$Pnh</b></td>
    <td class=row2 colspan=2><input type=radio value=BLOCK_ALL name=DEFAULT_SERVICES_FILTER `[ "$DEFAULT_SERVICES_FILTER"  = "BLOCK_ALL" ] && echo -n checked` ><b>$Pni</b></td>
</tr>
<tr><td class=row1 align=left valign=top><b>$Pnj</b><br>$Pnq  $Pnl<br>80 tcp<br>53 udp<br>20:21 tcp</td>
    <td class=row1><textarea rows=7 cols=20 name=PORT_BLACK_LIST wrap=off>`cat $PORT_BLACK_LIST`</textarea></td>
    <td class=row2 align=left valign=top><b>$Pnk</b><br>$Pnr  $Pnl<br>80 tcp<br>53 udp<br>20:21 tcp</td>
    <td class=row2><textarea rows=7 cols=20 name=PORT_WHITE_LIST wrap=off>`cat $PORT_WHITE_LIST`</textarea></td>
</tr>
CLEOF
if [ -e /etc/l7-protocols ] ; then
cat << CLEOF
<tr><th colspan=4>$Pns</th></tr>
<tr><td colspan=2 class=row3 align=left valign=top>$Pnt<br>$Pnu<br>fasttrack<br>edonkey<br>directconnect<br><br>
    <a href='diags.cgi?COMMAND=/usr/sbin/protocols.list'><u>$Pnv<u></a></td>
    <td colspan=2 class=row3><textarea rows=7 cols=44 name=PROTOCOLS_LIST wrap=off>`cat $PROTOCOLS_LIST`</textarea></td>
</tr>
CLEOF
fi
cat << CLEOF
</table><p align=center><input type=submit value="$Fsb" name=OKBTN><input type=reset value="$Fer"></p></form>

<table class=maintable><tr><td class=row1>
<b>$Egf</td><td class=row2></b> [ <a href=$SCRIPT?ACTION=RELOAD><u>$Pau</u></a> &nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/coyote/firewall&DESCFILE=Firewall Configuration"><u>$Pav</u></a> &nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/coyote/firewall.local&DESCFILE=Custom Firewall Rules"><u>$Pdh</u></a> ]
</td></tr></table><br>
CLEOF
#rm -f /tmp/sfw_* 1> /dev/null 2> /dev/null
cl_footer2
