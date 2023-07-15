FROM python:3.9-alpine3.13
WORKDIR /
# copy requirement.txt to app file in the imagine.
COPY ./requirements.txt /
RUN pip install -r requirements.txt
# copy everything .
COPY . /Loan Dashboard /
ENV PORT=80
EXPOSE 80
CMD ["python", "./main.py", "--host", "0.0.0.0", "--port", "80"]
# deployment: docker build -t my-amort .
# run the container: docker run -p 8050:8050 my-amort

#run a command: docker run <image_name> python -c "import dash; print(dash.__version__)"
#excute a script in docker container: docker exec mycontainer bash -c "[path]"

# debug: docker attach <container-name>