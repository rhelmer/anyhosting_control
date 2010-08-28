#!/bin/bash
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

function fatal {
  EXIT_CODE=$?
  MSG=$1
  if [ $EXIT_CODE -ne 0 ]
  then
    echo "FATAL: exit code $EXIT_CODE"
    echo $MSG
    exit $EXIT_CODE
  fi
}

WEBDIR="/var/www/${DOMAIN}"
useradd -d ${WEBDIR}/htdocs ${USERNAME}
fatal "Could not add user: ${USERNAME}"
mkdir ${WEBDIR}
fatal "Could not create webdir: ${WEBDIR}"
chmod 701 ${WEBDIR}
fatal "Could not change mode on webdir: ${WEBDIR}"
cd ${WEBDIR}
fatal "Could not change working dir to webdir: ${WEBDIR}"
SUBDIRS="htdocs logs conf tmp usr etc lib bin var"
mkdir -p ${SUBDIRS}
fatal "Could not create webdir subdirs: ${SUBDIRS}"
chmod 700 conf tmp
fatal "Could not change mode on subdirs: conf tmp"
chmod 701 htdocs
fatal "Could not change mode on subdir htdocs"
chmod 750 logs
fatal "Could not change mode on subdir logs"
chown www-data:${USERNAME} logs
fatal "Could not chown logs to www-data:${USERNAME}"
chown ${USERNAME}:${USERNAME} htdocs tmp
echo "/usr            ${WEBDIR}/usr ext3 bind,ro      0       0" >> /etc/fstab
fatal "Could not add /usr to fstab"
echo "/etc            ${WEBDIR}/etc ext3 bind,ro      0       0" >> /etc/fstab
fatal "Could not add /etc to fstab"
echo "/lib            ${WEBDIR}/lib ext3 bind,ro      0       0" >> /etc/fstab
fatal "Could not add /lib to fstab"
echo "/bin            ${WEBDIR}/bin ext3 bind,ro      0       0" >> /etc/fstab
fatal "Could not add /bin to fstab"
echo "/var            ${WEBDIR}/var ext3 bind,ro      0       0" >> /etc/fstab
fatal "Could not add /var to fstab"
mount -a
fatal "Could not mount -a"
cp /usr/local/etc/anyhosting_apache2.conf ${WEBDIR}/conf/apache2.conf
fatal "Could not copy user apache config into webdir: ${WEBDIR}/conf/apache2.conf"
cp /usr/local/etc/anyhosting_apache_proxy.conf /etc/apache2/sites-available/${DOMAIN}
fatal "Could not copy system apache proxy config into system dir: /etc/apache2/sites-available/${DOMAIN}"
# TODO the rest is manual, automate
echo "TODO Configs copied into place, customize:"
echo "sensible-editor ${WEBDIR}/conf/apache2.conf"
echo "sensible-editor /etc/apache2/sites-available/${DOMAIN}
echo "/usr/sbin/a2ensite ${DOMAIN}"
