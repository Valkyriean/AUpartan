#!/bin/bash

. ./openrc.sh; ansible-playbook instance_setup.yaml --ask-become-pass