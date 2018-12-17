reddit anti-censorship bot

Hi. One day I'm going to be a decent readme!

# Usage

## With docker

```
$ docker build . -t racb:latest
$ docker run \
    -v `pwd`:/app/racbot \
    racb:latest
```

## With docker dev
```
$ docker build . -t racb:latest
$ docker-compose -f \
    docker-compose.dev.yml run \
    --rm app
```

## config file: change default-config.yml to config.yml
```
subreddit: [add subreddit names]
  original: subreddit to scan
  new: subreddit to post to

user: default values [add reddit info]
  limit: 30
    -> You can override the default number of new threads fetched on each timeout
  username:
  password:
  client_id:
  client_secret:
  user_agent:
  debug: False
  sleep: 300
```