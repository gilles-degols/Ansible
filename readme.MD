# Requirements:
User system: ideally, on centos - cluster master.
Host: Centos 7.
Docker: Centos 7.

# Ansible installation on your "Master" machine
0. Install ansible
``` 
    yum clean all && yum update
    yum install -y epel-release 
    yum install -y ansible
```

1. Generate a ssh key locally (called "cluster", without passphrase)
``ssh-keygen -t rsa -b 4096 ``

2. Set the path to the ssh key in the different files in the "hosts" directory from this project

# Other
1. Ping all machines
  ansible all -i hosts/cluster -m ping

# Manual installation on each host

0. Install Centos 7 iso, with partitioned /home, /var, /tmp and /. Values in parenthesis are for small deployment.
 - 30GB (5GB) for /, 
 - 20GB (5GB) for /home, 
 - 5GB (1GB) for /tmp,
 - 5GB (1GB) for /swap
 - and the remaining in /var should be enough.

1. Set up a static ip for your Debian (local install only)
 - vi /etc/network/interfaces
   - Replace 
   ``` iface enp0s3 inet dhcp ```
   - By 
   ``` 
   auto enp0s3
   iface enp0s3 inet static 
     address 192.168.56.121 
     netmask 255.255.255.0
     gateway 192.168.56.100
    ```
    Where ``` address 192.168.56.121 ``` is the ip address.
 - Then
    ```service networking restart```
1. If Centos 
    https://gist.github.com/fernandoaleman/2172388
    ```
    [root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
    TYPE=Ethernet
    #BOOTPROTO=dhcp
    BOOTPROTO=static
    DEFROUTE=yes
    IPV4_FAILURE_FATAL=no
    IPV6INIT=yes
    IPV6_AUTOCONF=yes
    IPV6_DEFROUTE=yes
    IPV6_FAILURE_FATAL=no
    IPV6_ADDR_GEN_MODE=stable-privacy
    NAME=enp0s8
    UUID=617b7523-4277-40e4-941f-46086b24229a
    DEVICE=enp0s8
    ONBOOT=yes
    PEERDNS=yes
    PEERROUTES=yes
    IPV6_PEERDNS=yes
    IPV6_PEERROUTES=yes
    IPV6_PRIVACY=no
    NM_CONTROLLED=0
    IPADDR=192.168.56.150
    NETMASK=255.255.255.0
    ```
   
2. (On your "master" machine only) In Windows, add the new ip to /Windows/System32/drivers/etc/hosts. In Linux, add the ip to /etc/hosts

    ``` 192.168.56.101 node1 ```

3. Add the ip to "hosts/deployer", in the "all" section

    ``` 192.168.56.101 hostname=node1```   

4. Add your local ssh key to access the server

    ``` ssh-copy-id -i /root/.ssh/cluster root@node1 ```

5. Add the "deployer" user first, it also uploads the public key. Use the correct private-key or password for this first
login. Afterwards the "deployer" users will all have the same public/private key

```ansible-playbook -i hosts/deployer -b roles/deployer.yml```

If error to connect like the following (mostly with cygwin on windows):

``` {"changed": false, "msg": "Failed to connect to the host via ssh: mux_client_request_session: read from master failed: Connection reset by peer\r\nFailed to connect to new control master\r\n", "unreachable": true}```

Try multiple times, it seems there is a problem to connect with the internet connection, Ansible is probably not at fault

6. Run the first basic installation with ansible (common for all hosts), after adding the hosts to the corresponding inventory file

``` ansible-playbook -i hosts/cluster -s roles/common.yml ```

If you want to run a short update: 

```ansible-playbook -i hosts/cluster -s roles/common.yml --skip-tags slow ```

# Install Ansible on Windows (local machine)
- Do not use cygwin to run Ansible. It works sometimes, sometimes not.
- For each host: Add root user to the server
- For each host: Upload your ssh key
- For each host: Add the ip to the related groups in the "hosts" file. Or better, create a specific "host" file
- For each separated installation (if no cluster, host would only contain one line most of the time)

# Install docker
ansible-playbook -i hosts/dedistore -s roles/common.yml
ansible-playbook -i hosts/dedistore -s roles/docker.yml

# Install kafka
ansible-playbook -i hosts/cluster -s roles/common.yml
ansible-playbook -i hosts/cluster -s roles/kafka.yml

# Install repository (kaio server)
ansible-playbook -i hosts/repository -s roles/common.yml
ansible-playbook -i hosts/repository -s roles/repository.yml

# Install jenkins (kaio server)
ansible-playbook -i hosts/jenkins -s roles/common.yml
ansible-playbook -i hosts/jenkins -s roles/jenkins.yml

# Oracle VM VirtualBox
Do not forget to enable a local DHCP to be sure that your VM does not take new IPs.
 File > Preferences > Network > Host Only Network > VirtualBox Host-Only Ethernet Adapter (add or edit)
 In the left panel, set:
 - IPv4 at 192.168.56.1
 - IPv4 Network Mask at 255.255.255.0
 In the right panel:
 - Enable DHCP 
 - Server Address 192.168.56.100
 - Server Mask 255.255.255.0
 - Lower Address Bound 192.168.56.101
 - Upper Address Bound 192.168.56.254
 