#!/bin/bash
chmod 600 keys/key.pem; 

. ./openrc.sh; ansible-playbook instance_setup.yaml -i inventory/host.ini --ask-become-pass
