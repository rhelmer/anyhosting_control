#!/bin/sh

USERNAME=$1
DOMAIN=$2
if [ $# != 2 ]
then
  echo "syntax: $0 <username> <domain>"
  exit 1
fi

WEBDIR="/var/www/${DOMAIN}"
useradd -d ${WEBDIR}/htdocs ${USERNAME}
mkdir ${WEBDIR}
chmod 701 ${WEBDIR}
cd ${WEBDIR}
mkdir htdocs logs conf tmp usr
chmod 700 conf tmp
chmod 701 htdocs
chmod 750 logs
chown www-data:${USERNAME} logs
chown ${USERNAME}:${USERNAME} htdocs tmp
echo "TODO Add to /etc/fstab and mount -a:"
echo "/usr            ${WEBDIR}/usr ext3 bind,ro      0       0"
echo "TODO Config copied into place, customize:"
cp /usr/local/etc/anyhosting_apache2.conf ${WEBDIR}/conf/apache2.conf
echo "sensible-editor ${WEBDIR}/conf/apache2.conf"
echo "TODO Create /etc/apache2/sites-enabled/${DOMAIN}"
