import os
from pprint import pprint
import smtplib
import time

import praw


USER_AGENT = 'pip_boy_checker at https://github.com/grantmcconnaughey/pip-boy-checker'
SUBMISSIONS_TO_CHECK = 20
SEARCH_WORDS = ['pip boy', 'pip-boy', 'in stock', 'in-stock', 'truth']
SECONDS_BETWEEN_CHECKS = 60
GMAIL_USER = os.environ['GMAIL_USER']
GMAIL_PWD = os.environ['GMAIL_PWD']

# A list of submission ids where a search word match was found.
matches = []


def check_subreddit(subreddit):
    for submission in subreddit.get_hot(limit=SUBMISSIONS_TO_CHECK):
        found = False
        for word in SEARCH_WORDS:
            if word.lower() in submission.title.lower():
                found = True
        if found and submission.id not in matches:
            send_success_email(submission.permalink)
            matches.append(submission.id)


def send_success_email(url):
    to = ['grantmcconnaughey@gmail.com']
    from_email = GMAIL_USER
    pwd = GMAIL_PWD
    subject = 'Pip Boy edition in stock!'
    body = 'Pip Boy edition in stock! See ' + url

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
        r = praw.Reddit(user_agent=USER_AGENT)

        fo4 = r.get_subreddit('fo4')
        check_subreddit(fo4)

        fallout = r.get_subreddit('fallout')
        check_subreddit(fallout)

        time.sleep(SECONDS_BETWEEN_CHECKS)


if __name__ == '__main__':
    main()
