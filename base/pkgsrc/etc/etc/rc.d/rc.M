#!/bin/sh
#
# Coyote init script

. /tmp/boot.info
. /etc/coyote/coyote.conf
# If it's the first boot run the configuration wizard
#export TERMINFO=/etc/terminfo
#[ "$MEDIA" != "CDROM" ] && [ "$RUN_WIZARD" = "YES" ] && /usr/sbin/wizard --install

# Start the inet system
if [ ! -f /etc/coyote/coyote.conf ]; then
	echo
	echo "-------------------------ERROR--------------------------"
	echo "This Coyote boot disk does not appear to have been"
	echo "properly configured.  The network subsystem can not be"
	echo "configured.  Please rerun the Coyote Disk Creator."
	echo "--------------------------------------------------------"
	echo
	exit
fi

# Ensure basic filesystem sanity
chmod 755 /
chmod 1777 /tmp

# Load the coyote configuration file
. /etc/coyote/coyote.conf
. /tmp/boot.info

CONFIG_LOADED=YES

echo -n "Configure the root password ..."
if [ ! -z "$ADMIN_AUTH" ]; then
 [ -r /etc/shadow.tmp ] &&	rm /etc/shadow.tmp
 touch /etc/shadow.tmp
 chown root.root /etc/shadow.tmp
 chmod 600 /etc/shadow.tmp
 echo "root:\$1\$\$${ADMIN_AUTH}:10091:0:99999:7:::" >> /etc/shadow.tmp
 grep -v root: /etc/shadow >> /etc/shadow.tmp
 rm /etc/shadow
 mv /etc/shadow.tmp /etc/shadow
 echo "DONE"
else
 echo "FAULT"
fi

echo "Check for the SSH host keys"
if [ ! -r /etc/dropbear/dropbear_dss_host_key ]; then
 /usr/sbin/ssh-keygen -t dss -f /etc/dropbear/dropbear_dss_host_key
 NEW_KEYS=YES
 touch /tmp/need.save
fi
if [ ! -r /etc/dropbear/dropbear_rsa_host_key ]; then
 /usr/sbin/ssh-keygen -t rsa -f /etc/dropbear/dropbear_rsa_host_key
 NEW_KEYS=YES
 touch /tmp/need.save
fi
[ "$NEW_KEYS" = "YES" -a "$READONLY" = "no" ] && /usr/sbin/lrcfg.back ssh_keys

echo "Set the system clock"
if [ -z "$TZ" ]; then
 TZ="$(cat /etc/timezone)"
 echo "TZ=$TZ" >> /etc/coyote/coyote.conf
else
 echo "$TZ" > /etc/timezone
fi
cp /etc/timezone /etc/TZ
export TZ

# Set the clock using bios
[ -x /sbin/hwclock ] && /sbin/hwclock -s -l

# System loggers
SYSLOG_OPTS="-m 0 -C "
if [ ! -z "$LOGGING_HOST" ]; then
 SYSLOG_OPTS="$SYSLOG_OPTS -L -R $LOGGING_HOST"
 # If remote logging is requested, delay until after the network
 # is up
fi

#Create the wellcome screen
. /usr/sbin/mkissue.sh

echo "Starting network subsystems"

# Start the network
. /etc/rc.d/rc.inet

# Start any additional packages that were added
echo "Starting addon packages..."
SAVEDIR=`pwd`
cd /etc/rc.d/pkgs
for RCS in `ls rc.*`; do
  [ -x $RCS ] && /etc/rc.d/pkgs/$RCS
done
cd $SAVEDIR

[ -x /etc/rc.d/rc.subnet ] && . /etc/rc.d/rc.subnet

echo "Starting local packages..."
# Start any misc local commands
[ -x /etc/rc.d/rc.local ] && . /etc/rc.d/rc.local

