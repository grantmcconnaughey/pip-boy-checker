#!/usr/bin/env python
import argparse
import os
import smtplib
import sys
import time

import praw

parser = argparse.ArgumentParser()
parser.add_argument('--email', type=str,
                    help='Your email')
parser.add_argument('--password', type=str,
                    help='Your email password')
args = parser.parse_args()

if not args.email or not args.password:
    print 'Missing email or password'
    print 'Usage: python pipboychecker.py --email myemail@gmail.com --password hunter1'
    sys.exit()


USER_AGENT = 'pip_boy_checker for ' + args.email
SUBMISSIONS_TO_CHECK = 20
SEARCH_WORDS = ['pip boy', 'pip-boy', 'in stock', 'in-stock']
SECONDS_BETWEEN_CHECKS = 60
GMAIL_USER = args.email
GMAIL_PWD = args.password

# A list of submission ids where a search word match was found.
matches = []


def check_subreddit(subreddit):
    for submission in subreddit.get_new(limit=SUBMISSIONS_TO_CHECK):
        found = False
        for word in SEARCH_WORDS:
            if word.lower() in submission.title.lower():
                found = True
        if found and submission.id not in matches:
            print 'Found a match! ({})'.format(submission.permalink)
            send_success_email(submission.permalink)
            matches.append(submission.id)


def send_success_email(url):
    to = [args.email]
    from_email = GMAIL_USER
    pwd = GMAIL_PWD
    subject = 'Pip-Boy Checker found a match'
    body = 'Pip-Boy Checker found a match, so the Pip-Boy edition might be in stock!\n\nSee ' + url

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (from_email, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(from_email, pwd)
        server.sendmail(from_email, to, message)
        server.close()
    except Exception as e:
        print 'Failed to send mail ' + str(e)


def main():
    while True:
        try:
            r = praw.Reddit(user_agent=USER_AGENT)

            fo4 = r.get_subreddit('fo4')
            check_subreddit(fo4)

            # Delay between API calls
            time.sleep(3)

            fallout = r.get_subreddit('fallout')
            check_subreddit(fallout)
        except Exception as e:
            # Reddit might be down or something. Just ignore it and try again.
            print 'An exception occurred: ' + str(e)

        time.sleep(SECONDS_BETWEEN_CHECKS)


if __name__ == '__main__':
    main()
