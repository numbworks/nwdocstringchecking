#!/bin/bash

# --- CONFIGURATION ---
PROJECT_NAME="nwdocstringchecking"
PROJECT_VERSION="2.0.1"
PROJECT_ALIAS="nwds"
CLI_NAME="nwdocstringcheckingcli"

COMPANY_NAME="numbworks"
COPYRIGHT="numbworks"
TRADEMARK="numbworks"
FILE_DESCRIPTION="A CLI application designed to identify which methods in a Python file are missing docstrings."

DOCKER_FILE="nwdocstringcheckingcli-dockerfile"
BASE_IMAGE="python:3.12.5-bookworm"

# --- DOCKER IMAGE CHECK ---
if [[ "$(docker images -q $BASE_IMAGE 2> /dev/null)" == "" ]]; then
    docker pull $BASE_IMAGE
fi

# --- BUILD COMMAND ---
time DOCKER_BUILDKIT=1 docker build --progress=plain \
  -f "$DOCKER_FILE" \
  --build-arg PROJECT_NAME="$PROJECT_NAME" \
  --build-arg PROJECT_VERSION="$PROJECT_VERSION" \
  --build-arg PROJECT_ALIAS="$PROJECT_ALIAS" \
  --build-arg CLI_NAME="$CLI_NAME" \
  --build-arg COMPANY_NAME="$COMPANY_NAME" \
  --build-arg COPYRIGHT="$COPYRIGHT" \
  --build-arg TRADEMARK="$TRADEMARK" \
  --build-arg FILE_DESCRIPTION="$FILE_DESCRIPTION" \
  --output . .