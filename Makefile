# Utils

backup_db:
	$(eval DATE := $(shell date +%Y%m%d))
	cp db/timesheet.db "db/timesheet.db.${DATE}"

# Develop

build_be:
	docker-compose build --no-cache ts-be

up_be:
	docker-compose up ts-be

run_init:
	docker-compose run ts-be python main.py --init

build_fe:
	docker-compose build --no-cache ts-fe

up_fe:
	docker-compose up ts-fe

dev_up:
	# Run BE & FE using the development docker-compose
	docker-compose up ts-be ts-fe

# Tests

run_be_pytest:
	docker-compose run --build --rm ts-be pytest

run_fe_test:
	docker-compose run ts-fe npm run test-karma

# Alembic

alembic_revision_autogenerate:
	# make make_migrations name="My migration"
	docker-compose run ts-be alembic revision --autogenerate -m "${name}"

alembic_upgrade_head:
	# make make_migrations name="My migration"
	docker-compose run ts-be alembic upgrade head

# Production

build_prod:
	# Build the production image
	docker build -t zeezdev/timesheet -f prod.Dockerfile .

up:
	# Run from the production image
	docker run --rm -p 8874:8874 -p 8875:8875 -v ./db:/db --name ts-prod zeezdev/timesheet

upd:
	# Run from the production image as demon
	docker run --rm -d -p 8874:8874 -p 8875:8875 -v ./db:/db --name ts-prod zeezdev/timesheet
