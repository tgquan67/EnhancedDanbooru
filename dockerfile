FROM ubuntu:xenial
LABEL maintainer="Quan Tran Gia (tgquan67@gmail.com)"
EXPOSE 5555/tcp
RUN apt-get update && apt-get install python3 python3-pip -y && pip3 install requests Flask
COPY EnhancedDanbooru.py server-flask.py ./
CMD /usr/bin/python3 server-flask.py