#!/bin/sh
cat > /usr/share/nginx/html/env-config.js << EOF
window.__env__ = {
  AT_FRONTEND_URL: "${PLATFORM_PROTOCOL:-http}://${PLATFORM_HOST:-localhost}${TRACKER_PATH:-/tracker}",
  N8N_URL: "${PLATFORM_PROTOCOL:-http}://${PLATFORM_HOST:-localhost}${N8N_PATH:-/n8n}",
  ADMINER_URL: "${PLATFORM_PROTOCOL:-http}://${PLATFORM_HOST:-localhost}${ADMINER_PATH:-/adminer}",
  TRAEFIK_URL: "${PLATFORM_PROTOCOL:-http}://${PLATFORM_HOST:-localhost}${TRAEFIK_PATH:-/traefik}",
  HEALTHCHECK_URL: "${PLATFORM_PROTOCOL:-http}://${PLATFORM_HOST:-localhost}/health",
};
EOF
exec "$@"
