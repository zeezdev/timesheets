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

up_be:
	docker-compose up ts-be

run_init:
	docker-compose run ts-be python main.py --init

make_migrations:
	# make make_migrations name="My migration"
	docker-compose run ts-be alembic revision --autogenerate -m "${name}"

run_be_pytest:
	docker-compose run ts-be pytest

build_fe:
	docker-compose build --no-cache ts-fe

up_fe:
	docker-compose up ts-fe

run_fe_test:
	docker-compose run ts-fe npm run test-karma

dev_up:
	docker-compose up ts-be ts-fe

# Production

build_web:
	docker-compose -f production.yaml build --no-cache ts-web

push_web:
	docker-compose -f production.yaml push ts-web

up:
	docker-compose -f production.yaml up ts-be ts-web --remove-orphans

backup_db:
	$(eval DATE := $(shell date +%Y%m%d))
	cp db/timesheet.db "db/timesheet.db.${DATE}"
