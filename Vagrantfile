# -*- mode: ruby -*-
# vi: set ft=ruby :

# TODO Add necessary minimum provisioning for testarteria
$script = <<EOF
mkdir -pv /data/testarteria1
mkdir /data/testarteria1/mon1
mkdir /data/testarteria1/mon2
mkdir -pv /srv/samplesheet/processning/
chown -R vagrant:vagrant /data
chown -R vagrant:vagrant /srv/samplesheet
chmod -R g+w /data
mkdir -pv /data/scratch

mkdir -pv /var/log/arteria/

yum groupinstall -y development

# Install newer version of Python; repo version is too old in centos
yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel wget tar
pushd /usr/src
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz && tar xzf Python-2.7.10.tgz
popd

pushd /usr/src/Python-2.7.10
./configure && make --quiet altinstall

# Python 2.7 is installed under /usr/local/bin
echo "PATH=/usr/local/bin:$PATH" > ~/.bashrc
source ~/.bashrc

wget -q --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz
tar -xvf setuptools-1.4.2.tar.gz && cd setuptools-1.4.2 && python2.7 setup.py install
curl -q https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python2.7 -
popd

echo "Installing main python requirements (in no virtualenv)"
yum update
pip2.7 install virtualenv

echo "Installing supervisor"
# Install supervisord; repo version in centos is too old
pip2.7 install supervisor
mkdir -p /etc/supervisor/conf.d && mkdir -p /var/log/supervisor
chmod +x /etc/init.d/supervisord && chkconfig --add supervisord
service supervisord start

echo "Install bcl2fastq"
yum install -y http://support.illumina.com/content/dam/illumina-support/documents/downloads/software/bcl2fastq/bcl2fastq2-v2.17.1.14-Linux-x86_64.rpm

echo "Install services"
source_path=/arteria/arteria-lib
product=runfolder
pushd /arteria/arteria-provisioning/services
./install-service $product vagrant vagrant dev $source_path/$product $source_path/arteria /opt/$product
popd

sudo /etc/init.d/iptables stop

EOF

Vagrant.configure(2) do |config|

  # Ensure that the VMs can reach each other
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.ignore_private_ip = false

  # Configure the stackstorm master node
  config.vm.define "stackstorm-master" do |stackstorm|

    stackstorm.vm.box = "ubuntu/trusty64"

    stackstorm.vm.hostname = "stackstorm-master"
    stackstorm.vm.network :private_network, ip: '192.168.42.42'

    stackstorm.vm.synced_folder "../arteria-packs/", "/opt/stackstorm/packs/arteria-packs"
    stackstorm.vm.synced_folder "../arteria-packs/", "/arteria/arteria-packs"
    stackstorm.vm.synced_folder "../arteria-core/", "/arteria/arteria-core"
    stackstorm.vm.synced_folder "../arteria-bcl2fastq/", "/arteria/arteria-bcl2fastq"
    stackstorm.vm.synced_folder "../arteria-siswrap/", "/arteria/arteria-siswrap"
    stackstorm.vm.synced_folder "../arteria-runfolder/", "/arteria/arteria-runfolder"
    stackstorm.vm.synced_folder "../arteria-provisioning/", "/arteria/arteria-provisioning"

    # Forwarding these ports is required for the webui to work
    stackstorm.vm.network :forwarded_port, host: 8080, guest: 8080
    stackstorm.vm.network :forwarded_port, host: 9100, guest: 9100
    stackstorm.vm.network :forwarded_port, host: 9101, guest: 9101

    stackstorm.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 2
      v.customize ["modifyvm", :id, "--ioapic", "on"]
    end

    stackstorm.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible-st2/playbooks/arteriaexpress.yaml"
      ansible.inventory_path = "ansible-st2/inventories/test_inventory"
    end

  end

  # Configure the biotank stand-in
  config.vm.define "testarteria1" do |testtank|

    testtank.vm.box = "puppetlabs/centos-6.6-64-puppet"

    testtank.vm.provider "virtualbox" do |v|
      v.memory = 8000
      v.cpus = 4
      v.customize ["modifyvm", :id, "--ioapic", "on"]
    end

    testtank.vm.hostname = "testarteria1"
    testtank.vm.network :private_network, ip: '192.168.42.43'

    testtank.vm.synced_folder "../arteria-packs/", "/arteria/arteria-packs"
    testtank.vm.synced_folder "../arteria-core/", "/arteria/arteria-core"
    testtank.vm.synced_folder "../arteria-bcl2fastq/", "/arteria/arteria-bcl2fastq"
    testtank.vm.synced_folder "../arteria-siswrap/", "/arteria/arteria-siswrap"
    testtank.vm.synced_folder "../arteria-runfolder/", "/arteria/arteria-runfolder"
    testtank.vm.synced_folder "../arteria-provisioning/", "/arteria/arteria-provisioning"
    #testtank.vm.synced_folder "/data/arteria_test_data/", "/data/testarteria1/mon1/"

    testtank.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible-st2/playbooks/arteriaexpress.yaml"
      ansible.inventory_path = "ansible-st2/inventories/test_inventory"
    end

  end

  # Deploy ssh keys to all host to ensure they have the
  # password less ssh-access to each other.

  vagrant_ssh = "/home/vagrant/.ssh"

  config.vm.provision "file",
    source: "private_key",
    destination: vagrant_ssh + "/key"

  config.vm.provision "file",
    source: "ssh_config",
    destination: vagrant_ssh + "/config"

  config.vm.provision "shell", inline: "ssh-keygen -y -f #{vagrant_ssh}/key > #{vagrant_ssh}/key.pub"
  config.vm.provision "shell", inline: "cat #{vagrant_ssh}/key.pub >> #{vagrant_ssh}/authorized_keys"

end
