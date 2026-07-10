# Platform

A self-hosted platform composed of Docker services, orchestrated via Traefik.

## Services

| Service | Description |
|---|---|
| **Traefik** | Reverse proxy & router |
| **Portal** | React/Vite dashboard linking all services |
| **Application Tracker** | FastAPI backend + Streamlit frontend for tracking job applications |
| **n8n** | Workflow automation |
| **PostgreSQL** | Relational database |
| **Adminer** | Database admin UI |
| **Healthcheck** | Aggregated health status endpoint |

## Requirements

- Docker & Docker Compose
- A `.env` file (see below)

## Setup

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in the values.
3. Start all services:

```bash
docker compose up -d
```

Or use the provided Makefile targets:

```bash
make up     # start
make down   # stop
make logs   # follow logs
```

## License

MIT — see [LICENSE](LICENSE).
