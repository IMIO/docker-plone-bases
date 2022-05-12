FROM imiobe/base:py2-ubuntu-22.04 as builder

ENV PIP=20.3.4 \
    PLONE_VERSION=4.3.20 \
    ZC_BUILDOUT=2.13.3 \
    SETUPTOOLS=44.1.1

LABEL plone=$PLONE_VERSION \
    name="Plone 4.3" \
    description="Plone image, based on Unified Installer" \
    maintainer="iMio"

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
COPY buildout.cfg versions-py2.cfg /plone/
WORKDIR /plone
RUN apt-get update -qqy \
  && buildDeps="build-essential \
        python2-dev \
        python3-pip \
        wget \
        git \
        gcc \
        libpq-dev \
        libreadline-dev \
        libc6-dev \
        libpcre3-dev \
        libssl-dev \
        libssl-dev \
        libxml2-dev \
        libxslt1-dev \
        libbz2-dev \
        zlib1g-dev \
        libffi-dev \
        libjpeg62-dev \
        libopenjp2-7-dev \
        libwebp-dev \
        libgif-dev \
        libwebp-dev" \
  && apt-get install -qqy --no-install-recommends $buildDeps \
  && rm -rf /var/lib/apt/lists/* \
  && sed -ie "s#versions-plone.cfg#https://dist.plone.org/release/$PLONE_VERSION/versions.cfg#" buildout.cfg \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && pip install "virtualenv>=20.7.2" \
  && su -c "virtualenv -p python2 ." -s /bin/sh imio \
  && su -c "bin/pip install pip==$PIP setuptools==$SETUPTOOLS zc.buildout==$ZC_BUILDOUT" -s /bin/sh imio \
  && su -c "bin/buildout -t 30 -N" -s /bin/sh imio

FROM imiobe/base:py2-ubuntu-22.04
ENV PIP=20.3.4
COPY --chown=imio --from=builder /plone/eggs /plone/eggs
COPY --from=builder /usr/local/lib/python2.7/dist-packages /usr/local/lib/python2.7/dist-packages
COPY --chown=imio count_users.py /plone/
WORKDIR /plone
RUN apt-get update \
  && apt-get install -qqy --no-install-recommends \
  libxml2 \
  libxslt1.1 \
  libpng16-16 \
  libjpeg62 \
  libwebp7 \
  libopenjp2-7 \
  libtiff5 \
  libgif7 \
  librsvg2-bin \
  poppler-utils \
 && mkdir -p /data /data/blobstorage /data/filestorage \
 && chown imio:imio -R /plone \
 && chown imio:imio -R /data \
 && find /data -not -user imio -exec chown imio:imio {} \+ \
 && find /plone -not -user imio -exec chown imio:imio {} \+
