#!/usr/bin/env bash

source venv/bin/activate
uvicorn --host localhost --port 8874 api:app --reload
