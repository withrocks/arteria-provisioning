# Build with
# docker build -t arteria/dependencies:versionnr .
# where . is the path of this Dockerfile.

FROM arteria/frozendata:1
LABEL Description="Some of the more static dependencies for the Arteria services" Version="0.1"

# Run everything as root for now
# USER

# Install all the dependencies
RUN yum groupinstall -y development

# Install newer version of Python; repo version is too old in centos
RUN yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel wget tar
WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz && tar xzf Python-2.7.10.tgz
WORKDIR /usr/src/Python-2.7.10
RUN ./configure && make altinstall
RUN wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz
RUN tar -xvf setuptools-1.4.2.tar.gz && cd setuptools-1.4.2 && python2.7 setup.py install
RUN curl https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python2.7 -
RUN pip install virtualenv

# Install supervisord; repo version in centos is too old
RUN pip install supervisor
COPY build_data/supervisord.conf /etc/supervisord.conf
COPY build_data/supervisord_init /etc/init.d/supervisord
RUN mkdir -p /etc/supervisor/conf.d && mkdir -p /var/log/supervisor
RUN chmod +x /etc/init.d/supervisord && chkconfig --add supervisord

# Some various things good to have
RUN yum install -y screen sudo which  

# Start the supervisord for the sake of our children
#CMD ["supervisord", "-c", "/etc/supervisor.conf"]
CMD service supervisord start
ONBUILD RUN service supervisord start
