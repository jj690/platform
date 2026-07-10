COMPOSE = docker compose
BASE    = -f infra/compose/docker-compose.base.yml
DB      = -f infra/compose/docker-compose.db.yml
TRACKER = -f infra/compose/docker-compose.application-tracker.yml
LOCAL   = -f infra/compose/docker-compose.local.yml

.PHONY: start-tracker start-tracker-dev stop-tracker start-all stop-all logs ps

## Application Tracker --------------------------------------------------------

start-tracker:
	$(COMPOSE) $(BASE) $(DB) $(TRACKER) up -d

start-tracker-dev:
	$(COMPOSE) $(BASE) $(DB) $(TRACKER) $(LOCAL) up -d

stop-tracker:
	$(COMPOSE) $(BASE) $(DB) $(TRACKER) down

## All apps -------------------------------------------------------------------

start-all: start-tracker

stop-all: stop-tracker

## Utilities ------------------------------------------------------------------

logs:
	$(COMPOSE) $(BASE) $(DB) $(TRACKER) logs -f

ps:
	$(COMPOSE) $(BASE) $(DB) $(TRACKER) ps
