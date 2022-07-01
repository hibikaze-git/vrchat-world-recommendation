FROM python:3.8.12

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Tokyo

WORKDIR /django/myproject

RUN apt update && apt upgrade -y \
 && apt install -y wget \
 && pip install -U pip

# for django
RUN pip install django==4.0.2

# for MariaDB
RUN pip install mysqlclient==2.1.0

RUN pip install pillow==9.1.1

RUN pip install requests

# Google Chrome selenium
RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt update && apt install -y google-chrome-stable=103.*

ADD https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && unzip chromedriver_linux64.zip

RUN pip install selenium && pip install chromedriver_binary==103.*