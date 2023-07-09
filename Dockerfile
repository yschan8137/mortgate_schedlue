FROM python:3.11-bookworm
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
# deployment: docker build -t my-amort .
# run the container: docker run -p 80:5000 -d my-amort
# update the scripts: docker-compose up -d --build
