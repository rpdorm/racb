reddit anti-censorship bot

Hi. One day I'm going to be a decent readme!

# Usage

## With docker

```
$ docker build . -t racb:latest
$ docker run \
  -v `pwd`:/racbot \
  -e PYTHONENCODING=utf-8 \
  -e PYTHONUNBUFFERRED=1 \
  -e RACBOT_OC_SUBREDDIT=_oc_subreddit_ \
  -e RACBOT_USERNAME=_username \
  -e RACBOT_PASSWORD=_password  \
  -e RACBOT_CLIENT_ID=_client_id \
  -e RACBOT_CLIENT_SECRET=_client_secret_ \
  racb:latest
```

## With only a shell :(

```
$ pip install praw
$ PYTHONENCODING=utf-8 \
  PYTHONUNBUFFERRED=1 \
  RACBOT_OC_SUBREDDIT=_oc_subreddit_ \
  RACBOT_USERNAME=_username \
  RACBOT_PASSWORD=_password  \
  RACBOT_CLIENT_ID=_client_id \
  RACBOT_CLIENT_SECRET=_client_secret_ \
  python ./racbot.py

```
## Notes:

The `PYTHONUBBUFFERED` environment variable may be needed if your system is
excessively buffering python's output.

The `PYTHONENCODING` environment variable may also be needed to keep python2
from exiting due to those smelly string encoding exceptions.

You can override the default timeout of 300s between scanning new threads with
the environment variable `RACBOT_SLEEP_TIMEOUT`.

You can override the default number of new threads fetched on each timeout with
`RACBOT_LIMIT`.
