FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Defaults that Compose can override at runtime
ENV TRACKER_FRONTEND_PORT=8501 \
    STREAMLIT_BASE_PATH=tracker \
    PLATFORM_HOST=localhost \
    PLATFORM_HTTP_PORT=80

# Informational only. It does not publish the port.
EXPOSE 8501

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]