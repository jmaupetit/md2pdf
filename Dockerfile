FROM python:3.6

MAINTAINER Julien Maupetit <julien@maupetit.net>

COPY . /usr/local/src/md2pdf

RUN cd /usr/local/src/md2pdf && \
  pip install -r requirements.txt && \
  python setup.py install

VOLUME ["/app"]
WORKDIR /app
ENTRYPOINT ["md2pdf"]
