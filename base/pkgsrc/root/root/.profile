# ~/.profile: executed for shells.

export HOSTNAME=`hostname`
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export PS1="$HOSTNAME# "
export TERMINFO=/etc/terminfo

umask 022

if [ -n "$TERM" ] ; then
  . /tmp/boot.info
  . /etc/coyote/coyote.conf
  # If it's the first boot run the configuration wizard
  [ "$MEDIA" != "CDROM" ] && [ "$RUN_WIZARD" = "YES" ] && /usr/sbin/wizard --install
  /usr/sbin/menu
fi

if [ $? = 10 ] ; then
  exit
fi

cd /
