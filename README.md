Arteria-provisioning
--------------------

Note that this is not yet production ready, and should only be used for development purposes at the moment.

*Getting started*

Install the hostmanager plugin for Vagrant:

    vagrant plugin install vagrant-hostmanager

This will manage the host files of the VMs and your hosting machine. Run `vagrant hostmanager` to update the hosts files.

Generate a ssh-key (without a password) that will be used to establish password less ssh between the hosts.

    ssh-keygen -f private_key

Running `vagrant up` will produce a virtual machine which runs StackStorm, including the WebUI, listening on `localhost:8080`.

Login with `user=testu password=testp`.

The playbooks here are forked from: https://github.com/StackStorm/ansible-st2. In the future we'll probably move to running the StackStorm services in Docker containers, and at that point this will change a lot, but for now this is a working solution.

You'll need the following repos:
  ./arteria-provisioning (this)
  ./arteria-packs
  ./arteria-lib

*The runfolder micro-service*

The runfolder package will be installed on testarteria1 and integration tests will run during provisioning. The service is running on port 10800 by default:
 * Browse to http://testarteria1:10800/api/1.0 for api help
 * Run integration tests:
   * From testarteria1: 
     - Change to the runfolder virtualenv with `source /opt/runfolder/bin/activate`
     - Run the tests with `runfolder-ws-test`
   * If you want to run it from your machine:
     - Install nose with `pip install nose`
     - Run `nosetests ./arteria-lib/runfolder/tests/integration`
