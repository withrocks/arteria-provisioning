# Idea is to have general dependencies from parent image and specific
# dependencies here. Then for testing we install the software via
# running the container instead on the host mounted drives.

FROM arteria/dependencies:1
LABEL Description="Monolithic test image for all Arteria services" Version="0.1"

# We might want to do this in a layer higher up; or add it
RUN mkdir -pv /srv/samplesheet/processing/ && mkdir /var/log/arteria && mkdir /opt/runfolder
RUN touch /var/log/arteria/runfolder.log

# bcl2fast service dependency
RUN yum install -y http://support.illumina.com/content/dam/illumina-support/documents/downloads/software/bcl2fastq/bcl2fastq2-v2.17.1.14-Linux-x86_64.rpm

# siswrap service dependencies
RUN yum install -y dos2unix gnuplot PyXML ImageMagick libxslt-devel libxml2-devel libxml2-devel ncurses-devel libtiff-devel bzip2-devel zlib2-devel perl-XML-LibXML perl-XML-LibXML-Common perl-XML-NamespaceSupport perl-XML-SAX perl-XML-Simple zlib-devel perl-Archive-Zip perl-CPAN git perl-PDL perl-PerlIO-gzip

# Deploy SSH keys
#COPY

#ENV ARTERIA_TEST=1

# We need to open up the ports that the container needs to expose
# We don't really need to do this here though, it is mostly for linking
# containers, or when we want to map them with -P, but we want to use
# -p to get specific mappings at run time for the container.
EXPOSE 8888
EXPOSE 10900
EXPOSE 10800

# Insert an install script that makes it somewhat easier to install the
# services on the running container. We presume that
# /arteria/arteria-{lib,packs,provisioning} have been mounted from the host
COPY build_data/install_services /root/install_services

# Start the serviced that takes care of our processes
CMD service supervisord start
