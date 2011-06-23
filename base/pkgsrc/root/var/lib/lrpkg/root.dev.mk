
cd /dev/

mknod null c 1 3

mkdir pts

#tty
makedevs tty c 4 0 0 63 >null 2>&1
makedevs ttyp c 3 0 0 9 >null 2>&1
makedevs ttyq c 3 16 0 9 >null 2>&1
makedevs ttyr c 3 32 0 9 >null 2>&1
makedevs ttys c 3 48 0 9 >null 2>&1

makedevs ptyp c 2 0 0 9 >null 2>&1
makedevs ptyq c 2 16 0 9 >null 2>&1
makedevs ptyr c 2 32 0 9 >null 2>&1
makedevs ptys c 2 48 0 9 >null 2>&1

mknod ptmx c 5 2 >null 2>&1

#PPP
mknod ppp c 108 0 >null 2>&1

#Serial ports
makedevs ttyS c 4 64 0 63 >null 2>&1

#IDE 
makedevs hda b 3 0 0 8 s >null 2>&1
makedevs hdb b 3 64 0 8 s >null 2>&1
makedevs hdc b 22 0 0 8 s >null 2>&1
makedevs hdd b 22 64 0 8 s >null 2>&1
makedevs hdg b 34 0 0 8 s >null 2>&1

#SCSI
makedevs sda b 8   0 0 8 s >null 2>&1
makedevs sdb b 8  16 0 8 s >null 2>&1
makedevs sdc b 8  32 0 8 s >null 2>&1
makedevs sdd b 8  48 0 8 s >null 2>&1
makedevs sde b 8  64 0 8 s >null 2>&1
makedevs sdf b 8  80 0 8 s >null 2>&1
makedevs sdg b 8  96 0 8 s >null 2>&1
makedevs sdh b 8 112 0 8 s >null 2>&1

#Block devs
makedevs ram b 1 0 0 7 >null 2>&1
makedevs loop b 7 0 0 7 >null 2>&1


mknod beep c 10 128 >null 2>&1
mknod modreq c 10 129 >null 2>&1
mknod watchdog c 10 130 >null 2>&1
mknod temperature c 10 131 >null 2>&1
mknod hwtrap c 10 132 >null 2>&1
mknod exttrp c 10 133 >null 2>&1
mknod rtc c 10 135 >null 2>&1
mknod relay8 c 10 140 >null 2>&1
mknod relay16 c 10 141 >null 2>&1
mknod msr c 10 142 >null 2>&1
mknod pciconf c 10 143 >null 2>&1
mknod nvram c 10 144 >null 2>&1
mknod hfmodem c 10 145 >null 2>&1
mknod led c 10 151 >null 2>&1
mknod apm_bios c 10 134 >null 2>&1
mknod mem c 1 1 >null 2>&1
mknod kmem c 1 2 >null 2>&1
mknod null c 1 3 >null 2>&1
mknod port c 1 4 >null 2>&1
mknod zero c 1 5 >null 2>&1
mknod full c 1 7 >null 2>&1
mknod random c 1 8 >null 2>&1
mknod urandom c 1 9 >null 2>&1
mknod initrd b 1 250 >null 2>&1
mknod tty c 5 0 >null 2>&1
mknod socksys c 30 0 >null 2>&1
mknod spx c 30 1 >null 2>&1

mknod inet/arp c 30 2 >null 2>&1
mknod inet/icmp c 30 2 >null 2>&1
mknod inet/ip c 30 2 >null 2>&1
mknod inet/tcp c 30 2 >null 2>&1
mknod inet/udp c 30 2 >null 2>&1

mknod fd0 b 2 0 >null 2>&1
mknod fd0h1200 b 2 8 >null 2>&1
mknod fd0h1440 b 2 40 >null 2>&1
mknod fd0h1476 b 2 56 >null 2>&1
mknod fd0h1494 b 2 72 >null 2>&1
mknod fd0h1600 b 2 92 >null 2>&1
mknod fd0u1040 b 2 84 >null 2>&1
mknod fd0u1120 b 2 88 >null 2>&1
mknod fd0u1440 b 2 28 >null 2>&1
mknod fd0u1600 b 2 124 >null 2>&1
mknod fd0u1680 b 2 44 >null 2>&1
mknod fd0u1722 b 2 60 >null 2>&1
mknod fd0u1743 b 2 76 >null 2>&1
mknod fd0u1760 b 2 96 >null 2>&1
mknod fd0u1840 b 2 116 >null 2>&1
mknod fd0u1920 b 2 100 >null 2>&1
mknod fd0u2880 b 2 32 >null 2>&1
mknod fd0u3200 b 2 104 >null 2>&1
mknod fd0u3520 b 2 108 >null 2>&1
mknod fd0u3840 b 2 112 >null 2>&1

mknod console c 5 1 >null 2>&1

#symlinks
ln -sf /proc/self/fd fd >null 2>&1
ln -sf fd/0 stdin >null 2>&1
ln -sf fd/1 stdout >null 2>&1
ln -sf fd/2 stderr >null 2>&1

#ln -sf tty1 console >null 2>&1
ln -sf socksys nfsd >null 2>&1
ln -sf null X0R >null 2>&1

ln -sf ram0 ramdisk >null 2>&1
ln -sf ram0 ram >null 2>&1

cd /
