FROM python:2

RUN pip install praw

ADD . /racbot

WORKDIR /racbot
ENTRYPOINT [ "python", "./racbot.py" ]
