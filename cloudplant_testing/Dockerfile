FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN pip3 install Flask

RUN mkdir /app

WORKDIR /app

COPY ./app.py /app/app.py

EXPOSE 8080

CMD ["python3", "app.py"]

