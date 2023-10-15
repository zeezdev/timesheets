# Docker

docker_build_be:
	docker build -t zeezdev/timesheet-be .

docker_run_be:
	docker run -p 8874:8874 -v ./db:/app/db --rm --name ts-be zeezdev/timesheet-be

docker_build_fe:
	docker build -t zeezdev/timesheet-fe ts

docker_run_fe:
	docker run -p 8875:8875 --rm --name ts-fe zeezdev/timesheet-fe

# Docker-compose

docker_compose_be_build:
	docker-compose build --no-cache ts-be

docker_compose_be_migrate:
	docker-compose run ts-be python main.py --migrate

docker_compose_be_tests:
	docker-compose run ts-be pytest

docker_compose_be_up:
	docker-compose up ts-be

docker_compose_fe_build:
	docker-compose build --no-cache ts-fe

docker_compose_fe_up:
	docker-compose up ts-fe

docker_compose_up:
	docker-compose up ts-be ts-fe
