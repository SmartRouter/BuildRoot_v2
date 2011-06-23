
cd /dev/

#Default
chmod 660 * >null 2>&1

chmod 622 tty* >null 2>&1
chmod 666 ttyp* >null 2>&1
chmod 666 ttyq* >null 2>&1
chmod 666 ttyr* >null 2>&1
chmod 660 ttyS* >null 2>&1
chmod 666 tty >null 2>&1

chmod 666 pty* >null 2>&1

chmod 666 null >null 2>&1
chmod 666 zero >null 2>&1

chmod 622 full >null 2>&1

chmod 644 random >null 2>&1
chmod 644 urandom >null 2>&1

chmod 666 socksys >null 2>&1
chmod 666 spx >null 2>&1

chmod 666 inet/* >null 2>&1
chmod 755 inet/ >null 2>&1

cd /
