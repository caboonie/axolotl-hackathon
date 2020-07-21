import requests
import json
import os

# Make a get request to get the latest position of the international space station from the opennotify api.
response = requests.get("https://api.github.com/repos/caboonie/axolotl-hackathon/pulls")
# Print the status code of the response.
# print(response.content)
content = json.loads(response.content)
# print(len(content))
pr_summary = []
slack_info = ''
slack_info = slack_info + 'Hi, here are the PRs for \n'
for pr in content:
	slack_info = slack_info + pr['body'] + ' - ' + pr['url'] + '\n'
    #pr_summary.append(pr['title'])

print(pr_summary)
slack_token = 'xoxb-1266930654353-1278198044544-VN1SnYmdtmKgHFXQvHVXBe3h'
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

post_message_to_slack(slack_info)
