#!/bin/sh
# CRON CONFIGURATION - WEBADMIN SCRIPT
# Claudio Roberto Cussuol - claudio_cl@rictec.com.br
# 05/15/2005
#####################################################
# Bugs corrigidos por:
# Coidiloco e Antonelli2006
# 02/10/2009
#####################################################
# Edit - Fábio Leandro Janiszevski - fabiosammy - fabiosammy@gmail.com - 29/01/2010

. /var/http/web-functions
. /etc/coyote/coyote.conf
SCRIPT="cron.cgi"
FILE="/var/spool/cron/crontabs/root"
TMPFILE="/tmp/cron"
RELOAD="/usr/sbin/./cron.reload"

[ "$ENABLE_CRON" = "YES" ] && ENABLE_CRON_YES='checked' || ENABLE_CRON_NO='checked'

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

 MIN=`echo $MIN | sed s/\all/\$Pqk/g`
 DMIN="$MIN"
 [ "$MIN" = 'all' ] && DMIN="$Pqk"
 HOR=`echo $HOR | sed s/\all/\$Pqk/g`
 DHOR="$HOR"
 [ "$HOR" = 'all' ] && DHOR="$Pqk"
 DAY=`echo $DAY | sed s/\all/\$Pqk/g`
 DDAY="$DAY"
 [ "$DAY" = 'all' ] && DDAY="$Pqk"
 MON=`echo $MON | sed s/\all/\$Pqk/g`
 DMON="$MON"
 [ "$MON" = 'all' ] && DMON="$Pqk"
 WEK=`echo $WEK | sed s/\all/\$Pqk/g`
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
 ENABLE_CRON=$FORM_ENABLE_CRON
 cl_rebuildconf
}
#==================================
show_list() {
 init_table "maintable"
 add_new "$Pqi" "$Pqj"
 init_add_control "$Lce"
 add_control "$SCRIPT?ACTION=RELOAD" "$Pqg"
 add_control "editconf.cgi?CONFFILE=$FILE&DESCFILE=$Pjv" "$Pqh"
 end_add_control
 end_table
 echo "<br>"
 if [ "$ENABLE_CRON" = "YES" ]; then
	init_form "$SCRIPT?ACTION=RELOAD"
	init_main_table
	add_title "$Pjv"
	form_info_item "$Ban" "" "$(input_radio_cron "ENABLE_CRON" "NO" "$Fno") $(input_radio_cron "ENABLE_CRON" "YES" "$Fye" "checked")"
	end_table
	end_form
 else
	init_form "$SCRIPT?ACTION=RELOAD"
	init_main_table
	add_title "$Pjv"
	form_info_item "$Ban" "" "$(input_radio_cron "ENABLE_CRON" "NO" "$Fno" "checked") $(input_radio_cron "ENABLE_CRON" "YES" "$Fye")"
	end_table
	end_form
 fi
 init_main_table
 add_title "$Msg" "6"
 header_table "$Pqa" "$Pqb" "$Pqc" "$Pqd" "$Pqe" "$Pqf"
 LINECOUNT=0
 cat $FILE | sed s/\*/\all/g | awk -vPqk=$Pqk '{
	COMAND=$6" "$7" "$8" "$9" "$10" "$11" "$12" "$13" "$14" "$15;
	{ if ($1 == "all") { MIN=Pqk } else { MIN = $1 } }
	{ if ($2 == "all") { HOUR=Pqk } else { HOUR = $2 } }
	{ if ($3 == "all") { DAY_MONTH=Pqk } else { DAY_MONTH = $3 } }
	{ if ($4 == "all") { MONTH=Pqk } else { MONTH = $4 } }
	{ if ($5 == "all") { WEEK=Pqk } else { WEEK = $5 } }
	}{print MIN" "HOUR" "DAY_MONTH" "MONTH" "WEEK" "COMAND}'| while read DMIN DHOR DDAY DMON DWEK SCR; do
	 LINECOUNT=$(($LINECOUNT+1))
	 case "$DMIN" in
		\#*|"") continue;;
		*) output_line "$DMIN" "$DHOR" "$DDAY" "$DMON" "$DWEK" "$SCR";;
	 esac
	done
 end_table
}
#==================================
show_form() {
 FMIN=`echo $FMIN | sed s/\$Pqk/\*/g`
 FHOR=`echo $FHOR | sed s/\$Pqk/\*/g`
 FDAY=`echo $FDAY | sed s/\$Pqk/\*/g`
 FMON=`echo $FMON | sed s/\$Pqk/\*/g`
 FWEK=`echo $FWEK | sed s/\$Pqk/\*/g`
 [ "$FMIN" = '*' ] && FMIN=""
 [ "$FHOR" = '*' ] && FHOR=""
 [ "$FDAY" = '*' ] && FDAY=""
 [ "$FMON" = '*' ] && FMON=""
 [ "$FWEK" = '*' ] && FWEK=""
 init_form
 input_hidden "ENABLE_CRON" "$ENABLE_CRON"
 init_main_table
 add_title "$Msg"
 add_message_form "$Pql"
 form_info_item "$Pqa" "$Pqm" "$(input_text "MIN" "$FMIN" "22")"
 form_info_item "$Pqb" "$Pqn" "$(input_text "HOR" "$FHOR" "22")"
 form_info_item "$Pqc" "$Pqo" "$(input_text "DAY" "$FDAY" "22")"
 form_info_item "$Pqd" "$Pqp" "$(input_text "MON" "$FMON" "22")"
 form_info_item "$Pqe" "$Pqq" "$(input_text "WEK" "$FWEK" "22")"
 form_info_item "$Pqf" "$Pqr" "$(input_text "SCR" "$SCR" "22")"
 end_table
 end_form
}
#==================================
# MAIN ROUTINE
cl_header2 "$Msg"
if [ "$FORM_OKBTN" = "$Fsb" ]; then
 mount_configuration
 if [ -n "$CONFIG_LINE" ]; then
	[ "$FORM_ACTION" = "ADD" ] && addline "${CONFIG_LINE//XaXlXlX/*}" $FILE || changeline $FORM_LINE "${CONFIG_LINE//XaXlXlX/'*'}" $FILE
	alert "$Pqs" "$Pqu"
 fi
fi

case "$FORM_ACTION" in
 "DELETE")
	deleteline "$FORM_LINE" $FILE
	alert "$Pqt" "$Pqu"
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
 "RELOAD") command_reload;;
 *) show_list;;
esac

cl_footer2
