#!/bin/bash


# login in ecr
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 730335644260.dkr.ecr.ap-south-1.amazonaws.com


#pull the latest image
docker pull 730335644260.dkr.ecr.ap-south-1.amazonaws.com/delivery_time:v2


docker stop model_v2 || true
docker rm model_v2 || true


# Run the Docker container
docker run -d -p 80:8000 -e DAGSHUB_USER_TOKEN=705171615cb002f197303ee05d8813d5f80e089a --name model_v2 730335644260.dkr.ecr.ap-south-1.amazonaws.com/delivery_time:v2