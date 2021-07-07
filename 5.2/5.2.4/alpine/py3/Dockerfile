FROM imiobe/base:py3-alpine as builder

ENV PIP=21.1.3 \
    PLONE_VERSION=5.2.4

LABEL plone=$PLONE_VERSION \
    name="Plone 5.2.4" \
    description="Plone image, based on Unified Installer" \
    maintainer="iMio"

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
COPY buildout.cfg /plone
WORKDIR /plone
RUN buildDeps="build-base wget git gcc libc-dev zlib-dev libjpeg-turbo-dev libpng-dev libxml2-dev libxslt-dev pcre-dev libffi-dev postgresql-dev pcre-dev libbz2 openjpeg-dev libwebp-dev bzip2-dev" \
  && apk add --no-cache --virtual $buildDeps \
  && wget -nv https://dist.plone.org/release/$PLONE_VERSION/requirements.txt \
  && wget -nv https://dist.plone.org/release/$PLONE_VERSION/versions.cfg \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && pip install pip==$PIP -r requirements.txt \
  && su -c "buildout -t 30 -N" -s /bin/sh imio

FROM imiobe/base:py3-alpine

RUN mkdir -p /plone /data /data/blobstorage /data/filestorage
RUN chown imio:imio -R /plone \
  && chown imio:imio -R /data

WORKDIR /plone

COPY --chown=imio --from=builder /plone/eggs eggs
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
RUN find /data -not -user imio -exec chown imio:imio {} \+ \
 && find /plone -not -user imio -exec chown imio:imio {} \+  \
