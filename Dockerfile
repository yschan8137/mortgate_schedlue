FROM python:3.9-slim-buster

# copy requirement.txt to the image.
COPY ./requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade -r requirements.txt
# copy files in root path to the reposity in docker image.
COPY ./main.py ./
# add Loan and Dashboard folders to docker image.
ADD Loan/ /Loan/
ADD Dashboard/ /Dashboard/


ENV PORT=80
EXPOSE 80
CMD ["python", "./main.py", "--host", "0.0.0.0", "--port", "80"]

# deployment: docker build -t my-amort .
# run the container: docker run -p 80:80 -e DASH_CALLBACK_FUNCTIONS_FILENAME=main.py my-amort_<date-ver.> 

#run a command: docker run <image_name> python -c "import dash; print(dash.__version__)"

#excute a script in docker container: docker exec mycontainer bash -c "[path]"

# debug: docker attach <container-name>

# view the files in the docker image