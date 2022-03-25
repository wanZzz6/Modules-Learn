```dockerfile
...

ENV PYTHON_VERSION 3.8.3
ENV PYTHON_PREFIX /usr/local/python3

RUN apt-get install -y --no-install-recommends build-essential zlib1g-dev libbz2-1.0 libssl-dev libncurses5-dev \
    libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb5.3 libpcap-dev xz-utils libexpat1-dev liblzma-dev\
    libssl-dev openssl libffi-dev libc6-dev vim && \
    wget -O python.tgz https://cdn.npm.taobao.org/dist/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    mkdir ${PYTHON_PREFIX} && \
    tar -xzf python.tgz --directory ${PYTHON_PREFIX} && \
    rm python.tgz

RUN cd /usr/local/python3/Python-${PYTHON_VERSION} && \
    ./configure --enable-shared --prefix=${PYTHON_PREFIX} --enable-optimizations && make -j8 && make altinstall && \
    cp ${PYTHON_PREFIX}/lib/lib* /usr/lib && ldconfig &&\
    ln -s ${PYTHON_PREFIX}/bin/python${PYTHON_VERSION:0:3} /usr/bin/python3 && \
    ln -s ${PYTHON_PREFIX}/bin/pip${PYTHON_VERSION:0:3} /usr/bin/pip3
    
...
```





```dockerfile
...

RUN yum install -y wget aclocal automake autoconf make gcc gcc-c++ python-devel mysql-devel bzip2 libffi-devel epel-release

# install python 3.7.0
RUN wget https://npm.taobao.org/mirrors/python/3.7.0/Python-3.7.0.tar.xz \
&& tar -xvf Python-3.7.0.tar.xz -C /usr/local/ \
&& rm -rf Python-3.7.0.tar.xz \
&& cd /usr/local/Python-3.7.0 \
&& ./configure && make && make install

# install related packages
RUN yum install -y python-pip \
&& yum install -y python-setuptools \
&& pip3 install --upgrade pip -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com \

...
```

