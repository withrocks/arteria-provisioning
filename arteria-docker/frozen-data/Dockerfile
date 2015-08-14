# Build with
# docker build -t arteria/frozendata:versionnr .
# where . is the path of this Dockerfile.

FROM centos:6
LABEL Description="NGS test data image to be used by Arteria service containers" Version="0.1"

RUN mkdir /data/
COPY build_data/ /data/

RUN yum update -y
RUN yum install -y epel-release

# We're lazy right now and using root instead of normal user
# RUN chown -R vagrant:vagrant /data/
CMD echo "data layer container"
