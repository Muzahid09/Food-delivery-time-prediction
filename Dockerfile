# Set the base image 
FROM python:3.13.1-slim

# install lightgbm dependency
RUN apt-get update && apt-get install -y libgomp1

# Setup the working directory
WORKDIR /app

# Copy the required files
COPY  requirements-docker.txt ./


# Installing pacakages
RUN pip install -r requirements-docker.txt


# Copy other necessary files
COPY /app_beta.py ./
COPY ./scripts/data_clean_utils.py ./scripts/data_clean_utils.py
COPY ./run_information.json ./



# Exposing the port
EXPOSE 8000


# Run the file using command
CMD [ "python", "./app_beta.py" ]

