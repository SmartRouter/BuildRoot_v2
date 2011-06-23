#!/bin/sh
# Source the Web Functions
. /var/http/web-functions
cl_header2 "$Mdt - BrazilFW"
if [ -n "$FORM_COMMAND" ] ; then
  COMMAND=$FORM_COMMAND
  echo "<table class=maintable><tr><td nowrap>"
  if [ -n "$FORM_PARAMNAME" ] ; then
    echo "<center><form method=POST action=/cgi-bin/diags.cgi>"
    echo "$FORM_PARAMNAME"
    echo "&nbsp;:&nbsp;"
    echo "<input type=text size=30 name=PARAM value=\"$FORM_PARAM\">&nbsp;&nbsp;"
    echo "<input type=submit value=&nbsp;$Feo&nbsp;>"
    echo "<input type=hidden name=COMMAND value=\"$FORM_COMMAND\">"
    echo "<input type=hidden name=PARAMNAME value=\"$FORM_PARAMNAME\"></form></center>"
    echo "</td></tr><tr><td nowrap>"
    COMMAND=`echo $COMMAND | sed s/MARK_param_MARK/$FORM_PARAM/`
  fi
  echo "<pre>"
  if [ -n "$FORM_PARAM" -o -z "$FORM_PARAMNAME" ] ; then
    $COMMAND
  fi
  echo "</pre></td></tr></table>"
else 
cat << CLEOF  
<table class=maintable border=0><tr><th>$Mdt</th></tr><tr><td><br><ol>
<li><a href="/cgi-bin/diags.cgi?COMMAND=logread">$Pka</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/showcfg -w">$Pkb</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=ps">$Pkc</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=ping -c 4 MARK_param_MARK&PARAMNAME=IP Number or Host Name">Ping</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=nslookup MARK_param_MARK&PARAMNAME=Host Name">$Pkd</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=ifconfig -a">$Pke</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/dns.test">$Pkf</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/gateway.test">$Pkg</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/iptables -L -n -v">$Pkh</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/iptables -L -t nat -n -v">$Pkh - nat</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/iptables -L -t mangle -n -v">$Pkh - mangle</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=dmesg">$Pki</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=lsmod">$Pkj</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=route">$Pkk</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=cat /proc/meminfo">$Pkl</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=df -h">$Pkm</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=cat /proc/net/arp">$Pkn</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=cat /proc/net/ip_conntrack">$Pko</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=cat /proc/pci">$Psb</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/lsnet">$Pue</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/sbin/lshw -disable ide -html">$Puf</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/changeboot -info">$Pug</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/changeboot -showdevice">$Puh</a></li>
<li><a href="/cgi-bin/diags.cgi?COMMAND=/usr/sbin/detecthds">$Pui</a></li>
</ol></td></tr></table>
CLEOF
fi
cl_footer2
