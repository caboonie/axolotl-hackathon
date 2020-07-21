import requests
import json
import os

# Make a get request to get the latest position of the international space station from the opennotify api.
response = requests.get("https://api.github.com/repos/caboonie/axolotl-hackathon/pulls")

content = json.loads(response.content)
pr_summary = []
slack_info = ''
slack_info = slack_info + 'Hi, here are the PRs for \n'
for pr in content:
	changes = 0
	status_response = requests.get(pr['url'] + '/files')
	files = json.loads(status_response.content)
	for file in files:
		changes += file['changes']
	type_of_review = ''
	if changes < 1000:
		type_of_review = 'Short Review(' + str(changes) + ')'
	elif (changes < 2000 and changes > 1000):
		type_of_review = 'Medium Review(' + str(changes) + ')'
	else:
		type_of_review = 'Long Review(' + str(changes) + ')'
	slack_info = slack_info + pr['body'] + ' - ' + pr['url'] + ' - Type: ' + type_of_review +' - Reporter: <@U017UV4FAG1>' + '\n'

slack_token = 'xoxb-1266930654353-1278198044544-VTZeknhgwnxXk5uFaCkWbuhm'
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
