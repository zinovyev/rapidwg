import os
import jinja2
import random
import ipaddress

def generate_custom_ipv4():
    return "10." + ".".join(str(random.randint(0, 255)) for _ in range(2)) + ".0"

def generate_custom_ipv6():
    return "fc00:" + ":".join(f"{random.randint(0, 0xFFFF):04x}" for _ in range(2)) + "::0"

def generate_key_paar():
    command = 'wg genkey | tee privatekey1 | wg pubkey > publickey1 ; ' \
            'echo -e "$(cat privatekey1)\n$(cat publickey1)" ; ' \
            'rm privatekey1 ; rm publickey1'
    return os.popen(command).read().split("\n")

def ip_next(custom_ip, offset):
    return ipaddress.ip_address(custom_ip) + offset

custom_ipv4 = generate_custom_ipv4()
custom_ipv6 = generate_custom_ipv6()
custom_port = random.randint(49500, 65500)

environment = jinja2.Environment()

# Generate "all" config
#

config_all = '''
ansible_connection: ssh
ansible_user: {{ ssh_user }}
ansible_private_key_file: {{ ssh_private_key }}
ansible_public_key_file: {{ ssh_public_key }}
'''

template = environment.from_string(config_all)
template.stream(ssh_user="wgadmin", ssh_private_key="~/.ssh/id_rsa", ssh_public_key="~/.ssh/id_rsa.pub").dump("./group_vars/all")

# Generate "wireguard" config
#

keys = [generate_key_paar() for _ in range(3)]
ip_addresses4 = [ip_next(custom_ipv4, i) for i in range(4)]
ip_addresses6 = [ip_next(custom_ipv6, i) for i in range(4)]

config_wireguard = '''
wireguard_network:
  ip_address: "{{ ipv4[0] }}"
  ip6_address: "{{ ipv6[0] }}"

wireguard_server:
  port: {{ port }}
  ip_address: "{{ ipv4[1] }}"
  ip6_address: "{{ ipv6[1] }}"
  private_key: "{{ keys[0][0] }}"
  public_key: "{{ keys[0][1] }}"

wireguard_clients:
  - name: John
    ip_address: "{{ ipv4[2] }}"
    ip6_address: "{{ ipv6[2] }}"
    private_key: "{{ keys[1][0] }}"
    public_key: "{{ keys[1][1] }}"

  - name: Smith
    ip_address: "{{ ipv4[3] }}"
    ip6_address: "{{ ipv6[3] }}"
    private_key: "{{ keys[2][0] }}"
    public_key: "{{ keys[2][1] }}"
'''

template = environment.from_string(config_wireguard)
template.stream(ipv4 = ip_addresses4, ipv6 = ip_addresses6, port = custom_port, keys = keys).dump("./group_vars/wireguard")
