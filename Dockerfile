FROM python:3.9

WORKDIR /app

# copy requirement.txt to the image.
COPY ./requirements.txt .

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade -r requirements.txt pip install dash gunicorn
# copy files in root path to the reposity in docker image.
COPY ./app ./app

# Set the command to run when the container starts
CMD gunicorn --bind 0.0.0.0:8500 app.main

# deployment: docker build -t my-amort .
# run the container: docker run -p 80:80 my-amort_<date-ver.> 

#run a command: docker run <image_name> python -c "import dash; print(dash.__version__)"

#excute a script in docker container: docker exec mycontainer bash -c "[path]"

# debug: docker attach <container-name>

# view the files in the docker image