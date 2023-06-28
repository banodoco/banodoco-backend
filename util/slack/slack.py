# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from datetime import datetime
from slack_sdk.errors import SlackApiError
import traceback

from neuralblade.settings import SLACK_BOT_TOKEN
from util.sentry import log_sentry_exception


class SlackClient():
    def __init__(self):
        # WebClient instantiates a client that can call API methods
        # When using Bolt, you can use either `app.client` or the `client` passed to listeners.
        self.client = WebClient(token=SLACK_BOT_TOKEN)

    def send_message_to_channel(self, *args, channel: str, text: str, blocks, **kwargs):
        try:
            return self.client.chat_postMessage(*args, channel=channel, text=text, blocks=blocks, **kwargs)
        except SlackApiError as e:
            log_sentry_exception(
                "Slack API Error " + str(e), {}, traceback)

    def files_upload(self, *args, file: bytes, filename: str, filetype: str, channels: str, **kwargs):
        try:
            today = datetime.now()
            date = today.date().strftime("%d-%m-%Y")
            return self.client.files_upload(*args, file=file, filename=f"{filename}_{date}.{filetype}", filetype=filetype, channels=channels, **kwargs)
        except SlackApiError as e:
            log_sentry_exception(
                "Slack API File Upload Error " + str(e), {}, traceback)