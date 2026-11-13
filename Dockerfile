FROM nginx:1.27-alpine

COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY deploy/snippets/ /etc/nginx/snippets/
COPY site/ /usr/share/nginx/html/

EXPOSE 80
