#/bin/sh
# do NOT use this script from XBMC addons directory, it is intented for development only
DESTDIR=~/.xbmc/addons/plugin.video.rtvs.sk

rm -rf ${DESTDIR}
mkdir -p ${DESTDIR}
cp -a * ${DESTDIR}
