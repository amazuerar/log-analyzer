FROM python:3.7
RUN mkdir -p /app
WORKDIR /app
COPY ./access.log /app
COPY ./analyzer.py /app
WORKDIR /app
