#! /bin/sh
#
# Coyote single user startup script

PATH=/sbin:/bin:/usr/sbin:/usr/bin
umask 022

#
#	Trap CTRL-C &c only in this shell so we can interrupt subprocesses.
#
trap ":" 2 3 20

# Mount devpts
mount -t devpts devpts /dev/pts

# Load the modules
if [ -x /etc/rc.d/rc.modules ]; then
	. /etc/rc.d/rc.modules
fi

# Clean up /var/run and create /var/run/utmp so that we can login.
: > /var/run/utmp

# Set pseudo-terminal access permissions.
#chmod 666 /dev/tty[p-za-e][0-9a-f]
#chown root.tty /dev/tty[p-za-e][0-9a-f]

#insmod softdog
#/sbin/watchdog -t 30 /dev/watchdog

# Start the Multi-user configuration
. /tmp/boot.info
[ "$MEDIA"  = "CDROM" ] && /usr/sbin/install --cdrom
[ ! -e /tmp/reboot ] && /etc/rc.d/rc.M
