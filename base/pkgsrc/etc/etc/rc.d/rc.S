#! /bin/sh
#
# System single user startup script

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
umask 022

#
#Trap CTRL-C &c only in this shell so we can interrupt subprocesses.
#
trap ":" 2 3 20

# Mount devpts
mount -t devpts devpts /dev/pts

# Load the modules
sh /etc/rc.d/rc.modules

# Clean up /var/run and create /var/run/utmp so that we can login.
: > /var/run/utmp

# Set pseudo-terminal access permissions.
#chmod 666 /dev/tty[p-za-e][0-9a-f]
#chown root.tty /dev/tty[p-za-e][0-9a-f]

# Start the Multi-user configuration
. /tmp/boot.info
[ "$MEDIA"  = "CDROM" ] && /usr/sbin/install --cdrom
[ ! -e /tmp/reboot ] && /etc/rc.d/rc.M
