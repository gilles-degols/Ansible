### Requirements:
Deployment machine: Centos 7, 512MB of RAM, 10GB of disk, 1 vCPU. 

Any host: Centos 7. 
 
Docker: Centos 7.

Note that every machine runs on VirtualBox in those scripts, to reduce the cost to test the deployment on multiple servers.
You only need to adapt the hosts/ directory and the VM setup described here to be able to run the script on any machine.

The goal in the current scripts is to try to only use Docker images for each role.

### Ansible installation on your "Deployment" machine
1. Install ansible
``` 
    yum clean all && yum -y update
    yum install -y epel-release 
    yum install -y ansible
```

2. Generate a ssh key locally (called "cluster", without passphrase)
``ssh-keygen -t rsa -b 4096 ``

3. Set the path to the ssh key in the different files in the "hosts" directory from this project

### Oracle VM VirtualBox
Do not forget to enable a local DHCP to be sure that your VMs do not take new IPs.
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

Before installing Centos 7 on your VM, do not forget to add the "Host Only" Adapter in the VM Settings, otherwise
the ifcfg-enp0s8 used below will not exist.

### Manual installation off a "clean host"

0. Install Centos 7 iso, with partitioned /home, /var, /tmp and /. Values in parenthesis are for small deployment.
 - 30GB (5GB) for /, 
 - 20GB (5GB) for /home, 
 - 5GB (1GB) for /tmp,
 - 5GB (1GB) for /swap
 - and the remaining in /var should be enough.

1. On a Centos 7 running in VirtualBox, you need to adapt network configuration to set a specific ip address
    https://gist.github.com/fernandoaleman/2172388
    - Activate your "Host-Only Adapter" in the VM Settings
    - Now you need to update the appropriate network configuration, here we will set up the ip ```192.168.56.121```
    you normally only need to set the appropriate value for "BOOTPROTO", "ONBOOT", "IPADDR", "NETMASK".
    ```
    [root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
    TYPE=Ethernet
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
    IPADDR=192.168.56.121
    NETMASK=255.255.255.0
    ```
    - Then you need to restart the network on the VM to take the ip address.
    ```systemctl restart network```
    - Verify if the ip address was correctly set up:
    ```ip a```
    - Then go on another machine, and ping the ip ad:
    ```ping 192.168.56.121```
    - If you see the ip address on the VM, and not outside of it. verify your VirtualBox configuration. Verify also that you activated the "Host-Only Adapter" on your VM Settings.
    - Try to connect to the internet (for now, all the nodes need an internet connection)
    ```ping 8.8.8.8```
    If you cannot access to the internet, you might need to update ```/etc/sysconfig/network-scripts/ifcfg-enp0s3```
    and set up "ONBOOT=yes". To directly test the configuration change, run ```systemctl restart network``` 
    
2. Add the ip to "hosts/deployer", in the section "all"

    ``` 192.168.56.101 hostname=node1```   

3. Add your local ssh key to access the server

    ``` ssh-copy-id -i /root/.ssh/cluster.pub root@192.168.56.101 ```

4. If not done previously, for the first installation, you need to allow the connection from the deployment to the deployment machine itself

    ``` ssh-copy-id -i /root/.ssh/cluster.pub root@127.0.0.1 ```

4. Add the "deployer" user first, it also uploads the public key. Use the correct private-key or password for this first
login. Afterwards the "deployer" users will all have the same public/private key

```ansible-playbook -i hosts/deployer -b roles/deployer.yml```

### List of available roles

##### Before any role
ansible-playbook -i hosts/deployer -s roles/deployer.yml

##### Before any role, as network can change for every cluster
ansible-playbook -i hosts/cluster -s roles/network.yml

##### Install repository (kaio server)
ansible-playbook -i hosts/repository -s roles/repository.yml

##### Install jenkins (kaio server)
ansible-playbook -i hosts/jenkins -s roles/jenkins.yml

##### Install kafka
ansible-playbook -i hosts/cluster -s roles/kafka.yml

### Other
1. Ping all machines:
  ```ansible all -i hosts/cluster -m ping```
