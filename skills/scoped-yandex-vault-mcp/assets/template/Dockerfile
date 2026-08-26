# syntax=docker/dockerfile:1.7
FROM python:3.14.7-slim-bookworm@sha256:23c59390fc717bf09f9336908199a0ae75d9c4264bf296123f94ad772fea3b52

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN groupadd --gid 10001 vaultmcp \
    && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /nonexistent --shell /usr/sbin/nologin vaultmcp

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --requirement /app/requirements.txt

COPY --chown=10001:10001 app /app/app
COPY --chown=10001:10001 scripts/healthcheck.py /app/healthcheck.py

USER 10001:10001
EXPOSE 8200

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "/app/healthcheck.py"]

CMD ["python", "-m", "app.server"]
