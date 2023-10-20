# Timesheet - time tracking system

## Working with a project using Docker Compose.

### Up service for dev

#### Build images for dev
* build the backend image `make build_be`.
* build the frontend image `make dev_build_fe`.

#### Migration
* Init the database `make run_migrate`.

#### Up
* Up service in the "dev" mode `make dev_up`.

### Up service for prod

#### Build images
* build the backend image `make build_be`.
* build the frontend image `make prod_build_web`.

#### Migration
* Init the database `make run_migrate`.

#### Up

* `make up`

### Run backend tests

* `make dev_be_run_pytest`

### Environment variables

* `TIMESHEET_DB_FILENAME` ('./db/timesheet.db') - the location of the ([SQLite](https://www.sqlite.org/index.html)) database file.

## Images

`zeezdev/timesheet-web` - nginx with the frontend static dist & backend upsetream.
`zeezdev/timesheet-be` - backend (API) for develop & prod.
`zeezdev/timesheet-fe` - frontend for develop.
