FROM python:3.7

RUN pip install praw
RUN pip install pyyaml

ADD . /racbot

WORKDIR /racbot
ENTRYPOINT [ "python", "./app/racbot.py" ]