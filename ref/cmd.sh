docker build -t openrefine-notebook .
docker pull vimagick/openrefine
docker run --rm -it --entrypoint bash vimagick/openrefine


docker build -t openrefine/client .
docker run --rm -it -v ${PWD}:/app --network host --entrypoint bash openrefine/client
docker run --rm -it -v ${PWD}:/app --network host --entrypoint python openrefine/client /app/main.py
docker run --rm --network host openrefine/client --list


refine_server = refine.Refine(refine.RefineServer())
project = refine_server.new_project(
    project_file="work/data/wine-raw.csv",
    project_name="test",
    separator=","
)


docker compose up
docker attach openrefine-client
docker-compose run --rm -it --entrypoint python openrefine-client /app/main.py
docker-compose run --rm -it --entrypoint openrefine openrefine-client --list
docker-compose run --rm -it --entrypoint openrefine openrefine-client --info "wine"
