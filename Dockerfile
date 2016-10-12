FROM python:2-onbuild

MAINTAINER Julien Maupetit <julien@maupetit.net>

RUN rm -fr ./md2pdf && \
  git clone https://github.com/jmaupetit/md2pdf && \
  cd md2pdf && python setup.py install

VOLUME ["/srv"]
WORKDIR /srv
ENTRYPOINT ["md2pdf"]
