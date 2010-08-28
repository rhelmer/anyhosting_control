#!/bin/bash -x
#
# The rationale for doing it this way is explained in these blog posts:
# 
# http://anyhosting.com/blog/2009/10/01/secure-shared-web-hosting-on-ubuntu-server-part-1/
# http://anyhosting.com/blog/2009/10/03/secure-shared-web-hosting-on-ubuntu-server-part-2/
# http://anyhosting.com/blog/2009/10/04/secure-shared-web-hosting-on-ubuntu-server-part-3/

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
mkdir htdocs logs conf tmp usr etc lib bin var
chmod 700 conf tmp
chmod 701 htdocs
chmod 750 logs
chown www-data:${USERNAME} logs
chown ${USERNAME}:${USERNAME} htdocs tmp
echo "/usr            ${WEBDIR}/usr ext3 bind,ro      0       0" > /etc/fstab
echo "/etc            ${WEBDIR}/etc ext3 bind,ro      0       0" > /etc/fstab
echo "/lib            ${WEBDIR}/lib ext3 bind,ro      0       0" > /etc/fstab
echo "/bin            ${WEBDIR}/bin ext3 bind,ro      0       0" > /etc/fstab
echo "/var            ${WEBDIR}/var ext3 bind,ro      0       0" > /etc/fstab
mount -a
echo "TODO Configs copied into place, customize:"
cp /usr/local/etc/anyhosting_apache2.conf ${WEBDIR}/conf/apache2.conf
# TODO automate
echo "sensible-editor ${WEBDIR}/conf/apache2.conf"
cp /usr/local/etc/anyhosting_apache_proxy.conf /etc/apache2/sites-available/${DOMAIN}
# TODO automate
echo "sensible-editor /etc/apache2/sites-available/${DOMAIN}
a2ensite ${DOMAIN}
