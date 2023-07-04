start:
	@docker compose up -d

run:
	@docker-compose run --rm -it --entrypoint python openrefine-client /app/main.py

explore:
	@python3 app/explore.py

stop:
	@docker-compose stop
	@docker system prune -f
	@rm -rf app/data/*.project app/data/workspace*.json app/data/dbextension

format:
	@isort .
	@black .
