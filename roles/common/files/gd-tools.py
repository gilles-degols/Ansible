#!/usr/bin/python2.7

import sys
import os
import time

"""
    This file contains basic tools available outside the docker
"""

class MySQL:
    def is_started(self, container_name, password):
        # MySQL can take some time to boot (like easily 30s)
        filename = '/tmp/docker.mysql.'+container_name+'.txt'
        waiting = True
        n = 0
        while waiting:
            os.system('docker exec ' + container_name + ' mysql -uroot -p"' + password + '" -Bse "SHOW DATABASES;" > '+filename)
            if os.path.isfile(filename):
                f = open(filename, 'r')
                for line in f:
                    if line.strip() == 'performance_schema':
                        waiting = False
                f.close()
                os.remove(filename)

            if waiting is True:
                n += 1
                time.sleep(5)

                if n >= 30:
                    print('Problem to init MySQL, abort.')
                    return False
        return True

class Repository:
    path = '/var/www/html/kaio/centos/7/os/x86_64/'

    # Build locally a rpm
    def build(self):
        pass

    # Send a rpm to "kaio" and update metadata for the repo
    def send(self, filepath):
        os.system('scp '+filepath+' root@kaio:'+Repository.path)
        os.system('ssh root@kaio "cd '+Repository.path+' && /usr/bin/createrepo . --update"')

        return True

if __name__ == '__main__':
    module = sys.argv[1]
    operation = sys.argv[2]
    result = False

    if module == 'mysql':
        container_name = sys.argv[3]
        password = sys.argv[4]

        mysql = MySQL()
        if operation == 'is-started':
            result = mysql.is_started(container_name=container_name, password=password)
    elif module == 'build':
        operation = sys.argv[3]

        repository = Repository()
        if operation == 'send':
            result = repository.send(sys.argv[4])

    if result is False:
        exit(1)
    exit(0)