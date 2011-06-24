#!/bin/sh
#

cd pkgsrc

for x in `ls *.*` ; do
	newdir=`echo "$x" | sed 's,\.tgz,,g'`
	#echo $newdir
	case $x in
		*.tgz)
			mkdir $newdir
			tar -zxf $x -C $newdir
			#echo $x
		;;
	esac
done

cd ..
