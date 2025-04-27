#!/bin/bash

docker compose down -v
# docker run -v /sftp/sftpuser/files:/data -p 8100:8100 -d --name web_app web_app
docker compose up -d --build