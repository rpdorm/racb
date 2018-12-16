#### REDDIT ANTI-CENSORSHIP BOT
#### Version: 0.1.0
#### Created by u/rpdorm
#### Contributors:
#### SAVING THREADS SINCE DEC 2018

#!/usr/local/bin/python
import yaml
import praw
import time
import os
from os import environ
from datetime import datetime

with open('config.yml', 'r') as f:
    data = yaml.load(f)
    print(data)

OC_SUBREDDIT = data['subreddit']['original']
X_SUBREDDIT = data['subreddit']['new']
LIMIT = data['user']['limit']
USERNAME = data['user']['username']
PASSWORD = data['user']['password']
CLIENT_ID = data['user']['client_id']
CLIENT_SECRET = data['user']['client_secret']
DEBUG = data['user']['debug']
SLEEP_TIMEOUT = data['user']['sleep']
USER_AGENT = data['user']['user_agent']

USER_AGENT = 'script:reddit anti-censorship bot:v0.1.0:created by /u/rpdorm'

if not OC_SUBREDDIT:
    raise ValueError('Missing Environment Variable: RACBOT_OC_SUBREDDIT')

def print_debug(*args):
    if DEBUG:
        print(u' '.join(args))

def log(*args):
    timestamp = datetime.now()
    print(u'{}: {}'.format(timestamp, u' '.join(args)))

def Reddit():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME)

# SCAN NEW THREADS
def scan_new_threads():
    reddit = Reddit()

    # SCAN NEW THREADS
    f_threads = open('threads.txt', 'a')
    log('Checking r/{}'.format(OC_SUBREDDIT))
    for new_thread in reddit.subreddit(OC_SUBREDDIT).new(limit=LIMIT):
        saved = False
        submission = reddit.submission(id=new_thread.id)
        title = submission.title
        # CHECK IF THREAD IS ALREADY SAVED
        if submission.id in open('threads.txt').read():
            saved=True
        # IF NOT...
        if saved is False:
            log(u'Saving #{} {}'.format(submission.id, submission.title))
            ## SAVE THEM
            author = submission.author.name
            permalink = submission.permalink
            e = 'threads/{}/title.txt'.format(submission.id)
            if not os.path.exists(e):
                os.makedirs(os.path.dirname(e))
            with open(e, 'w') as f_thread_title:
                f_thread_title.write(title.encode('utf-8'))
                f_thread_title.close()
            f = 'threads/{}/body.txt'.format(submission.id)
            with open(f, 'w') as f_thread_body:
                f_thread_body.write(submission.selftext.encode('utf-8'))
                f_thread_body.close()
            g = 'threads/{}/author.txt'.format(submission.id)
            with open(g, 'w') as f_thread_author:
                f_thread_author.write(author.encode('utf-8'))
                f_thread_author.close()
            h = 'threads/{}/permalink.txt'.format(submission.id)
            with open(h, 'w') as f_thread_permalink:
                f_thread_permalink.write(permalink.encode('utf-8'))
                f_thread_permalink.close()
            f_threads.write(submission.id + '\n')
    check_removed()
    time.sleep(SLEEP_TIMEOUT)

def check_removed():
    reddit = Reddit()
    saved_threads = os.listdir('threads')
    num_saved_threads = len(saved_threads)
    for x in range(0,num_saved_threads):
        this_thread = saved_threads[x]
        submission = reddit.submission(id=this_thread)
        if submission.selftext == '[removed]':
            if this_thread not in open('shared_threads.txt').read():
                log('{} has been removed'.format(this_thread))
                s = open('shared_threads.txt', 'a')
                share_removed_post(this_thread)
                s.write(this_thread + '\n')
        elif submission.locked is True:
            log('{} is locked'.format(this_thread))

def share_removed_post(thread):
    reddit = Reddit()
    log('Reporting {}...'.format(thread))
    title = 'threads/{}/title.txt'.format(thread)
    author = 'threads/{}/author.txt'.format(thread)
    body = 'threads/{}/body.txt'.format(thread)
    permalink = 'threads/{}/permalink.txt'.format(thread)

    oc_title = open(title, 'r')
    removed_title = '[REMOVED] {}'.format(oc_title.read())
    oc_title.close()

    oc_author = open(author, 'r')
    removed_author = oc_author.read()
    oc_author.close()

    oc_body = open(body, 'r')
    removed_body = oc_body.read()
    oc_body.close()

    oc_permalink = open(permalink, 'r')
    removed_permalink = oc_permalink.read()
    oc_permalink.close()

    # REORG
    t = open('temp.txt', 'w')
    t.write('~ [OC]({}) by u/{}'.format(removed_permalink, removed_author))
    t.write('\n\n')
    t.write(removed_body)
    t.close()
    # POST
    x = open('temp.txt', 'r')
    selftext = x.read()
    new_cross_post = reddit.subreddit(X_SUBREDDIT).submit(removed_title, selftext=selftext)


print_debug('Entering main loop...')
while True:
    scan_new_threads()
