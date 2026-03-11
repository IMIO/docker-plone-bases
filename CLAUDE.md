# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository builds and publishes base Docker images for Plone CMS to the iMio Harbor registry (`harbor.imio.be/common/plone-base`). Each Plone version has its own subdirectory with a Dockerfile and buildout config.

## Building Images Locally

```bash
# Build a specific version (context path must point to the directory containing buildout.cfg)
docker build -f 6.1/6.1.4/ubuntu/Dockerfile -t common/plone-base:6.1.4 6.1/6.1.4/ubuntu/

# Build legacy Python 2 image
docker build -f 4.3.20/ubuntu/py2/Dockerfile -t common/plone-base:4.3.20-ubuntu 4.3.20/ubuntu/py2/
```

There is no Makefile or test suite. Validation is done by successfully building the Docker image.

## Adding a New Plone Version

1. Create directory `<major>/<version>/ubuntu/`
2. Add `Dockerfile` — copy from the nearest existing version, update `PLONE_VERSION` and any pinned tool versions (`ZC_BUILDOUT`, `SETUPTOOLS`, `PIP`, `WHEEL`)
3. Add `buildout.cfg` — copy from another version in the same series (6.0.x or 6.1.x), it's minimal
4. Add the new entry to `.github/workflows/build-push-notify.yml` in the `matrix.include` list

## Architecture

**Multi-stage Dockerfiles** (all except 4.3.20):
- **Stage 1 (builder)**: Installs build tools, downloads Plone release config from `https://dist.plone.org/release/<version>/`, runs `zc.buildout` to compile Python eggs
- **Stage 2 (runtime)**: Copies only `requirements.txt` and `eggs/` from builder, installs minimal runtime libs, creates `/data/{blobstorage,filestorage}` dirs

**Parent images** come from `harbor.imio.be/common/base:py3-ubuntu-24.04` (or `py2-ubuntu-22.04` for 4.3.20). These are maintained in [IMIO/docker-bases](https://github.com/IMIO/docker-bases).

**Version layout**:
- `4.3.20/ubuntu/py2/` — Python 2, Ubuntu 22.04 (legacy)
- `6.0/6.0.x/ubuntu/` — Python 3, Ubuntu 24.04
- `6.1/6.1.x/ubuntu/` — Python 3, Ubuntu 24.04 (current series)

## CI/CD

`.github/workflows/build-push-notify.yml` triggers on push to `master`, manual dispatch, and weekly (Sundays 03:00 UTC). It builds all versions in parallel using the `IMIO/gha/build-push-notify@v3.2` action and pushes to Harbor. Required secrets: `HARBOR_URL`, `COMMON_HARBOR_USERNAME`, `COMMON_HARBOR_PASSWORD`, `COMMON_MATTERMOST_WEBHOOK_URL`.
