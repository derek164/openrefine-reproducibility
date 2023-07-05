start:
	@docker compose -f .devcontainer/docker-compose.yml up -d

run:
	@docker-compose -f .devcontainer/docker-compose.yml run --rm -it --entrypoint python openrefine-client /app/main.py

explore:
	@python3 app/explore.py

stop:
	@docker-compose -f .devcontainer/docker-compose.yml stop
	@docker system prune -f
	@rm -rf app/data/*.project app/data/workspace*.json app/data/dbextension

format:
	@isort .
	@black .
