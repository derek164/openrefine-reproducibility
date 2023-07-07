docker compose up
docker attach openrefine-client
docker-compose run --rm --entrypoint python openrefine-client /app/main.py
docker-compose run --rm --entrypoint openrefine openrefine-client --list
docker-compose run --rm --entrypoint openrefine openrefine-client --info "wine"


# docker build --no-cache -t openrefine-python-client:latest .
# docker tag openrefine-python-client:latest derekz325/openrefine-python-client:latest
# docker push derekz325/openrefine-python-client:latest

# https://docs.docker.com/build/building/multi-platform/#getting-started
# https://stackoverflow.com/questions/59613303/how-do-i-make-multi-arch-docker-images
# https://medium.com/@josephadewole1/how-to-build-multiarch-images-in-docker-4cdd552c2fe3
docker buildx create --name mybuilder --driver docker-container --bootstrap
docker buildx use mybuilder
docker buildx inspect
export DOCKER_CLI_EXPERIMENTAL=enabled
docker buildx build --platform linux/amd64,linux/arm64 -f ref/Dockerfile -t derekz325/openrefine-python-client:latest --output type=registry .


docker system prune -f
rm -rf app/data/*.project app/data/workspace*.json app/data/dbextension