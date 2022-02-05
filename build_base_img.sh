#!bin/bash
docker build -t nn-trade/indicators/base-img --ssh default --no-cache -f ./.devcontainer/base_image/Dockerfile .