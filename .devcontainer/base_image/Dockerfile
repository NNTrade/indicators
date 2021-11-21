# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.177.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.9 

RUN apt-get update \
    && apt-get install -y openssh-client git

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN --mount=type=ssh pip3 --no-cache-dir install git+ssh://git@github.com/NNTrade/pandas-data-reader-service-core.git