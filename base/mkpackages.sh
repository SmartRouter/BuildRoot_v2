#!/bin/sh
#
#

create_advroute() {
	echo "Creating Advanced Router Package"
	# Reset the modules definition file
	> pkgsrc/advroute/etc/modules.advroute
	# Reset the modules directory
	rm -f pkgsrc/advroute/lib/modules/advroute/*
	for REQMODS in `cat data/modules.advroute`; do
		cp drivers/$REQMODS.o pkgsrc/advroute/lib/modules/advroute 1>&2 > /dev/null
		if [ $? = 0 ]; then
			echo $REQMODS >> pkgsrc/advroute/etc/modules.advroute
		else
			echo "Error copying module file: $REQMODS.o"
			exit 1
		fi	
	done
}

create_bridge() {
	echo "Creating Bridge Package"
	# Reset the modules definition file
	> pkgsrc/bridge/etc/modules.bridge
	# Reset the modules directory
	rm -f pkgsrc/bridge/lib/modules/bridge/*
	for REQMODS in `cat data/modules.bridge`; do
		cp drivers/$REQMODS.o pkgsrc/bridge/lib/modules/bridge 1>&2 > /dev/null
		if [ $? = 0 ]; then
			echo $REQMODS >> pkgsrc/bridge/etc/modules.bridge
		else
			echo "Error copying module file: $REQMODS.o"
			exit 1
		fi
	done
}

create_drivers() {
	echo "Creating Drivers Package"
	# Reset the modules definition file
	> pkgsrc/drivers/etc/modules.drivers
	# Reset the modules directory
	rm -f pkgsrc/drivers/lib/modules/drivers/*
	for REQMODS in `cat data/modules.drivers`; do
		cp drivers/$REQMODS.o pkgsrc/drivers/lib/modules/drivers 1>&2 > /dev/null
		if [ $? = 0 ]; then
			echo $REQMODS >> pkgsrc/drivers/etc/modules.drivers
		else
			echo "Error copying module file: $REQMODS.o"
			exit 1
		fi
	done
}

create_modules() {
	echo "Creating Modules Package"
	# Reset the modules definition file
	> pkgsrc/modules/etc/modules
	# Reset the modules directory
	rm -f pkgsrc/modules/lib/modules/*.o
	for REQMODS in `cat data/modules.modules`; do
		cp drivers/$REQMODS.o pkgsrc/modules/lib/modules 1>&2 > /dev/null
		if [ $? = 0 ]; then
			echo $REQMODS >> pkgsrc/modules/etc/modules
		else
			echo "Error copying module file: $REQMODS.o"
			exit 1
		fi
	done
}

create_l7filter() {
	echo "Creating l7filter Package"
	cp drivers/ipt_layer7.o pkgsrc/l7filter/lib/modules 1>&2 > /dev/null
}

create_root() {
	echo "Creating root Package"
	mknod pkgsrc/root/dev/tty1 c 4 1
	mknod pkgsrc/root/dev/tty2 c 4 2
	mknod pkgsrc/root/dev/tty3 c 4 3
        mknod pkgsrc/root/dev/ttyS0 c 4 64
}

buildpkg (){
	echo "Building package: $1"
	rm -f ../packages/${1}.tgz 2>&1 > /dev/null
	cd $1
	tar -cf ../../packages/${1}.tar *
	cd ../../packages
	gzip -9 ${1}.tar
	mv ${1}.tar.gz ${1}.tgz
	cd ../pkgsrc
}


buildall() {
  ln -s ../cd packages

#  create_modules
#  create_drivers
#  create_advroute
#  create_bridge
#  create_l7filter
#  create_root

  cd pkgsrc
#  buildpkg advroute
  buildpkg bridge
#  buildpkg dhcpd
  buildpkg etc
  buildpkg iwtools
#  buildpkg l7filter
  buildpkg root
  buildpkg webadmin
  buildpkg modules
  buildpkg modules_smp
  mv ../packages/modules_smp.tgz ../packages/SMP/modules.tgz
#  buildpkg drivers
  buildpkg hdtools
  buildpkg hdparm
  buildpkg language
  buildpkg ssh_keys
  buildpkg acpid
  buildpkg rrdtool
  cd ..

  rm -rf packages

  echo > ../cd/SRP.dpy
  echo -n "SmartRouter PROJECT v" >> ../cd/SRP.dpy
  cat pkgsrc/root/var/lib/lrpkg/root.version >> ../cd/SRP.dpy
  echo >> ../cd/SRP.dpy
  echo "http://www.smartrouter.com.br" >> ../cd/SRP.dpy
  echo >> ../cd/SRP.dpy
}

reset_all() {
  echo "Cleaning...."

  rm -f ../cd/*.tgz 1>&2 > /dev/null
  rm -f ../cd/SMP/*.tgz 1>&2 > /dev/null

  #rm -f pkgsrc/modules/etc/modules
  #rm -f pkgsrc/modules/lib/modules/*.o 1>&2 > /dev/null

  #rm -f pkgsrc/advroute/etc/modules.advroute
  #rm -f pkgsrc/advroute/lib/modules/advroute/* 1>&2 > /dev/null

  #rm -f pkgsrc/bridge/etc/modules.bridge
  #rm -f pkgsrc/bridge/lib/modules/bridge/* 1>&2 > /dev/null

  #rm -f pkgsrc/l7filter/lib/modules/ipt_layer7.o 1>&2 > /dev/null

  #rm -f pkgsrc/drivers/etc/modules.drivers
  #rm -f pkgsrc/drivers/lib/modules/drivers/* 1>&2 > /dev/null

  #rm -f pkgsrc/ppp/etc/etc/peers/*
  #rm -f pkgsrc/ppp/etc/etc/*-secrets
  #rm -f pkgsrc/ppp/etc/etc/*.chat
  #rm -f pkgsrc/ppp/etc/etc/options

  rm -f pkgsrc/etc/etc/ssh/ssh_host_key*

  #rm -f pkgsrc/language/var/http/language/*

  rm -f pkgsrc/root/dev/* > /dev/null
}

reset_all

[ -z "$1" ] && buildall

echo "Done."
