Arteria-provisioning
--------------------

Note that this is not yet production ready, and should only be used for development purposes at the moment.

Running `vagrant up` will produce a virtual machine which runs StackStorm, including the WebUI, listening on `localhost:8080`.

Login with `user=testu password=testp`.

The playbooks here are forked from: https://github.com/StackStorm/ansible-st2. In the future we'll probably move to running the StackStorm services in Docker containers, and at that point this will change a lot, but for now this is a working solution.
