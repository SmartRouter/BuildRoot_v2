#!/bin/sh
# Write the status of the network subsystems to a temp file for later use
# Changed to support subnet QOS in others LAN interfaces
# by BFW user "agsoliveira" - Revision by BFW user "marcos do vale" - 10/09/2007

echo "IF_LOCAL=${IF_LOCAL}" >> /tmp/netsubsys.state
echo "LOCAL_UP=${LOCAL_UP}" >> /tmp/netsubsys.state
echo "IF_INET=${IF_INET}" >> /tmp/netsubsys.state
echo "INET_UP=${INET_UP}" >> /tmp/netsubsys.state
[ -n "$IF_DMZ" ] && echo "IF_DMZ=${IF_DMZ}" >> /tmp/netsubsys.state
[ -n "$DMZ_UP" ] && echo "DMZ_UP=${DMZ_UP}" >> /tmp/netsubsys.state
[ -n "$IF_LOCAL2" ] && echo "IF_LOCAL2=${IF_LOCAL2}" >> /tmp/netsubsys.state
[ -n "$LOCAL2_UP" ] && echo "LOCAL2_UP=${LOCAL2_UP}" >> /tmp/netsubsys.state
[ -n "$IF_LOCAL3" ] && echo "IF_LOCAL3=${IF_LOCAL3}" >> /tmp/netsubsys.state
[ -n "$LOCAL3_UP" ] && echo "LOCAL3_UP=${LOCAL3_UP}" >> /tmp/netsubsys.state
[ -n "$IF_LOCAL4" ] && echo "IF_LOCAL4=${IF_LOCAL4}" >> /tmp/netsubsys.state
[ -n "$LOCAL4_UP" ] && echo "LOCAL4_UP=${LOCAL4_UP}" >> /tmp/netsubsys.state
[ -n "$IF_WLAN" ] && echo "IF_WLAN=${IF_WLAN}" >> /tmp/netsubsys.state
[ -n "$WLAN_UP" ] && echo "WLAN_UP=${WLAN_UP}" >> /tmp/netsubsys.state
[ -n "$IF_INET2" ] && echo "IF_INET2=${IF_INET2}" >> /tmp/netsubsys.state
[ -n "$INET2_UP" ] && echo "INET2_UP=${INET2_UP}" >> /tmp/netsubsys.state
[ -n "$IF_INET3" ] && echo "IF_INET3=${IF_INET3}" >> /tmp/netsubsys.state
[ -n "$INET3_UP" ] && echo "INET3_UP=${INET3_UP}" >> /tmp/netsubsys.state
[ -n "$IF_INET4" ] && echo "IF_INET4=${IF_INET4}" >> /tmp/netsubsys.state
[ -n "$INET4_UP" ] && echo "INET4_UP=${INET4_UP}" >> /tmp/netsubsys.state
[ -n "$CONNECTTIME" ] && echo CONNECTTIME=\"$CONNECTTIME\" >> /tmp/netsubsys.state
[ -n "$CONNECTSTRING" ] && echo CONNECTSTRING=\"$CONNECTSTRING\" >> /tmp/netsubsys.state

cat /tmp/netsubsys.state 1> /dev/null 2> /dev/null
