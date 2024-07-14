# Rapid WG

This is a tool to rapidly deploy a new wg server on mostly any VPS using a CENT OS.
Currently tested with CENT OS 9

## Instructions

These instructions imply that you already have a VPS instance accessible by a root user with some kind of RSA key.

1. After cloning the repo, you need to create an `inventory` file that contains an IP-address of your VPN server:
    ```config
    [wireguard]
    167.67.67.10
    ```
2. The other file that you will need is the `group_vars/all` file. It contains some variables needed to create a user
    that will be responsible for the further configuration of the server while the `root` connection will be blocked
    for security reasons:
    ```yaml
    ansible_connection: ssh
    ansible_user: wgadmin
    ansible_private_key_file: ~/.ssh/id_rsa
    ansible_public_key_file: ~/.ssh/id_rsa.pub
    ```
3. Remember that the files `inventory` and `group_vars/all` only have an introductory content
    and shouldn't be used without modification.
4. The next step would be to run the `make generate` to prepare the initial set of users
    and some initial configuration for the wireguard server.
5. After performing the steps `1.-4.`, we should be now ready to start provisioning the server.
    Do it by running `make setup`.
6. If everything went fine, you should now be able to connect to the server.
7. Get the list of VPN users by runing the `make list` command.
