#### REDDIT ANTI-CENSORSHIP BOT
#### Version: 0.1.0
#### Created by u/rpdorm
#### Contributors: 
#### SAVING THREADS SINCE DEC 2018

#!/usr/local/bin/python
import praw
import time
import os

OC_SUBREDDIT = ''
X_SUBREDDIT = ''
LIMIT = 5
# AUTHENTICATE AND DEFINE SUBREDDITS
USERNAME = ''
PASSWORD = ''
CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = 'script:reddit anti-censorship bot:v0.1.0:created by /u/rpdorm'

# SCAN NEW THREADS
def scan_new_threads():
	reddit = praw.Reddit(
		client_id=CLIENT_ID,
		client_secret=CLIENT_SECRET,
		password=PASSWORD,
		user_agent=USER_AGENT,
		username=USERNAME)
	# SCAN NEW THREADS
	f_threads = open('threads.txt', 'a')
	print('Checking r/' + OC_SUBREDDIT)
	for new_thread in reddit.subreddit(OC_SUBREDDIT).new(limit=LIMIT):
		saved = False
		submission = reddit.submission(id=new_thread.id)
		title = submission.title
		# CHECK IF THREAD IS ALREADY SAVED
		if submission.id in open('threads.txt').read():
			saved=True
		# IF NOT...
		if saved is False:
			print('Saving ' + submission.id + ' ' + submission.title)
			## SAVE THEM
			author = submission.author.name
			permalink = submission.permalink
			e = 'threads/'+submission.id+'/title.txt'
			if not os.path.exists(e):
				os.makedirs(os.path.dirname(e))
			with open(e, 'w') as f_thread_title:
				f_thread_title.write(title.encode('utf-8'))
				f_thread_title.close()
			f = 'threads/'+submission.id+'/body.txt'
			with open(f, 'w') as f_thread_body:
				f_thread_body.write(submission.selftext.encode('utf-8'))
				f_thread_body.close()
			g = 'threads/'+submission.id+'/author.txt'
			with open(g, 'w') as f_thread_author:
				f_thread_author.write(author.encode('utf-8'))
				f_thread_author.close()
			h = 'threads/'+submission.id+'/permalink.txt'
			with open(h, 'w') as f_thread_permalink:
				f_thread_permalink.write(permalink.encode('utf-8'))
				f_thread_permalink.close()
			f_threads.write(submission.id + '\n')
	check_removed()
	time.sleep(300)

def check_removed():
	reddit = praw.Reddit(
		client_id=CLIENT_ID,
		client_secret=CLIENT_SECRET,
		password=PASSWORD,
		user_agent=USER_AGENT,
		username=USERNAME)
	saved_threads = os.listdir('threads')
	num_saved_threads = len(saved_threads)
	for x in range(0,num_saved_threads):
		this_thread = saved_threads[x]
		submission = reddit.submission(id=this_thread)
		if submission.selftext == '[removed]':
			if this_thread not in open('shared_threads.txt').read():
				print(this_thread + ' has been removed.')
				s = open("shared_threads.txt", "a")
				share_removed_post(this_thread)
				s.write(this_thread + '\n')
		elif submission.locked is True:
			print(this_thread + ' is locked.')

def share_removed_post(thread):
	reddit = praw.Reddit(
		client_id=CLIENT_ID,
		client_secret=CLIENT_SECRET,
		password=PASSWORD,
		user_agent=USER_AGENT,
		username=USERNAME)
	print('Reporting '+ thread +'...')
	title = 'threads/'+thread+'/title.txt'
	author = 'threads/'+thread+'/author.txt'
	body = 'threads/'+thread+'/body.txt'
	permalink = 'threads/'+thread+'/permalink.txt'

	oc_title = open(title, 'r')
	removed_title = '[REMOVED] ' + oc_title.read()
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
	t = open("temp.txt", "w")
	t.write('~ [OC](' + removed_permalink + ') by u/'+ removed_author)
	t.write('\n\n')
	t.write(removed_body)
	t.close()
	# POST
	x = open('temp.txt', 'r')
	selftext = x.read()
	new_cross_post = reddit.subreddit(X_SUBREDDIT).submit(removed_title, selftext=selftext)


while True:
	scan_new_threads()