FROM certbot/certbot:v0.38.0

ENV DOMAIN 'undefined'
ENV EMAIL noreply@qq.com

VOLUME /opt/certbot/config

RUN pip install certbot-dns-hostker
ENTRYPOINT certbot certonly -n --renew-by-default --email ${EMAIL} --text --agree-tos --authenticator certbot-dns-hostker:dns-hostker --certbot-dns-hostker:dns-hostker-credentials /opt/certbot/config/config.ini -d ${DOMAIN}
