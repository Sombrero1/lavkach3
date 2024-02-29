#!/bin/bash

#alembic upgrade head


gunicorn app.bff.server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8003