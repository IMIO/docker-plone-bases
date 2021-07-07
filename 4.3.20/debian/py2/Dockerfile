FROM imiobe/base:py2-debian-buster as builder

ENV PIP=20.2.2 \
    PLONE_VERSION=4.3.20

LABEL plone=$PLONE_VERSION \
    name="Plone 4.3" \
    description="Plone image, based on Unified Installer" \
    maintainer="iMio"

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
COPY buildout.cfg /plone
WORKDIR /plone
RUN apt-get update \
  && buildDeps="python-pip libpq-dev libreadline-dev wget git gcc libc6-dev libpcre3-dev libssl-dev libxml2-dev libxslt1-dev libbz2-dev libffi-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev libwebp-dev lbzip2" \
  && apt-get install -y --no-install-recommends $buildDeps \
  && wget -nv https://dist.plone.org/release/$PLONE_VERSION/requirements.txt \
  && wget -nv https://dist.plone.org/release/$PLONE_VERSION/versions.cfg \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && pip install pip==$PIP -r requirements.txt \
  && su -c "buildout -t 30 -N" -s /bin/sh imio

FROM imiobe/base:py2-debian-buster
ENV PIP=20.2.2

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
RUN chown imio:imio -R /plone \
  && chown imio:imio -R /data

WORKDIR /plone

COPY --chown=imio --from=builder /plone/eggs eggs
COPY --from=builder /usr/local/lib/python2.7/dist-packages /usr/local/lib/python2.7/dist-packages
RUN find /data -not -user imio -exec chown imio:imio {} \+ \
 && find /plone -not -user imio -exec chown imio:imio {} \+  \
