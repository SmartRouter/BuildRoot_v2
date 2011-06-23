#!/bin/sh
#
# Changed by: Claudio Roberto Cussuol 07-08-2004

# Source the coyote configuration file
if [ -z "$CONFIG_LOADED" ]; then
	. /etc/coyote/coyote.conf
fi

if [ -z "$PPP_ISP" -a "$INETTYPE" = "PPP" ] ; then
  PPP_ISP="isp"
  echo PPP_ISP=$PPP_ISP >> /etc/coyote/coyote.conf
fi

echo "Performing On-The-Fly config of PPP Options"

#-*-*-*-*-*-*-* Create peers file
echo "$PPP_MODEMTTY $PPP_PORTSPEED crtscts" > /etc/ppp/peers/$PPP_ISP
echo "user '$PPP_USERNAME' connect '/usr/sbin/chat -v -f /etc/ppp/${PPP_ISP}.chat'" >> /etc/ppp/peers/$PPP_ISP
echo "noauth" >> /etc/ppp/peers/$PPP_ISP

#-*-*-*-*-*-*-* Create chap-secrets file
# --- A * will make the secret usable without knowing the peers name.
echo "$PPP_USERNAME * $PPP_PASSWORD *" > /etc/ppp/chap-secrets
chmod 600 /etc/ppp/chap-secrets

#-*-*-*-*-*-*-* Create pap-secrets file
# --- A * will make the secret usable without knowing the peers name.
echo "$PPP_USERNAME * $PPP_PASSWORD *" > /etc/ppp/pap-secrets
chmod 600 /etc/ppp/pap-secrets

#-*-*-*-*-*-*-* Create chat file
#--------------------------------------------
# Two possible chat files: without or with login.

if [ "$PPP_CHATLOGIN" = "YES" ]; then
    echo "REPORT 'CONNECT'" > /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'BUSY'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'ERROR'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'NO CARRIER'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'NO DIALTONE'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'Invalid Login'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'Login incorrect'" >> /etc/ppp/$PPP_ISP.chat
    echo "'' '$PPP_INITSTR'" >> /etc/ppp/$PPP_ISP.chat
    echo "OK 'ATDT$PPP_PHONENUM'" >> /etc/ppp/$PPP_ISP.chat
    echo "CONNECT ''" >> /etc/ppp/$PPP_ISP.chat
    echo "'ogin:' '$PPP_USERNAME'" >> /etc/ppp/$PPP_ISP.chat
    echo "'ord:' '$PPP_PASSWORD'" >> /etc/ppp/$PPP_ISP.chat
    echo "TIMEOUT '5'" >> /etc/ppp/$PPP_ISP.chat
    echo "'~--' ''" >> /etc/ppp/$PPP_ISP.chat
    chmod 0600 /etc/ppp/$PPP_ISP.chat
else
    echo "REPORT 'CONNECT'" > /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'BUSY'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'ERROR'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'NO CARRIER'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'NO DIALTONE'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'Invalid Login'" >> /etc/ppp/$PPP_ISP.chat
    echo "ABORT 'Login incorrect'" >> /etc/ppp/$PPP_ISP.chat
    echo "'' '$PPP_INITSTR'" >> /etc/ppp/$PPP_ISP.chat
    echo "OK 'ATDT$PPP_PHONENUM'" >> /etc/ppp/$PPP_ISP.chat
    echo "CONNECT '\d\c'" >> /etc/ppp/$PPP_ISP.chat
fi

#-*-*-*-*-*-*-* Create options file
echo "lock" > /etc/ppp/options
if [ "$PPP_DEMANDDIAL" != "NO" ]; then
	echo "demand" >> /etc/ppp/options
	echo "idle $PPP_DEMANDDIAL" >> /etc/ppp/options
fi
if [ "$PPP_STATICIP" = "NO" ]; then
	echo "$PPP_LOCALREMOTE:$PPP_LOCALREMOTE" >> /etc/ppp/options
	echo "ipcp-accept-local" >> /etc/ppp/options
	echo "ipcp-accept-remote" >> /etc/ppp/options
	echo "noipdefault" >> /etc/ppp/options
else
	echo "$PPP_STATICIP:0.0.0.0" >> /etc/ppp/options
	echo "ipcp-accept-remote" >> /etc/ppp/options
fi

echo "holdoff 10" >> /etc/ppp/options
echo "defaultroute" >> /etc/ppp/options
echo "usepeerdns" >> /etc/ppp/options
if [ "$IP_FILTERING" = "YES" ]; then
  echo "active-filter 'outbound'" >> /etc/ppp/options
fi
echo "maxfail 0" >> /etc/ppp/options
