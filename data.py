import re

"""
Handles search function
"""

results = []
urls = []

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