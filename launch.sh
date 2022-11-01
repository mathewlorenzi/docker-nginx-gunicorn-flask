#!/bin/bash
pkill python*
res=$(pgrep python*)
if [ "$res" != "" ]; then
    echo "failed to kill all python processes: "$res
    exit 1
fi
source venv/bin/activate
python web/app/file_watcher.py &
python web/app/app.py