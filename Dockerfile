from python:3.8.13-slim-buster

RUN apt update && apt install -y curl && curl -sf https://gobinaries.com/ncarlier/webhookd >/tmp/wh.sh && chmod +x /tmp/wh.sh
RUN bash -c "/tmp/wh.sh"

COPY ./ /opt/

WORKDIR  /opt/

EXPOSE 80

CMD ["/usr/local/bin/webhookd","-scripts","scripts","-static-dir", "www","-static-path","/www","-listen-addr", ":80"]