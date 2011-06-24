#!/bin/sh
# QOS webadmin configuration
# Author: Dolly <dolly@czi.cz>
. /var/http/web-functions
. /etc/qos.config
. /etc/coyote/coyote.conf
RELOAD="/etc/rc.d/rc.qos"
cl_header2 "$Mqc - SmartRouter"
if ! [ "$FORM_OKBTN" = "$Fsv" ] && [ -z $FORM_ACTION ]; then
#----------------------------------------------HTML---------------------------------------------------
CHK1=
CHK2=
CHK3=
CHK4=
case $QOS_TYPE in
	DISABLED)
 	   CHK1=checked
	   ;;
	COYOTE_DEFAULT)
 	   CHK2=checked
	   ;;
	COYOTE_MANUAL)
 	   CHK3=checked
	   ;;
	SUBNET)
 	   CHK4=checked
	   ;;
	CUSTOM)
 	   CHK5=checked
	   ;;
	*) CHK1=checked
	   ;;
esac
cat << CLEOF
<form method="POST" action="/cgi-bin/qos.cgi"><table class=maintable border=0 width="100%"><tr><th colspan=2>$Pea</th></tr>
<tr><td width="50%" class=row1 align=right valign=top><b>$Peb &nbsp;</b></td>
 <td class=row2 nowrap>
   <input type=radio value=DISABLED ${CHK1} name=QOS_TYPE>$Pec<br>
   <input type=radio value=COYOTE_DEFAULT ${CHK2} name=QOS_TYPE>$Ped<br>
   <input type=radio value=COYOTE_MANUAL ${CHK3} name=QOS_TYPE>$Pee<br>
   <input type=radio value=SUBNET ${CHK4} name=QOS_TYPE>$Psw<br>
   <input type=radio value=CUSTOM ${CHK5} name=QOS_TYPE>$Psx<br></td></tr>
<tr><td class=row1 align=right valign=top><b>$Peg &nbsp;</b>&nbsp;</td><td class=row2 valign=top><input type=text value="$QOS_DOWNSTREAM" name=QOS_DOWNSTREAM size=8>&nbsp;kbit/s</td></tr>
<tr><td class=row1 align=right valign=top><b>$Peh &nbsp;</b>&nbsp;</td><td class=row2 valign=top><input type=text value="$QOS_UPSTREAM" name=QOS_UPSTREAM size=8>&nbsp;kbit/s</td></tr>
<tr><td class=row1 align=right valign=top><b>ZPH ($Psw) &nbsp;</b>&nbsp;</td><td class=row2 valign=top><input type=text value="$QOS_ZPH" name=QOS_ZPH size=8>&nbsp;kbit/s</td></tr>
</table>
CLEOF
if [ "$QOS_TYPE" != "" -a "$QOS_TYPE" != "DISABLED" ]; then
cat << CLEOF
<br><table class=maintable width=100%><tr><th colspan=4>$Pei</th></tr>
CLEOF
if [ "$QOS_TYPE" = "COYOTE_DEFAULT" -o "$QOS_TYPE" = "COYOTE_MANUAL" ]; then
cat << CLEOF
<tr><td width=50% colspan=2 align=right class=row1><b>$Pej -&gt; $Pek</b></td><td width=50% colspan=2 class=row2><input type=text value="$QOS_UPFW_STREAM" name=QOS_UPFW_STREAM size=5>% (5-80)</td></tr>
<tr><td colspan=4 class=row3 align=center><b>$Pel</b><br>$Pem $Pen</td></tr>
<tr><td colspan=2 align=right class=row1><b>$Peo &nbsp;</b></td><td class=row2><input type=text value="$QOS_HIGH_PRI_PER" name=QOS_HIGH_PRI_PER size=5>%</td><td rowspan=3 width=100% nowrap class=row2>$Pep</td></tr>
<tr><td colspan=2 align=right class=row1><b>$Peq &nbsp;</b></td><td class=row2><input type=text value="$QOS_NORM_PRI_PER" name=QOS_NORM_PRI_PER size=5>%</td></tr>
<tr><td colspan=2 align=right class=row1><b>$Per &nbsp;</b></td><td class=row2><input type=text value="$QOS_SLOW_PRI_PER" name=QOS_SLOW_PRI_PER size=5>%</td></tr>
CLEOF
fi
cat << CLEOF
<tr><th colspan=2 width=50%>UPSTREAM</th><th colspan=2 width=50%>DOWNSTREAM</th></tr><tr><td colspan=4 class=row3 align=center><b>$Pes</b><br>$Pet</td></tr>
<tr><td width=25% class=row1 align=right><b>$Peu &nbsp;</b></td><td width=25% class=row1><input type=text value="$QOS_FUP_BURST" name=QOS_FUP_BURST size=5>kB</td>
 <td width=25% class=row2 align=right><b>$Peu &nbsp;</b></td><td width=25% class=row2><input type=text value="$QOS_FDOWN_BURST" name=QOS_FDOWN_BURST size=5>kB</td></tr>
<tr><td class=row1 align=right><b>$Pev &nbsp;</b></td><td class=row1><input type=text value="$QOS_NUP_BURST" name=QOS_NUP_BURST size=5>kB</td>
 <td class=row2 align=right><b>$Pev &nbsp;</b></td><td class=row2><input type=text value="$QOS_NDOWN_BURST" name=QOS_NDOWN_BURST size=5>kB</td></tr>
<tr><td class=row1 align=right><b>$Pew &nbsp;</b></td><td class=row1><input type=text value="$QOS_SUP_BURST" name=QOS_SUP_BURST size=5>kB</td>
 <td class=row2 align=right><b>$Pew &nbsp;</b></td><td class=row2><input type=text value="$QOS_SDOWN_BURST" name=QOS_SDOWN_BURST size=5>kB</td></tr>
<tr><td colspan=4 class=row3 align=center><b>$Pex</b><br>$Pey</td></tr>
<tr><td class=row1 align=right><b>$Pez</b></td><td class=row1><input type=text value="$QOS_UPSTREAM_INDIVIDUAL" name=QOS_UPSTREAM_INDIVIDUAL size=5>%</td>
 <td class=row2 align=right><b>$Pfa</b></td><td class=row2><input type=text value="$QOS_DOWNSTREAM_INDIVIDUAL" name=QOS_DOWNSTREAM_INDIVIDUAL size=5>%</td></tr>
<tr><td colspan=4 class=row3 align=center><b>$Pfb</b><br>$Pfc</td></tr>
<tr><td class=row1 align=right><b>$Pfd &nbsp;</b></td><td class=row1><input type=text value="$QOS_UPSTREAM_JUNK" name=QOS_UPSTREAM_JUNK size=5>% (5-80%)</td>
 <td class=row2 align=right><b>$Pfe &nbsp;</b></td><td class=row2><input type=text value="$QOS_DOWNSTREAM_JUNK" name=QOS_DOWNSTREAM_JUNK size=5>% (5-80%)</td></tr>
</table>
CLEOF
fi
cat << CLEOF
<p align=center><input type=submit value="$Fsv" name=OKBTN><input type=reset value="$Fer"></p>
<table class=maintable><tr><td class=row1><b>$Pff</b></td>
<td class=row2>[&nbsp; <a href=qosfilter.cgi><u>$Pfg</u></a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href=qosclasses.cgi><u>$Pfh</u></a> &nbsp;| 
&nbsp;<a href="editconf.cgi?CONFFILE=/etc/rc.d/rc.qos.custom&DESCFILE=Custom QOS Script"><u>$Psy</u></a> &nbsp;]</td></tr>
<tr><td cass=row1><b>$Egf</b></td><td class=row2>[ &nbsp;<a href=qos.cgi?ACTION=RELOAD><u>$Pfi</u></a>&nbsp;|&nbsp;<a href="qosstatus.cgi"><u>$Pfj</u></a> ]</td></tr>
</table></form>
CLEOF
#-------------------------------------- END HTML -----------------------------------------------
# Process Form Submission
elif [ "$FORM_ACTION" = "RELOAD" ]; then
	echo "<br><pre>"
	$RELOAD
	echo "</pre><center><div id=back><a href="qos.cgi">$Pfk</a></div></center><br>"
else
	MAINCONFIGCHANGED=
	[ "$FORM_QOS_TYPE" != "$QOS_TYPE" ] && { QOS_TYPE=$FORM_QOS_TYPE; MAINCONFIGCHANGED=yes; }
	[ "$FORM_QOS_DOWNSTREAM" != "$QOS_DOWNSTREAM" ] && QOS_DOWNSTREAM=$FORM_QOS_DOWNSTREAM
	[ "$FORM_QOS_UPSTREAM" != "$QOS_UPSTREAM" ] && QOS_UPSTREAM=$FORM_QOS_UPSTREAM
	[ "$FORM_QOS_ZPH" != "$QOS_ZPH" ] && QOS_ZPH=$FORM_QOS_ZPH

#      if [ "$QOS_TYPE" = "COYOTE_DEFAULT" -o "$QOS_TYPE" = "COYOTE_MANUAL" ]; then

	[ ! -z "$FORM_QOS_FUP_BURST" ] && QOS_FUP_BURST=$FORM_QOS_FUP_BURST
	[ ! -z "$FORM_QOS_NUP_BURST" ] && QOS_NUP_BURST=$FORM_QOS_NUP_BURST
	[ ! -z "$FORM_QOS_SUP_BURST" ] && QOS_SUP_BURST=$FORM_QOS_SUP_BURST
	[ ! -z "$FORM_QOS_FDOWN_BURST" ] && QOS_FDOWN_BURST=$FORM_QOS_FDOWN_BURST
	[ ! -z "$FORM_QOS_NDOWN_BURST" ] && QOS_NDOWN_BURST=$FORM_QOS_NDOWN_BURST
	[ ! -z "$FORM_QOS_SDOWN_BURST" ] && QOS_SDOWN_BURST=$FORM_QOS_SDOWN_BURST

	if [ ! -z "$FORM_QOS_HIGH_PRI_PER" ] && [ ! -z "$FORM_QOS_NORM_PRI_PER" ] && [ ! -z "$FORM_QOS_SLOW_PRI_PER" ]; then
	    if [ "$FORM_QOS_HIGH_PRI_PER" -gt 0 ] 2>/dev/null && [ "$FORM_QOS_NORM_PRI_PER" -gt 0 ] 2>/dev/null && [ "$FORM_QOS_SLOW_PRI_PER" -gt 0 ] 2>/dev/null; then
		if [ $((${FORM_QOS_HIGH_PRI_PER}+${FORM_QOS_NORM_PRI_PER}+${FORM_QOS_SLOW_PRI_PER})) -eq 100 ] 2>/dev/null; then
		   QOS_HIGH_PRI_PER=$FORM_QOS_HIGH_PRI_PER
		   QOS_NORM_PRI_PER=$FORM_QOS_NORM_PRI_PER
		   QOS_SLOW_PRI_PER=$FORM_QOS_SLOW_PRI_PER
		else
                   echo "<center><div id=back>$Pfl</div></center><br>"
		fi
	    else
                   echo "<center><div id=back>$Pfm</div></center><br>"
	    fi
	else
                   echo "<center><div id=back>$Pfn</div></center><br>"
	fi

	if [ ! -z "$FORM_QOS_UPFW_STREAM" ]; then
	  if [ "$FORM_QOS_UPFW_STREAM" -ge 5 ] 2>/dev/null && [ "$FORM_QOS_UPFW_STREAM" -le 80 ] 2>/dev/null; then
	     QOS_UPFW_STREAM=$FORM_QOS_UPFW_STREAM
	  else
                   echo "<center><div id=back>$Pfo -&gt; $Pfp</div></center><br>"
	  fi
	fi
#     fi	

     if [ "$QOS_TYPE" != "" -a "$QOS_TYPE" != "DISABLED" ]; then
	[ -n "$FORM_QOS_UPSTREAM_JUNK" ]   && QOS_UPSTREAM_JUNK=$FORM_QOS_UPSTREAM_JUNK
        [ -n "$FORM_QOS_DOWNSTREAM_JUNK" ] && QOS_DOWNSTREAM_JUNK=$FORM_QOS_DOWNSTREAM_JUNK
	QOS_DOWNSTREAM_INDIVIDUAL=$FORM_QOS_DOWNSTREAM_INDIVIDUAL
	QOS_UPSTREAM_INDIVIDUAL=$FORM_QOS_UPSTREAM_INDIVIDUAL
     fi
 	cl_rebuildconf
	echo "<center><div id=back>$Wsv $Pfs"

	if [ ! -z "$MAINCONFIGCHANGED" ]; then
	  echo "<br>$Pft"
	fi

	echo "</div></center><br>"
	echo "<center><div id=back><a href="qos.cgi">$Pfk</a></div></center><br>"
fi
cl_footer2
