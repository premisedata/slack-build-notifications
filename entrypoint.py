import sys
import json
from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError

url = sys.argv[4] 
webhook = WebhookClient(url)

def message_builder(status, project, build):
    success_color = "#4BB543"
    failure_color = "#FF0000"
    # need to account for different statuses? cloud run vs maven
    message = [
        {
            "color": success_color,
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Status: {status}"},
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
                            "value": f"https://github.com/premisedata/{service}/actions/runs/{build}",
                            "url": f"https://github.com/premisedata/{service}/actions/runs/{build}",
                        },
                    ],
                },
            ],
        }
    ]
    return message


if __name__ == "__main__":
    status = sys.argv[1]
    project = sys.argv[2]
    build = sys.argv[3]

    try:
        formatted_message = message_builder(status, project, build)
        response = webhook.send(
            attachments=formatted_message
        )
    except SlackApiError as e:
        assert e.response["error"]
