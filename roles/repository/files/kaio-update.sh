#!/usr/bin/env bash

/usr/bin/rsync -avz --delete --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/os/x86_64/ /var/www/html/repos/centos/7/os/x86_64/
/usr/bin/rsync -avz --delete --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/updates/x86_64/ /var/www/html/repos/centos/7/updates/x86_64/
#/usr/bin/rsync -avz --delete --exclude='repo*' --exclude='debug' rsync://mirrors.rit.edu/epel/7/x86_64/ /var/www/html/repos/epel/7/x86_64/

/usr/bin/createrepo --update /var/www/html/repos/centos/7/os/x86_64/
/usr/bin/createrepo --update /var/www/html/repos/centos/7/updates/x86_64/
#/usr/bin/createrepo --update /var/www/html/repos/epel/7/x86_64/