FROM imiobe/base:py2-debian-buster as builder

ENV PIP=20.2.2 \
    PLONE_VERSION=4.3.20 \
    ZC_BUILDOUT=2.13.1 \
    SETUPTOOLS=40.8.0

LABEL plone=$PLONE_VERSION \
    name="Plone 4.3" \
    description="Plone image, based on Unified Installer" \
    maintainer="iMio"

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
COPY buildout.cfg versions-py2.cfg /plone/
WORKDIR /plone
RUN apt-get update \
  && buildDeps="build-essential \
                python2-dev \
                python-pip \
                poppler-utils \
                libpq-dev \
                libreadline-dev \
                wget \
                git \
                gcc \
                libc6-dev \
                libpcre3-dev \
                libssl-dev \
                libxml2-dev \
                libxslt1-dev \
                libbz2-dev \
                libffi-dev \
                libjpeg62-turbo-dev \
                libopenjp2-7-dev \
                zlib1g-dev \
                libwebp-dev \
                lbzip2" \
  && apt-get install -qqy --no-install-recommends $buildDeps \
  && sed -ie "s#versions-plone.cfg#https://dist.plone.org/release/$PLONE_VERSION/versions.cfg#" buildout.cfg \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && pip install pip==$PIP setuptools==$SETUPTOOLS zc.buildout==$ZC_BUILDOUT \
  && su -c "buildout -t 30 -N" -s /bin/bash imio

FROM imiobe/base:py2-debian-buster
ENV PIP=20.2.2
COPY --chown=imio --from=builder /plone/eggs /plone/eggs
COPY --from=builder /usr/local/lib/python2.7/dist-packages /usr/local/lib/python2.7/dist-packages
COPY --chown=imio count_users.py /plone/
WORKDIR /plone
RUN apt-get update \
  && apt-get install -qqy --no-install-recommends \
  python2 \
  libxml2 \
  libxslt1.1 \
  libpng16-16 \
  libjpeg62-turbo \
  libwebp6 \
  libopenjp2-7 \
  libtiff5 \
  poppler-utils \
 && mkdir -p /data /data/blobstorage /data/filestorage \
 && chown imio:imio -R /plone \
 && chown imio:imio -R /data \
 && find /data -not -user imio -exec chown imio:imio {} \+ \
 && find /plone -not -user imio -exec chown imio:imio {} \+