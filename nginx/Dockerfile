FROM nginx
LABEL J. Chaudourne <jchaudourne@laposte.net>

RUN groupadd docker
RUN usermod -a -G docker nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY proxy_conf /etc/nginx/proxy_conf
