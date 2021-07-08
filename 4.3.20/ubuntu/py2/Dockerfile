FROM imiobe/base:py2-ubuntu-20.04 as builder

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
RUN apt-get update -qqy \
  && buildDeps="build-essential \
        wget \
        git \
        gcc \
        python2-dev \
        virtualenv \
        libpq-dev \
        libreadline-dev \
        libc6-dev \
        libpcre3-dev \
        libssl1.1 \
        libssl-dev \
        libxml2-dev \
        libxslt1-dev \
        libbz2-dev \
        libffi-dev \
        libjpeg62-dev \
        libopenjp2-7-dev \
        zlib1g-dev \
        libwebp-dev" \
  && apt-get install -qqy --no-install-recommends $buildDeps \
  && rm -rf /var/lib/apt/lists/* \
  && sed -ie "s#versions-plone.cfg#https://dist.plone.org/release/$PLONE_VERSION/versions.cfg#" buildout.cfg \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && su -c "virtualenv -p python2 ." -s /bin/sh imio \
  && su -c "bin/pip install pip==$PIP setuptools==$SETUPTOOLS zc.buildout==$ZC_BUILDOUT" -s /bin/sh imio \
  && su -c "bin/buildout -t 30 -N" -s /bin/sh imio

FROM imiobe/base:py2-ubuntu-20.04
ENV PIP=20.2.2
COPY --chown=imio --from=builder /plone/eggs /plone/eggs
COPY --from=builder /usr/local/lib/python2.7/dist-packages /usr/local/lib/python2.7/dist-packages
WORKDIR /plone
RUN apt-get update \
  && apt-get install -qqy --no-install-recommends \
  python2 \
  libxml2 \
  libxslt1.1 \
  libpng16-16 \
  libjpeg62 \
  libwebp6 \
  libopenjp2-7 \
  libtiff5 \
  poppler-utils \
 && mkdir -p /data /data/blobstorage /data/filestorage \
 && chown imio:imio -R /plone \
 && chown imio:imio -R /data \
 && find /data -not -user imio -exec chown imio:imio {} \+ \
 && find /plone -not -user imio -exec chown imio:imio {} \+
