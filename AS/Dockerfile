FROM python:3.5

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 799 na3533 && \
    useradd -r -u 999 -g na3533 na3533

# Set up a working folder and install the pre-reqs
WORKDIR /app

RUN pip install Flask

RUN pip install requests

USER root

COPY --chown=na3533:na3533 . .

CMD [ "python", "./AS.py" ]
