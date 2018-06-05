FROM python:3.6.1

ADD project/requirements /requirements
RUN pip install -r requirements/dev.txt

EXPOSE 8000

WORKDIR /dash
