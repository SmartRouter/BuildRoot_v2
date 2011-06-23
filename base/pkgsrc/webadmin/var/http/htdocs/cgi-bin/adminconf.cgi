#!/bin/sh
. /var/http/web-functions
. /etc/coyote/coyote.conf
cl_header2 "$Baa - BrazilFW"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
	HOSTNAME=$FORM_HOSTNAME
	DOMAINNAME=$FORM_DOMAINNAME
	TZ=$FORM_TZ
	TIMESERVER=$FORM_TIMESERVER
	LOGGING_HOST=$FORM_LOGGING_HOST
	ENABLE_CRON=$FORM_ENABLE_CRON
	ENABLE_EXTERNAL_PING=$FORM_PING
	ENABLE_EXTERNAL_SSH=$FORM_SSH
	ENABLE_WEBADMIN=$FORM_WEBADMIN
	WEBADMIN_PORT=$FORM_WEBADMINPORT
	SSH_PORT=$FORM_SSHPORT
	DISABLE_NAT=$FORM_DISABLE_NAT
        LOG_ATTEMPTS=$FORM_LOG_ATTEMPTS
        LOG_INCOMING_ACCESS=$FORM_LOG_INCOMING_ACCESS
        LOG_OUTGOING_ACCESS=$FORM_LOG_OUTGOING_ACCESS
        DEBUG=$FORM_DEBUG
        MAX_CONNTRACK=$FORM_MAX_CONNTRACK
	cl_rebuildconf
        echo "<center><div id=alerta>$Wba $Wtc</div></center>"
else
  if [ "$ENABLE_EXTERNAL_PING" = "YES" ] ; then
    PING_YES='checked'
  else
    PING_NO='checked'
  fi
  if [ "$ENABLE_EXTERNAL_SSH" = "NO" ] ; then
    SSH_NO='checked'
  else
    SSH_YES='checked'
  fi
  if [ "$ENABLE_WEBADMIN" = "NO" ] ; then
    WEBADMIN_NO='checked'
  else
    WEBADMIN_YES='checked'
  fi
  if [ "$DISABLE_NAT" = "YES" ] ; then
    DISABLE_NAT_YES='checked'
  else
    DISABLE_NAT_NO='checked'
  fi
  if [ "$ENABLE_CRON" = "YES" ] ; then
    ENABLE_CRON_YES='checked'
  else
    ENABLE_CRON_NO='checked'
  fi
  if [ "$LOG_ATTEMPTS" = "YES" ] ; then
    LOG_ATTEMPTS_YES='checked'
  else
    LOG_ATTEMPTS_NO='checked'
  fi
  if [ "$LOG_INCOMING_ACCESS" = "YES" ] ; then
    LOG_INCOMING_ACCESS_YES='checked'
  else
    LOG_INCOMING_ACCESS_NO='checked'
  fi
  if [ "$LOG_OUTGOING_ACCESS" = "YES" ] ; then
    LOG_OUTGOING_ACCESS_YES='checked'
  else
    LOG_OUTGOING_ACCESS_NO='checked'
  fi
  if [ "$DEBUG" = "1" ] ; then
    DEBUG_YES='checked'
  else
    DEBUG_NO='checked'
  fi
  if [ -z "$WEBADMIN_PORT" ] ; then WEBADMIN_PORT='8180'; fi
  if [ -z "$SSH_PORT" ] ; then SSH_PORT='22'; fi
cat << CLEOF
<form method="POST" action="/cgi-bin/adminconf.cgi"><table class=maintable border=0 width="100%">
<tr><th colspan=2>$Baa</th></tr>
<tr><td width="50%" class=row1 align=right><b>$Ahs</b></td>
 <td width="50%" class=row2><input type=text name=HOSTNAME size=20 value="${HOSTNAME}"></td></tr>
<tr><td class=row1 align=right><b>$Edn</b></td>
 <td class=row2><input type=text name=DOMAINNAME size=20 value="${DOMAINNAME}"></td></tr>
<tr><td class=row1 align=right><b>$Bab</b></td>
 <td class=row2><input type=text name=TZ size=20 value="${TZ}"></td></tr>
<tr><td class=row1 align=right><b>$Bac</b></td>
 <td class=row2><input type=text name=TIMESERVER size=20 value="${TIMESERVER}"></td></tr>
<tr><td class=row1 align=right><b>$Bad</b></td>
 <td class=row2><input type=text name=LOGGING_HOST size=20 value="${LOGGING_HOST}"></td></tr>
<tr><td class=row1 align=right><b>$Bae</b></td>
 <td class=row2><input type=radio value=NO name=PING ${PING_NO}>$Fno &nbsp;<input type=radio value=YES name=PING ${PING_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Baf</b></td>
 <td class=row2><input type=radio value=NO name=SSH ${SSH_NO}>$Fno &nbsp;<input type=radio value=YES name=SSH ${SSH_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Bag</b></td>
 <td class=row2><input type=text name=SSHPORT size=20 value="${SSH_PORT}"></td></tr>
<tr><td class=row1 align=right><b>$Bah</b></td>
 <td class=row2><input type=radio value=NO name=WEBADMIN ${WEBADMIN_NO}>$Fno &nbsp;<input type=radio value=YES name=WEBADMIN ${WEBADMIN_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Bai</b></td>
 <td class=row2><input type=text name=WEBADMINPORT size=20 value="${WEBADMIN_PORT}"></td></tr>
<tr><td class=row1 align=right><b>$Bam</b></td>
 <td class=row2><input type=radio value name=DISABLE_NAT ${DISABLE_NAT_NO}>$Fno &nbsp;<input type=radio value=YES name=DISABLE_NAT ${DISABLE_NAT_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Ban</b></td>
 <td class=row2><input type=radio value name=ENABLE_CRON ${ENABLE_CRON_NO}>$Fno &nbsp;<input type=radio value=YES name=ENABLE_CRON ${ENABLE_CRON_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Bao</b></td>
 <td class=row2><input type=radio value name=LOG_ATTEMPTS ${LOG_ATTEMPTS_NO}>$Fno &nbsp;<input type=radio value=YES name=LOG_ATTEMPTS ${LOG_ATTEMPTS_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Bap</b></td>
 <td class=row2><input type=radio value name=LOG_INCOMING_ACCESS ${LOG_INCOMING_ACCESS_NO}>$Fno &nbsp;<input type=radio value=YES name=LOG_INCOMING_ACCESS ${LOG_INCOMING_ACCESS_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Baq</b></td>
 <td class=row2><input type=radio value name=LOG_OUTGOING_ACCESS ${LOG_OUTGOING_ACCESS_NO}>$Fno &nbsp;<input type=radio value=YES name=LOG_OUTGOING_ACCESS ${LOG_OUTGOING_ACCESS_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Bar</b></td>
 <td class=row2><input type=radio value name=DEBUG ${DEBUG_NO}>$Fno &nbsp;<input type=radio value=1 name=DEBUG ${DEBUG_YES}>$Fye</td></tr>
<tr><td class=row1 align=right><b>$Bas</b></td>
 <td class=row2><input type=text name=MAX_CONNTRACK size=20 value="${MAX_CONNTRACK}"></td></tr>
</table><p align=center><input type=submit value="$Fsb" name=OKBTN>&nbsp;<input type=reset value="$Fer"></p>
</form></center>
CLEOF
fi
cl_footer2
