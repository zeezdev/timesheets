# Timesheet - time tracking system

## Work with project using Docker Compose

### First run

* Make a directory for a database `mkdir db`.
* Build backend image `make docker_compose_build_be`.
* Build frontend image `make docker_compose_build_fe`.
* Init the database `make docker_compose_be_migrate`.

### Up service

* `make docker_compose_up`

### Run backend tests

* `make docker_compose_be_tests`
