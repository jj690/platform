#!/bin/sh

set -eu

exec streamlit run /app/main.py \
    --server.address=0.0.0.0 \
    --server.port="${TRACKER_FRONTEND_PORT}" \
    --server.headless=true \
    --server.baseUrlPath="${STREAMLIT_BASE_PATH}" \
    --browser.serverAddress="${PLATFORM_HOST}" \
    --browser.serverPort="${PLATFORM_HTTP_PORT}"