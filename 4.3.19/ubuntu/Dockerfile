FROM imiobe/base:py2-ubuntu-18.04 as builder

ENV PIP=9.0.3 \
    ZC_BUILDOUT=2.13.1 \
    SETUPTOOLS=40.8.0 \
    PLONE_MAJOR=4.3 \
    PLONE_VERSION=4.3.19 \
    PLONE_MD5=04ed5beac7fb8504f06a36d44e407b06

LABEL plone=$PLONE_VERSION \
    name="Plone 4.3" \
    description="Plone image, based on Unified Installer" \
    maintainer="iMio"

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
COPY buildout.cfg /plone
WORKDIR /plone
RUN apt-get update \
  && buildDeps="python-pip build-essential libpq-dev libreadline-dev wget git gcc libc6-dev libpcre3-dev libssl-dev libxml2-dev libxslt1-dev libbz2-dev libffi-dev libjpeg62-dev libopenjp2-7-dev zlib1g-dev libwebp-dev python-dev" \
  && apt-get install -y --no-install-recommends $buildDeps \
  && wget -nv -O Plone.tgz https://launchpad.net/plone/$PLONE_MAJOR/$PLONE_VERSION/+download/Plone-$PLONE_VERSION-UnifiedInstaller.tgz \
  && echo "$PLONE_MD5 Plone.tgz" | md5sum -c - \
  && tar -xzf Plone.tgz \
  && tar -xf Plone-$PLONE_VERSION-UnifiedInstaller/packages/buildout-cache.tar.bz2 \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && mv buildout-cache/eggs . \
  && mv buildout-cache/downloads . \
  && pip install pip==$PIP setuptools==$SETUPTOOLS zc.buildout==$ZC_BUILDOUT \
  && su -c "buildout -t 30 -N" -s /bin/sh imio

FROM imiobe/base:py2-ubuntu-16.04
ENV PIP=9.0.3 \
  ZC_BUILDOUT=2.11.3 \
  SETUPTOOLS=38.7.0

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
RUN chown imio:imio -R /plone \
  && chown imio:imio -R /data

WORKDIR /plone

COPY --chown=imio --from=builder /plone/eggs eggs
COPY --from=builder /usr/local/lib/python2.7/dist-packages /usr/local/lib/python2.7/dist-packages
RUN find /data -not -user imio -exec chown imio:imio {} \+ \
 && find /plone -not -user imio -exec chown imio:imio {} \+  \
