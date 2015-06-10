# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "private_network", ip: "172.28.128.121"

  config.vm.synced_folder "../arteria-packs/", "/opt/stackstorm/packs/arteria-packs"

  # Forwarding these ports is required for the webui to work
  config.vm.network :forwarded_port, host: 8080, guest: 8080
  config.vm.network :forwarded_port, host: 9100, guest: 9100
  config.vm.network :forwarded_port, host: 9101, guest: 9101
  
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible-st2/playbooks/arteriaexpress.yaml"
    ansible.sudo = true
  end
end


