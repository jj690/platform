from dotenv import load_dotenv
import os

load_dotenv()

SERVICES = {
    "n8n": os.getenv("N8N_HEALTH_URL"),
    "tracker_api": os.getenv("TRACKER_API_HEALTH_URL"),
    "adminer": os.getenv("ADMINER_HEALTH_URL"),
    "traefik": os.getenv("TRAEFIK_HEALTH_URL"),
}
