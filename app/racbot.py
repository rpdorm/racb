#### REDDIT ANTI-CENSORSHIP BOT
#### SAVING THREADS SINCE DEC 2018

#!/usr/local/bin/python
from datetime import datetime
import os
import praw
import time
import yaml


def load_config():
    """
    loads config.yml
    """
    with open('config.yml', 'r') as f:
        data = yaml.load(f)
    return data['subreddit']['original'], data['subreddit']['new'], data['user']


def print_debug(*args):
    if user['debug']:
        print(u' '.join(args))


def log(*args):
    timestamp = datetime.now()
    print(u'{}: {}'.format(timestamp, u' '.join(args)))


def reddit_instance():
    return praw.Reddit(
        client_id=user['client_id'],
        client_secret=user['client_secret'],
        password=user['password'],
        user_agent=user['user_agent'],
        username=user['username'])


def save_thread(thread):
    """
    saves thread content in seperate text files
    """
    for part in thread:
        save_path = '.data/{}/threads/{}/{}.txt'.format(OC_SUBREDDIT, thread['id'], part)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(thread[part].encode('utf-8'))
            f.close()


def load_threads():
    """
    :return: all saved thread ids from folder names
    """
    try:
        saved = os.listdir('.data/{}/threads'.format(OC_SUBREDDIT))
    except FileNotFoundError:
        saved = []
    return saved


def submission_data(thread_id):
    """
    :return: thread data based on thread id
    """
    submission = reddit.submission(id=thread_id)
    thread_data = {'id': submission.id,
                   'title': submission.title,
                   'author': submission.author.name,
                   'body': submission.selftext,
                   'permalink': submission.permalink
                   }
    return thread_data


def scan_new_threads():
    saved_ids = load_threads()
    log('Checking r/{}'.format(OC_SUBREDDIT))

    for new_thread in reddit.subreddit(OC_SUBREDDIT).new(limit=user['limit']):
        thread = submission_data(new_thread.id)
        # CHECK IF THREAD IS ALREADY SAVED
        if thread['id'] in saved_ids:
            pass
        else:
            log(u'Saving #{} {}'.format(thread['id'], thread['title']))
            save_thread(thread)
            saved_ids.append(thread['id'])

    check_removed(saved_ids)
    log('Pausing for {}s...'.format(user['sleep']))
    time.sleep(user['sleep'])


def check_removed(saved_ids):
    """
    compares saved threads with removed threads
    """
    print('checking removed')
    for id in saved_ids:
        submission = reddit.submission(id=id)
        shared_name = 'shared_threads.txt'
        try:
            f = open(shared_name, 'r')
            shared_threads = f.read()
        except IOError:
            open(shared_name, 'a').close()
            shared_threads = []

        if submission.selftext == '[removed]':
            if id not in shared_threads:
                print('{} has been removed'.format(id))
                share_removed_post(id)
                s = open(shared_name, 'a')
                s.write(id + '\n')
                s.close()
        elif submission.locked is True:
            print('{} is locked'.format(id))


def share_removed_post(id):
    """
    shares removed thread with new subreddit
    """
    log('Reporting {}...'.format(id))
    thread = {'id': None,
              'title': None,
              'author': None,
              'body': None,
              'permalink': None
              }

    for part in thread:
        save_path = '.data/{}/threads/{}/{}.txt'.format(OC_SUBREDDIT, id, part)
        if part == 'title':
            with open(save_path, 'r') as f:
                original_content = f.read()
            thread['title'] = '[REMOVED] {}'.format(original_content)
        else:
            original_content = open(save_path, 'r')
            thread[part] = original_content.read()
            original_content.close()

    selftext = '~ [OC] ({}) by u/{}\n\n{}'.format(thread['permalink'], thread['author'], thread['body'])
    reddit.subreddit(X_SUBREDDIT).submit(thread['title'], selftext=selftext)


if __name__ == '__main__':
    OC_SUBREDDIT, X_SUBREDDIT, user = load_config()
    reddit = reddit_instance()
    print_debug('Entering main loop...')

    while True:
        scan_new_threads()