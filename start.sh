#!/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker app:app