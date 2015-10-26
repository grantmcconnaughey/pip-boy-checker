# Pip-Boy Checker

Checks [/r/fo4](https://reddit.com/r/fo4) and [/r/fallout](https://reddit.com/r/fallout) for search terms that indicate the Fallout 4 Pip-Boy Edition may be in stock and sends an email to inform you of that.

Note: This script only works with Gmail email addresses.

## Usage

Run the script from the command line like so:

    python pipboychecker.py --email myemail@gmail.com --password hunter1

## Installation

The only library required is [praw](https://pypi.python.org/pypi/praw).

    pip install praw

or install from requirements.txt:

    pip install -r requirements.txt
