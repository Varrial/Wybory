# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./verdana.ttf ./
RUN mkdir -p /usr/share/fonts/truetype/
RUN install -m644 verdana.ttf /usr/share/fonts/truetype/
RUN rm ./verdana.ttf


COPY . /code/