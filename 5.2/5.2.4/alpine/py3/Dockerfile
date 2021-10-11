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
  && echo "pip==$PIP" | cat - requirements.txt >> tmp.txt \
  && mv tmp.txt requirements.txt \
  && wget -nv https://dist.plone.org/release/$PLONE_VERSION/versions.cfg \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && pip install -r requirements.txt \
  && su -c "buildout -t 30 -N" -s /bin/sh imio

FROM imiobe/base:py3-alpine
COPY --chown=imio --from=builder /plone/requirements.txt /plone/
COPY --chown=imio --from=builder /plone/eggs /plone/eggs
COPY --chown=imio count_users.py /plone/
WORKDIR /plone
RUN apk add --no-cache --virtual .run-deps \
  bash \
  rsync \
  libxml2 \
  libxslt \
  libpng \
  libjpeg-turbo\
  libwebp \
  openjpeg \
  && pip install -r requirements.txt \
  && mkdir -p /data /data/blobstorage /data/filestorage \
  && chown imio:imio -R /plone \
  && chown imio:imio -R /data \
  && find /data -not -user imio -exec chown imio:imio {} \+ \
  && find /plone -not -user imio -exec chown imio:imio {} \+