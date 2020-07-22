import requests
import json
import os
import datetime
# from jira_sel import run

# Make a get request to get the latest position of the international space station from the opennotify api.
token = os.environ['GITHUB_TOKEN'] 
headers={'Authorization': 'token {}'.format(token)}
response = requests.get("https://api.github.com/repos/caboonie/axolotl-hackathon/pulls", headers=headers)

PARSE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

content = json.loads(response.content)
# print(content)
pr_summary = []

blocks = [{  
        "type": "section",
        "text": {  
            "type": "mrkdwn",
            "text": "*Daily PR Summary*"
        }}]
for pr in content:
    changes = 0
    status_response = requests.get(pr['url'] + '/files', headers=headers)
    files = json.loads(status_response.content)
    for file in files:
        changes += file['changes']
    type_of_review = ''
    if changes < 50:
        type_of_review = ':green_heart: Short Review (' + str(changes) + ' changes)'
    elif (changes < 1000 and changes > 1000):
        type_of_review = ':yellow_heart: Medium Review (' + str(changes) + ' changes)'
    else:
        type_of_review = ':heart: Long Review (' + str(changes) + ' changes)'
    

    try:
        jira_link = pr['body'].split('\n')[0].split(': ')[1]
        jira_ticket = jira_link.split('/')[-1]
    except:
        jira_link, jira_ticket = '', ''

    pr_owner = pr['user']['login']

    # determine whether state of reviews and respective reviewer ids
    requested_reviewers = {reviewer['login'] for reviewer in pr["requested_reviewers"]}
    review_response = requests.get(pr['url'] + '/reviews', headers=headers)
    reviews = json.loads(review_response.content)
    commented_reviews, approved_reviews = set(), set()
    for review in reviews:
        if review['state'] == "APPROVED":
            approved_reviews.add(review['user']['login'])
        if review['state'] =='COMMENTED':
            commented_reviews.add(review['user']['login'])

    # Retrieve and sort comments based on which comments they reply to
    comments_response = requests.get(pr['url'] + '/comments', headers=headers)
    comments = json.loads(comments_response.content)

    root_comments = set()
    comment_hierarchy = {}
    comment_info = {}
    for comment in comments:
        comment_info[comment['id']] = {'body':comment['body'], 'owner':comment['user']['login']}
        if 'in_reply_to_id' in comment:
            parent = comment['in_reply_to_id']
            comment_hierarchy[parent] = comment['id']
        else:
            root_comments.add(comment['id'])

    # if no reviews, then currently waiting for the requested+recommended reviewers
    # else, go through the review comments and check the last commenter - 
    #  if it is the pr owner, we need reviewers to look again
    #  otherwise, pr owner needs to respond to feedback
    recommended_reviewers = set() # run()
    if len(comments) == 0:
        status = "Waiting for reviews"
        suggested_workers = requested_reviewers|recommended_reviewers-approved_reviews
    else:
        for root_comment in root_comments:
            curr = root_comment
            while curr in comment_hierarchy:
                curr = comment_hierarchy[curr]
            if comment_info[curr]['owner'] != pr_owner:
                status = 'Need to address reviews'
                suggested_workers = {pr_owner}
                break
        else:
            status = 'Awaiting further review'
            suggested_workers = (commented_reviews | requested_reviewers |recommended_reviewers) -approved_reviews-{pr_owner}
    suggested_workers_str = " ".join(["<@{}>".format(user) for user in suggested_workers])
    reviewers_str = " ".join(["<@{}>".format(user) for user in commented_reviews | approved_reviews])
    
    # Determine time since creation and since last update
    time_created = datetime.datetime.strptime(pr['created_at'], PARSE_FORMAT)
    time_since_created = datetime.datetime.utcnow()-time_created
    since_created_str = '{} days'.format(time_since_created.days)
    if time_since_created.days < 1:
        since_created_str = '{:.1f} hours'.format(time_since_created.seconds/3600)

    time_updated = datetime.datetime.strptime(pr['updated_at'], PARSE_FORMAT)
    time_since_updated = datetime.datetime.utcnow()-time_updated
    since_updated_str = '{} days'.format(time_since_updated.days)
    if time_since_updated.days < 1:
        since_updated_str = '{:.1f} hours'.format(time_since_updated.seconds/3600)
    
    # Assemble the Slack notification block
    pr_block_text = "<{}|*{}*>\n{}  <{}|Jira {}>\nMade by {} {} ago, {} since last action\nCurrent reviewers: {}\nStatus: *{}*".format(pr['html_url'], 
                    pr['title'], type_of_review, jira_link, jira_ticket, pr_owner, since_created_str, 
                    since_updated_str, reviewers_str or 'None', status)
    if suggested_workers_str:
        pr_block_text += ' (suggested workers: {})'.format(suggested_workers_str)
    blocks.append({  
        "type": "section",
        "block_id": pr['title'],
        "text": {  
            "type": "mrkdwn",
            "text": pr_block_text
        }})

slack_token = os.environ['SLACK_TOKEN'] 
slack_channel = '#test'
slack_icon_url = 'https://th.bing.com/th/id/OIP.ScZ7yk9J7_I9J166r5gLTwHaHa?pid=Api&rs=1'

def post_message_to_slack(text, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_url': slack_icon_url,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()	

print(blocks)

post_message_to_slack('Daily PR Summary - {} PRs'.format(len(content)), blocks)
