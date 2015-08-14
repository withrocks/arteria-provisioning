Idea is to have one base image for the test data, that shouldn't change often.  It inherits from the official centos image. At the moment the image is filled with around 15 GB of test data. (Not checked into the repo though; should be added under e.g. frozen-data/build_data/testarteria1/mon1/)

This data image is then the base for a dependency image that setups supervisord, pulls in a bunch of general development packages, and then installs a newer Python version.

Last we have a monolithic service image that inherits from the dependency image. Here we mainly pull in specific dependencies for e.g. Sisyphus and bcl2fastq, expose a couple of TCP ports, and then populate the image with an install script that can be used for running the various services own installation scripts, when we have a service container up and running.

Launching a new service container can be done manually or with the run script. The user will have to manually mount the local host's source code trees so that the container can reach them for installation/testing/running.

Note that build times are considerably longer from a clean slate. Generally when you're rebuilding multiple times the build time will be shorter because Docker will be able to re-use earlier steps that are in the cache. Therefore it is important to try to do as much as possible of all the future changes as "far down in the inheritance and build chain" as possible.

I.e. it is expected that the data image will be more or less frozen and stable, whereas the service image will be more volatile, and the dependency image somewhere in between. New additions to the service image should by the same reasons preferably be done in the lower end of the Dockerfile as well.

The launch of a service container is more or less instant, but when the user wants to start from scratch with a clean setup then the container has to be removed with "docker rm <container>", and this seems to take around up to a couple of minutes on our machines depending on load.

If the developer wants to create a smaller image for just his service then that can easily be done with their own Dockerfile that inherits from either frozendata or dependencies.  
