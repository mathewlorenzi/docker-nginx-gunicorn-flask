#!/bin/bash
source venv/bin/activate
python web/app/file_watcher.py &
python web/app/app.py