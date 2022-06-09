FROM python:3.8.12

WORKDIR /django/myproject

RUN apt-get update && apt-get upgrade -y \
 && pip install -U pip

# for django
RUN pip install django==4.0.2

# for MariaDB
RUN pip install mysqlclient==2.1.0

RUN pip install pillow==9.1.1