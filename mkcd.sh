cd base
find . -name .gitignore -exec rm {} \;
./mkpackages.sh
find . -type d -empty -exec touch {}/.gitignore \;
cd ..
mkisofs -o srp.iso -R -J -l -b isolinux.bin -c boot.cat \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        cd

cd base
./mkpackages.sh clean
cd ..
