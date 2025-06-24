FROM harbor.imio.be/common/base:py3-ubuntu-24.04 AS builder

ENV ZC_BUILDOUT=3.3 \
  SETUPTOOLS=75.6.0 \
  PLONE_VERSION=6.0.14

LABEL plone=$PLONE_VERSION \
    name="Plone 6.0.14" \
    description="Plone image, based on Unified Installer" \
    maintainer="iMio"

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
COPY buildout.cfg /plone
WORKDIR /plone
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  gcc \
  git \
  libbz2-dev \
  libc6-dev \
  libffi-dev \
  libjpeg62-dev \
  libopenjp2-7-dev \
  libmemcached-dev \
  libpcre3-dev \
  libpq-dev \
  libreadline-dev \
  libssl-dev \
  libxml2-dev \
  libxslt1-dev \
  python3-dev \
  wget \
  zlib1g-dev

RUN pip3 install --no-cache-dir --break-system-packages setuptools==$SETUPTOOLS zc.buildout==$ZC_BUILDOUT py-spy \
  &&  wget -nv https://dist.plone.org/release/$PLONE_VERSION/requirements.txt \
  && wget -nv https://dist.plone.org/release/$PLONE_VERSION/versions.cfg \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && pip install --break-system-packages --ignore-installed -r requirements.txt \
  && su -c "buildout -t 30 -N" -s /bin/sh imio

FROM harbor.imio.be/common/base:py3-ubuntu-24.04
COPY --chown=imio --from=builder /plone/requirements.txt /plone/
COPY --chown=imio --from=builder /plone/eggs /plone/eggs
WORKDIR /plone
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
  libjpeg62 \
  libmemcached11 \
  libopenjp2-7 \
  libpq5 \
  libtiff6 \
  libxml2 \
  libxslt1.1 \
  lynx \
  netcat-openbsd \
  poppler-utils \
  rsync \
  wget \
  wv \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install --break-system-packages --ignore-installed -r requirements.txt \
  && mkdir -p /data /data/blobstorage /data/filestorage \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && find /data -not -user imio -exec chown imio:imio {} \+ \
  && find /plone -not -user imio -exec chown imio:imio {} \+ \
  && curl -L https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_amd64.deb > /tmp/dumb-init.deb && dpkg -i /tmp/dumb-init.deb && rm /tmp/dumb-init.deb
