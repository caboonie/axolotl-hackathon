import requests
import json
import os

# Make a get request to get the latest position of the international space station from the opennotify api.
token = os.environ['GITHUB_TOKEN'] 
headers={'Authorization': 'token f69fe57bfd6bbc03426cec2f2cb76cef3769a4f6'}
response = requests.get("https://api.github.com/repos/caboonie/axolotl-hackathon/pulls", headers=headers)

content = json.loads(response.content)
print(content)
pr_summary = []

blocks = [{  
        "type": "section",
        "text": {  
            "type": "mrkdwn",
            "text": "*Daily PR Summary*"
        }}]
for pr in content:
    changes = 0
    # print('pr',content)
    status_response = requests.get(pr['url'] + '/files', headers=headers)
    files = json.loads(status_response.content)
    for file in files:
        print('file',file)
        changes += file['changes']
    type_of_review = ''
    if changes < 1000:
        type_of_review = 'Short Review(' + str(changes) + ' changes)'
    elif (changes < 2000 and changes > 1000):
        type_of_review = 'Medium Review(' + str(changes) + ' changes)'
    else:
        type_of_review = 'Long Review(' + str(changes) + ' changes)'
    
    jira_link = pr['body'].split('\n')[0].split(': ')[1]
    jira_ticket = jira_link.split('/')[-1]

    blocks.append({  
        "type": "section",
        "block_id": pr['title'],
        "text": {  
            "type": "mrkdwn",
            "text": "<{}|*{}*>\n{}  <{}|Jira {}>\nWaiting on: *{}* (suggested <@{}>)".format(pr['html_url'], pr['title'], type_of_review, jira_link, jira_ticket, 'Review', 'U017UV4FAG1')
        }})

slack_token = os.environ['SLACK_TOKEN'] 
slack_channel = '#test'
slack_icon_url = 'https://th.bing.com/th/id/OIP.ScZ7yk9J7_I9J166r5gLTwHaHa?pid=Api&rs=1'
# slack_user_name = 'axolotl'

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
