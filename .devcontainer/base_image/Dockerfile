# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.177.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.9

RUN apt-get update
RUN apt-get install -y openssh-client git

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY requirements_ssh.txt /tmp/pip-tmp/
RUN --mount=type=ssh pip3 --no-cache-dir install -U -r /tmp/pip-tmp/requirements_ssh.txt \ 
    && rm -rf /tmp/pip-tmp