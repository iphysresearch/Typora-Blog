FROM python:3.6.0
MAINTAINER Jackeriss <i@jackeriss.com>

RUN mkdir -p /usr/src/typora-blog
WORKDIR /usr/src/typora-blog
COPY . /usr/src/typora-blog

RUN pip install -r requirements/common.txt

EXPOSE 8079

CMD ["bash","run.sh"]
