#!/bin/bash

chmod 600 keys/key.pem; 

. ./openrc.sh; ansible-playbook deploy_worker2.yaml -i inventory/host.ini --ask-become-pass