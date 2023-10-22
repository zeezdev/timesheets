# Timesheet - time tracking system

## Working with a project using Docker Compose.

### Up service for dev

#### Build images for dev
* build the backend image `make build_be`.
* build the frontend image `make build_fe`.

#### Migration
* Init the database `make run_migrate`.

#### Up
* Up service in the "dev" mode `make dev_up`.

### Up service for prod

#### Build images
* build the backend image `make build_be`.
* build the frontend image `make build_web`.

#### Migration
* Init the database `make run_migrate`.

#### Up

* `make up`

### Run backend tests

* `make run_be_pytest`

### Environment variables

* `TIMESHEET_DB_FILENAME` ('../db/timesheet.db') - the location of the ([SQLite](https://www.sqlite.org/index.html)) database file.
* `TIMESHEET_API_HOST` ('localhost') - the expected host of API.

## Images

`zeezdev/timesheet-web` - nginx with the frontend static dist & backend upsetream.
`zeezdev/timesheet-be` - backend (API) for develop & prod.
`zeezdev/timesheet-fe` - frontend for develop.
