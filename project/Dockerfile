# use the python:3.8 base image
FROM python:3.8

# set a key-value label for the Docker image
LABEL maintainer="Amol Jagtap"

# set the working directory to /app within the container
WORKDIR /app

# copy the requirements.txt only first to install dependencies
COPY ./techtrends/requirements.txt .

# run commands within the container. 
# For example, invoke a pip command 
# to install dependencies defined in the requirements.txt file. 
RUN pip install -r requirements.txt

# copy files from the host to the container filesystem. 
# For example, all the files in the techtrends directory
# to the  `/app` directory in the container
COPY ./techtrends .

# initialize database with the pre-defined posts
RUN python init_db.py

# expose the port 3111
EXPOSE 3111

# provide a command to run on container start. 
# For example, start the `app.py` application.
CMD [ "python", "app.py" ]
