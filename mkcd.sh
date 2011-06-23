cd base
./mkpackages.sh
cd ..
mkisofs -o bfw.iso -R -J -l -b isolinux.bin -c boot.cat \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        cd

cd base
./mkpackages.sh clean
cd ..
