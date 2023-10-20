# Docker

docker_build_be:
	docker build -t zeezdev/timesheet-be .

docker_run_be:
	docker run -p 8874:8874 -v ./db:/db ./:/app  --rm --name ts-be zeezdev/timesheet-be

docker_build_fe:
	docker build -t zeezdev/timesheet-fe ts

docker_run_fe:
	docker run -p 8875:8875 --rm --name ts-fe zeezdev/timesheet-fe

# Docker-compose

build_be:
	docker-compose build --no-cache ts-be

push_be:
	docker-compose push ts-be

run_migrate:
	docker-compose run ts-be python main.py --migrate

dev_run_be_pytest:
	docker-compose run ts-be pytest

dev_up_be:
	docker-compose up ts-be

dev_build_fe:
	docker-compose build --no-cache ts-fe

dev_up_fe:
	docker-compose up ts-fe

dev_up:
	docker-compose up ts-be ts-fe

# Production

prod_build_web:
	docker-compose -f docker-compose.yaml -f production.yaml build --no-cache ts-web

prod_push_web:
	docker-compose -f docker-compose.yaml -f production.yaml push ts-web

up:
	docker-compose -f docker-compose.yaml -f production.yaml up ts-be ts-web
