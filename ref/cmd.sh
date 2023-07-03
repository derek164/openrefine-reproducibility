docker compose up
docker attach openrefine-client
docker-compose run --rm -it --entrypoint python openrefine-client /app/main.py
# docker-compose run --rm -it --entrypoint openrefine openrefine-client --list
# docker-compose run --rm -it --entrypoint openrefine openrefine-client --info "wine"
