#!/bin/bash
# Log everything to start_docker.log
exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging in to ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 730335644260.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling Docker image..."
docker pull 730335644260.dkr.ecr.ap-south-1.amazonaws.com/delivery_time:v2

echo "Checking for existing container..."
if [ "$(docker ps -q -f name=model_v2)" ]; then
    echo "Stopping existing container..."
    docker stop model_v2
fi

if [ "$(docker ps -aq -f name=model_v2)" ]; then
    echo "Removing existing container..."
    docker rm model_v2
fi

echo "Starting new container..."
docker run -d -p 80:8000 --name model_v2 -e DAGSHUB_USER_TOKEN=705171615cb002f197303ee05d8813d5f80e089a 730335644260.dkr.ecr.ap-south-1.amazonaws.com/delivery_time:v2
echo "Container started successfully."