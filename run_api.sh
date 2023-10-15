#!/usr/bin/env bash

source venv/bin/activate
uvicorn --host 0.0.0.0 --port 8874 api:app --reload
