#!/bin/sh
# LOCAL HOSTS CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 06/03/2004
. /var/http/web-functions
. /etc/coyote/coyote.conf
if [ "$INETTYPE" = "ETHERNET_DHCP" ] ; then
  if [ -e "/etc/dhcpc/$IF_INET.info" ] ; then
    . /etc/dhcpc/$IF_INET.info
  fi
fi
[ -z "$DOMAINNAME" -a -n "$dhcp_domain" ] && DOMAINNAME="$dhcp_domain"
[ -z "$DOMAINNAME" -a -n "$DHCPD_DOMAIN" ] && DOMAINNAME="$DHCPD_DOMAIN"
[ -z "$DOMAINNAME" ] && DOMAINNAME="localdomain"
SCRIPT="localhosts.cgi"
FILE="/etc/hosts.dns"
TMPFILE="/tmp/hosts.dns"
RELOAD="/etc/rc.d/rc.dnsmasq"
COLOR="row6"
#==================================
output_line() {
  echo "<tr>"
  echo "<td class=$COLOR>$DIP</td>"
  echo "<td class=$COLOR>$DHOSTF</td>"
  echo "<td class=$COLOR>$DHOST</td>"
  echo "<td class=$COLOR>$DCOMMENT</td>"
  echo "<td class=$COLOR nowrap><a href=$SCRIPT?ACTION=CALL_EDIT&LINE=$LINECOUNT>&nbsp;[$Faf]&nbsp;</a>&nbsp;<a href=$SCRIPT?ACTION=DELETE&LINE=$LINECOUNT>&nbsp;[$Fae]&nbsp;</a></td>"
  echo "</tr>"
  if [ "$COLOR" = "row6" ] ; then COLOR="row8"; else COLOR="row6"; fi
}
#==================================
treat_line() {
  IP=$1
  HOSTF=$2
  HOST=$3
  if [ -z "$3" ] ; then
    if [ "`echo $HOSTF | cut -f 1 -d .`" = "$HOSTF" ] ; then
      HOST=$HOSTF
      HOSTF=""
    fi
  fi
  DIP=$IP
  DHOSTF=$HOSTF
  DHOST=$HOST
  COMMENT=`echo "$TMPLINE" | sed s/.*#//`
  [ "$COMMENT" = "$TMPLINE" ] && COMMENT=""
  DCOMMENT=$COMMENT
}
#==================================
mount_configuration() {
  IP="$FORM_IP"
  HOSTF="$FORM_HOSTF"
  HOST="$FORM_HOST"
  COMMENT="$FORM_COMMENT"
  if [ -z "$HOSTF" -o -z "$HOST" ] ; then
    TMPPAR="$HOSTF$HOST"
    if [ "`echo $TMPPAR | cut -f 1 -d .`" = "$TMPPAR" ] ; then
      HOST="$TMPPAR"
      HOSTF=""
    else
      HOST=""
      HOSTF="$TMPPAR"
    fi
  fi
#  if [ -z "$HOSTF" -a -n "$HOST" ] ; then
#    if [ "`echo $HOSTF | cut -f 1 -d .`" = "$HOSTF" ] ; then
#      HOSTF="$HOST.$DOMAINNAME"
#    fi
#  fi
  [ ! -z "$FORM_COMMENT" ] && FORM_COMMENT="#$FORM_COMMENT"
  CONFIG_LINE="$IP $HOSTF $HOST $FORM_COMMENT"
}
#==================================
show_list() {
cat << CLEOF
<table class=maintable border=0 width="100%"><tr><th colspan=5>$Lca</th></tr><tr>
<td class=header>IP</td><td class=header>$Lcb</td><td class=header>$Faz</td><td class=header>$Fad</td><td class=header>$Fac</td></tr>
CLEOF
LINECOUNT=0
cat $FILE | while read TMPLINE; do
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
cat << CLEOF
</table><br>
<table class=maintable><tr><td class=row1><b>$Lcc</b></td>
<td class=row2><a href=$SCRIPT?ACTION=CALL_ADD>[&nbsp <u>$Lcd</u></a>&nbsp; ]</td></tr><tr><td class=row1>
<b>$Lce</b></td><td class=row2><a href=$SCRIPT?ACTION=RELOAD>[ &nbsp;<u>$Egg</u></a>&nbsp; | &nbsp;
<a href="editconf.cgi?CONFFILE=/etc/hosts.dns&DESCFILE=Local Hosts File"><u>$Lcf</u></a> ]</td></tr>
<tr><td class=row1><b>$Faw</b></td><td class=row2>[&nbsp <a href=dhcpconf.cgi><u>$Egj</u></a>&nbsp; ]</td></tr>
</table>
<br>
CLEOF
}
#==================================
show_form() {
FORMTITLE="$Lcg"
cat << CLEOF
<form method="POST" action="$SCRIPT"><input type=hidden value="$LINE" name=LINE><input type=hidden value="$ACTION" name=ACTION>
<table class=maintable border=0 width="100%"><tr><th colspan=2>$FORMTITLE</th></tr>
<tr><td class=row1 align=right><b>$Ego</b><br>$Lch</td><td class=row2><input type=text name=IP value="$IP" size=22></td></tr>
<tr><td class=row1 align=right><b>$Ahs</b><br>$Lci</td><td class=row2><input type=text name=HOST value="$HOST" size=22></td></tr>
<tr><td class=row1 align=right><b>$Lcj ($Fop)</b><br>$Lck</td><td class=row2><input type=text name=HOSTF value="$HOSTF" size=22></td></tr>
<tr><td class=row1 align=right><b>$Fad ($Fop)</b><br>$Lcl</td><td class=row2><input type=text name=COMMENT value="$COMMENT" size=30></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset  value="$Fer"></p>
</form>
CLEOF
}
#==================================
# MAIN ROUTINE
cl_header2 "$Lca"
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
     echo "<center><div id=back>$Lcm<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Egt</u></a><br><a href=backup.cgi class=lnk><u>$Fah</u></a></div></center><br>"
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
     echo "<center><div id=back>$Lcn<br><a href=$SCRIPT?ACTION=RELOAD class=lnk><u>$Egt</u></a><br><a href=backup.cgi class=lnk><u>$Fah</u></a></div></center><br>"
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
     show_list
     ;;
esac

cl_footer2
