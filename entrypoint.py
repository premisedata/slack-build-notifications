import sys
import json
from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError

url = sys.argv[4] 
webhook = WebhookClient(url)

def message_builder(outcome, project, build, repo):
    color = "#000000"
    success_color = "#4BB543"
    failure_color = "#FF0000"
    
    if outcome == "success":
        color = success_color
    if outcome == "failure":
        color = failure_color
    # need to account for different outcomees? cloud run vs maven
    org = repo.split("/")[0]
    service = repo.split("/")[1]
    message = [
        {
            "color": color,
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"outcome: {outcome}"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Service: {service}"},
                },
                {"type": "divider"},
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "project"},
                            "value": f"https://console.cloud.google.com/home/dashboard?project={project}",
                            "url": f"https://console.cloud.google.com/home/dashboard?project={project}",
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": f"Build #{build}"},
                            "value": f"https://github.com/{org}/{service}/actions/runs/{build}",
                            "url": f"https://github.com/{org}/{service}/actions/runs/{build}",
                        },
                    ],
                },
            ],
        }
    ]
    return message


if __name__ == "__main__":
    outcome = sys.argv[1]
    project = sys.argv[2]
    build = sys.argv[3]
    repo = sys.argv[5]

    try:
        formatted_message = message_builder(outcome, project, build, repo)
        response = webhook.send(
            attachments=formatted_message
        )
    except SlackApiError as e:
        assert e.response["error"]
