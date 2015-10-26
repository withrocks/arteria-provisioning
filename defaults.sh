#!/bin/bash

ansible-playbook -i ./ansible-st2/inventories/test_inventory -l testarteria1 --check ./ansible-st2/playbooks/arteriaexpress.yaml | grep msg

