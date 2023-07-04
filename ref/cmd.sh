docker compose up
docker attach openrefine-client
docker-compose run --rm -it --entrypoint python openrefine-client /app/main.py
# docker-compose run --rm -it --entrypoint openrefine openrefine-client --list
# docker-compose run --rm -it --entrypoint openrefine openrefine-client --info "wine"


docker build --no-cache -t openrefine-python-client:latest .
docker tag openrefine-python-client:latest derekz325/openrefine-python-client:latest
docker push derekz325/openrefine-python-client:latest