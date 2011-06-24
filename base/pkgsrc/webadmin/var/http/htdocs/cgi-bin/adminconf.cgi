#!/bin/sh 
. /var/http/web-functions
. /etc/coyote/coyote.conf
SCRIPT="/cgi-bin/adminconf.cgi"
cl_header2 "$Baa - SmartRouter"
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
 HD_SLEEP_TIME=$FORM_HD_SLEEP_TIME
 cl_rebuildconf
 alert "$Wba" "$Wtc"
else
 [ "$HD_SLEEP_TIME" = "" ] && HD_SLEEP_TIME=0
 [ "$ENABLE_EXTERNAL_PING" = "YES" ] && PING_YES='checked' || PING_NO='checked'
 [ "$ENABLE_EXTERNAL_SSH" = "NO" ] && SSH_NO='checked' || SSH_YES='checked'
 [ "$ENABLE_WEBADMIN" = "NO" ] && WEBADMIN_NO='checked' || WEBADMIN_YES='checked'
 [ "$DISABLE_NAT" = "YES" ] && DISABLE_NAT_YES='checked' || DISABLE_NAT_NO='checked'
 [ "$ENABLE_CRON" = "YES" ] && ENABLE_CRON_YES='checked' || ENABLE_CRON_NO='checked'
 [ "$LOG_ATTEMPTS" = "YES" ] && LOG_ATTEMPTS_YES='checked' || LOG_ATTEMPTS_NO='checked'
 [ "$LOG_INCOMING_ACCESS" = "YES" ] && LOG_INCOMING_ACCESS_YES='checked' || LOG_INCOMING_ACCESS_NO='checked'
 [ "$LOG_OUTGOING_ACCESS" = "YES" ] && LOG_OUTGOING_ACCESS_YES='checked' || LOG_OUTGOING_ACCESS_NO='checked'
 [ "$DEBUG" = "1" ] && DEBUG_YES='checked' || DEBUG_NO='checked'
 [ -z "$WEBADMIN_PORT" ] && WEBADMIN_PORT='8180'
 [ -z "$SSH_PORT" ] && SSH_PORT='22'
 init_form
 init_main_table
 add_title "$Baa"
 form_info_item "$Ahs" "" "$(input_text "HOSTNAME" "${HOSTNAME}" "20")"
 form_info_item "$Edn" "" "$(input_text "DOMAINNAME" "${DOMAINNAME}" "20")"
 form_info_item "$Bab" "" "$(input_text "TZ" "${TZ}" "20")"
 form_info_item "$Bac" "" "$(input_text "TIMESERVER" "${TIMESERVER}" "20")"
 form_info_item "$Bad" "" "$(input_text "LOGGING_HOST" "${LOGGING_HOST}" "20")"
 form_info_item "$Bae" "" "$(input_radio "PING" "NO" "$Fno" "${PING_NO}") $(input_radio "PING" "YES" "$Fye" "${PING_YES}")"
 form_info_item "$Baf" "" "$(input_radio "SSH" "NO" "$Fno" "${SSH_NO}") $(input_radio "SSH" "YES" "$Fye" "${SSH_YES}")"
 form_info_item "$Bag" "" "$(input_text "SSHPORT" "${SSH_PORT}" "20")"
 form_info_item "$Bah" "" "$(input_radio "WEBADMIN" "NO" "$Fno" "${WEBADMIN_NO}") $(input_radio "WEBADMIN" "YES" "$Fye" "${WEBADMIN_YES}")"
 form_info_item "$Bai" "" "$(input_text "WEBADMINPORT" "${WEBADMIN_PORT}" "20")"
 form_info_item "$Bam" "" "$(input_radio "DISABLE_NAT" "NO" "$Fno" "${DISABLE_NAT_NO}") $(input_radio "DISABLE_NAT" "YES" "$Fye" "${DISABLE_NAT_YES}")"
 form_info_item "$Ban" "" "$(input_radio "ENABLE_CRON" "NO" "$Fno" "${ENABLE_CRON_NO}") $(input_radio "ENABLE_CRON" "YES" "$Fye" "${ENABLE_CRON_YES}")"
 form_info_item "$Bao" "" "$(input_radio "LOG_ATTEMPTS" "NO" "$Fno" "${LOG_ATTEMPTS_NO}") $(input_radio "LOG_ATTEMPTS" "YES" "$Fye" "${LOG_ATTEMPTS_YES}")"
 form_info_item "$Bap" "" "$(input_radio "LOG_INCOMING_ACCESS" "NO" "$Fno" "${LOG_INCOMING_ACCESS_NO}") $(input_radio "LOG_INCOMING_ACCESS" "YES" "$Fye" "${LOG_INCOMING_ACCESS_YES}")"
 form_info_item "$Baq" "" "$(input_radio "LOG_OUTGOING_ACCESS" "NO" "$Fno" "${LOG_OUTGOING_ACCESS_NO}") $(input_radio "LOG_OUTGOING_ACCESS" "YES" "$Fye" "${LOG_OUTGOING_ACCESS_YES}")"
 form_info_item "$Bar" "" "$(input_radio "DEBUG" "0" "$Fno" "${DEBUG_NO}") $(input_radio "DEBUG" "1" "$Fye" "${DEBUG_YES}")"
 form_info_item "$Bas" "" "$(input_text "MAX_CONNTRACK" "${MAX_CONNTRACK}" "20")"
 form_info_item "$Bau" "" "$(input_text "HD_SLEEP_TIME" "${HD_SLEEP_TIME}" "20")"
 end_table
 end_form
fi
cl_footer2
