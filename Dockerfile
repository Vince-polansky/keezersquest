FROM debian:buster

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y nginx

WORKDIR /var/www/html/

RUN rm index.nginx-debian.html

COPY docker_srcs/nginx.conf /etc/nginx/sites-available/nginx.conf
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf && rm /etc/nginx/sites-enabled/default

COPY keezersquest.nl/ /var/www/html/

CMD service nginx start; bash
