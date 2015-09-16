FROM microservice
MAINTAINER Cerebro <cerebro@ganymede.eu>

ADD ./supervisor/* /etc/supervisor/conf.d/
ADD . /opt/static-file-server

EXPOSE 80
