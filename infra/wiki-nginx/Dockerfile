FROM gcr.io/google.com/cloudsdktool/cloud-sdk:alpine

RUN apk add --no-cache nginx bash \
  && mkdir -p /var/log/nginx /var/lib/nginx/tmp /usr/share/nginx/html \
  && chown -R nginx:nginx /var/log/nginx /var/lib/nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV GCS_BUCKET=conifervision-wiki-prod
ENV PORT=8080

EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
