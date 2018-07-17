#!/usr/bin/env bash

ECHO_PREFIX="[drucker-client example]: "

set -e
set -u

echo "$ECHO_PREFIX Start.."

pip install -r requirements.txt

pip install -r ./drucker-grpc-proto/requirements.txt
python ./drucker-grpc-proto/run_codegen.py
python sample.py