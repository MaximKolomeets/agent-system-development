# syntax=docker/dockerfile:1.7

FROM alpine:3.23.5@sha256:fd791d74b68913cbb027c6546007b3f0d3bc45125f797758156952bc2d6daf40

RUN apk add --no-cache \
        autossh=1.4g-r3 \
        openssh-client-default=10.2_p1-r0 \
    && addgroup -g 10006 relay \
    && adduser -D -H -u 10006 -G relay -s /sbin/nologin relay

WORKDIR /app
COPY --chown=10006:10006 scripts/entrypoint.sh /app/entrypoint.sh
COPY --chown=10006:10006 scripts/healthcheck.sh /app/healthcheck.sh
COPY --chown=10006:10006 scripts/generate-key.sh /app/generate-key.sh
RUN chmod 0555 /app/entrypoint.sh /app/healthcheck.sh /app/generate-key.sh

USER 10006:10006
ENTRYPOINT ["/app/entrypoint.sh"]
