from flask import Flask, render_template, request
import praw
import prawcore
import re
import os
import configparser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Reddit API info

# Check for production env

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    client_id= os.environ.get('client_id')
    client_secret = os.environ.get('secret')
    user_agent = os.environ.get('agent')
else:
    config = configparser.ConfigParser()
    config.read('config.ini')

    client_id = config.get('REDDIT','id')
    client_secret= config.get('REDDIT', 'secret')
    user_agent= config.get('REDDIT', 'agent')

# Reddit API info
reddit = praw.Reddit(client_id= client_id,
                     client_secret= client_secret,
                     user_agent= user_agent)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # User inputs for search function
    if request.method == 'GET':
        sub_name = request.args.get('InputSubreddit')
        key_name = request.args.get('InputKeyword')

        select_item = request.args.get('select-item')
        select_limit = request.args.get('select-limit')

        key_filter = request.args.get('key-filter')
        sub_filter = request.args.get('sub-filter')

        sub_name = sub_name.replace(",", "+")
        sub_name = sub_name.replace(" ", "")

    if sub_filter != '':
        sub_name = sub_name + '-' + sub_filter

    results = []
    urls = []
    comments = []

    subreddit = reddit.subreddit(sub_name)
    hot_sub = subreddit.hot(limit=int(select_limit))
    top_sub = subreddit.top(limit=int(select_limit))
    new_sub = subreddit.new(limit=int(select_limit))

    if select_item == 'Hot':
        sort_sub = hot_sub
    elif select_item == 'New':
        sort_sub = new_sub
    elif select_item == 'Top':
        sort_sub = top_sub

    # Search for keyword in submission titles using reddit API
    try:
        for submission in sort_sub:
            if re.search(key_name, submission.title, re.IGNORECASE):
                results.append(submission.title)
                urls.append(submission.url)
                comments.append('http://www.reddit.com' + submission.permalink)
                if re.search(key_filter, submission.title, re.IGNORECASE) and key_filter != '':
                    results.pop()
                    urls.pop()
                    comments.pop()
    except (prawcore.exceptions.Redirect, TypeError) as error:
        return render_template('index.html', error=error)

    # used zip function to combine 3 lists for iteration, urls, submission results, and submission comments
    return render_template('search.html', reddit_info = zip(urls, results, comments))

if __name__ == '__main__':

    app.run()