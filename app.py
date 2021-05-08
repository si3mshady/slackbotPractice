import os
import boto3
from slack_bolt import App

from slack_bolt.adapter.aws_lambda import SlackRequestHandler
# https://slack.dev/bolt-python/concepts#lazy-listeners?
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")

)

@app.command("/cloudwatch")
def listCloudWatchLogs(ack, say, command):
    # Acknowledge command request
    ack()
    say(
        blocks=[
            {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Select your region"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
				
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "us-east-1"
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "us-east-2",
							
						},
						"value": "value-1"
					}
				],
				"action_id": "selected-region"  #action id is needed to fetch and process the output of this block
			}
		}
        ]
    )
 

def process_log_groups(region):
 
    container = []
    logs=boto3.client(
                'logs',
                aws_access_key_id=os.getenv('AccessKeyId'),
                aws_secret_access_key=os.getenv('SecretAccessKey'),
                region_name=region
              
            )


    resp = logs.describe_log_groups()

    groups = [a['logGroupName'] for a in resp['logGroups']]
    

    for entry in groups:
      
        data = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{entry}*"
			}
		} 
        container.append(data)

    return container




@app.action("selected-region")
def action_button_click(body, ack, say):
    
    ack()

    region = body['actions'][0]['selected_option']['text']['text']
    response = process_log_groups(region)

    say({"blocks": response})



if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

# Button and Static Select
# //https://slack.dev/bolt-python/concepts#commands

# https://6b2ff9acfd87.ngrok.io
# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error