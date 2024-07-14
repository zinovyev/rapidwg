define HELP_BODY
rapidwg is a tool for rapidly provision you private wireguard server and generate client configurations.

For example, it can be used with a VPS instance running an CENTOS9 OS. Currently tested with DigitalOcean.

It uses Ansible and some Python scripting underneath, so you should have both installed on your host machine.

Usage:
	make help - print out this info
	make setup - perform the initial provisioning of the server
	make provision - update all the required packages and restart the processes
	make list - list existing users/clients of the wireguard server
	(not implemented) make add WG_USER=foo - add a new wireguard user where "foo" is the name of the user
	(not implemented) make delete WG_USER=foo - delete a wireguard user called "foo"
endef

export HELP_BODY

.SILENT: help
all: help
help:
	echo -e "$${HELP_BODY}"

generate:
	echo "Generating configuration file..."
	python ./scripts/generate_vars.py

setup: _setup
_setup:
	echo "Setting up the environment..."
	ansible-playbook ./plays/00_pre_init.yml
	ansible-playbook ./plays/01_init.yml

provision:
	ansible-playbook ./plays/02_wireguard.yml

list:
	echo "Existing users are: ..."

add: _add provision
_add:
	echo "Adding new user $(WG_USER)"
create: add
new: add

delete: _delete provision
_delete:
	echo "Deleting a user $(WG_USER)"
remove: delete
