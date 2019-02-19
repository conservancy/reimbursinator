FROM nginx:1.10.3

# copy config files
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./static/ /usr/share/nginx/html/
COPY ./ssl/ /etc/ssl/private/
