#!/usr/bin/env sh

set -e

# Apply DB migrations
alembic upgrade head
