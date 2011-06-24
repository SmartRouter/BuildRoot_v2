#!/bin/bash
#
# extrairtudo
#
# script que extrai todos os arquivos (.zip, .tar, .tar.gz, .tgz, tar.bz2, .bz2)
# do diretório atual em um outro diretório especificado
#
# precisa de: unzip, tar, gzip e bzip2
#
# Autor: Xerxes Lins (xerxeslins@gmail.com)
#

#Echo () { echo -e "\e[33;1m$*\e[m" ; }
#echo
#Echo " -> você está em" $(pwd)
#echo "digite o caminho do destino: "
#read exdir

#if [[ ! -dw $exdir ]]
#then
#Echo diretório inexistente ou sem permissão de escrita
#exit
##else
# continue
#fi


for x in `ls *.*` ; do
newdir=`echo "$x" | sed 's,\.tgz,,g'`
echo $newdir
case $x in
*.tgz)
mkdir $newdir
tar -zxf $x -C $newdir
echo $x
;;

#*.tar.gz | *.tgz)
#tar -zxf $x -C $exdir
#3echo $x
#;;
#
#3*.gz)
#gunzip $x -c $exdir
#echo $x
#;;
#
#*.zip)
#unzip -oq $x -d $exdir
#echo $x
#;;
#
#*.tar.bz2 | *.tbz)
#tar -jxf $x -C $exdir
#echo $x
#;;
#
#*.bz2)
#cp $x $exdir
#bunzip2 $exdir/$x
#echo $x
#;;
esac
done
