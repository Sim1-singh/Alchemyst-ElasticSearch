"""Entrypoint of the Alchemyst.ai Slack integration
"""

# Import the async app instead of the regular one
import asyncio
import json
import os

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncAck, AsyncApp, AsyncSay
from slack_sdk.web.async_client import AsyncWebClient

from handlers.message_handlers import thread_handler
from schemas.slack_schemas import SlackMessage, SlackThreadMessageEvent
from utils.message_utils import (
    get_all_messages_in_thread,
    is_message_a_mention,
    is_message_in_thread,
)
from utils.user_utils import get_user_id_from_message

from config import BACKEND_BASE_URL, BOT_USER_OAUTH_TOKEN, SLACK_APP_TOKEN

load_dotenv()

app = AsyncApp(
    token=BOT_USER_OAUTH_TOKEN,
    name="Maya - The Alchemyst Sales Executive",
)

async_client = app.client


@app.event("message")
async def message_action(body: SlackMessage, say: AsyncSay, logger) -> None:
    """Handle a message event"""
    print(json.dumps(body, indent=4))
    body_deserialized = SlackMessage(**body)
    event = body_deserialized.event
    channel_id = body_deserialized.event.channel

    sender = await get_user_id_from_message(body_deserialized)
    thread_ts = event.thread_ts if isinstance(event, SlackThreadMessageEvent) else None

    is_mention = is_message_a_mention(body_deserialized)  # Is the message mention
    is_in_thread = is_message_in_thread(body_deserialized)  # Is the message in thread
    # Handle Mentions here

    messages_received = await get_all_messages_in_thread(
        async_client, body_deserialized
    )

    messages_to_index = messages_received.get("messages", [])

    if is_mention:
        print("Mention event received.")
        # If the message is a mention, reply in the channel
        # TODO: Handle the case where the message is a mention using an appropriate handler.
        # Example: async def handle_message_mention(body: SlackMessage, say, logger) -> None:
        await thread_handler(messages_to_index, say, logger, mention=True)
    else:
        await thread_handler(messages_to_index, say, logger, mention=False)


@app.command("/add-api-key")
async def admin_command(ack: AsyncAck, say: AsyncSay, command):
    """Handle adding API Key to initialize bot inside workspace"""
    # Acknowledge command request
    await ack()

    # Check if the user is an admin
    user_id = command["user_id"]
    workspace_id = command["team_id"]

    user_info = await async_client.users_info(user=user_id)
    if user_info["user"]["is_admin"]:
        # Execute admin command
        await say(f"Hello, admin <@{user_id}>! You said: {command['text']}")
        # TODO: Add the register_api_key function here
        # await register_api_key(workspace_id, user_id, command["text"])
    else:
        await say(f"Sorry, <@{user_id}>, but this command is only for admins.")


@app.event("app_home_opened")
async def open_app_home_tab(client: AsyncWebClient, event, logger):
    """Handle app_home_opened event"""
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        await client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home_* :tada:",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This is a section block :ghost:",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Select a conversation from the dropdown to send a message",
                        },
                        "accessory": {
                            "type": "conversations_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a conversation",
                            },
                            "action_id": "conversation_select",
                        },
                    },
                ],
            },
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.event("call_rejected")
async def call_rejected_action(body, say: AsyncSay, logger) -> None:
    """Handle a call rejected event"""
    print(body.event.text)
    print(body.event.blocks)
    # logger.info(body)
    await say(
        "What's up?"
    )  # Use say.__call__ to avoid the type checker complaining about the missing thread_ts argument


@app.command("/hello-bolt-python")
async def command(ack: AsyncAck, body, respond):
    """Handle a /hello-bolt-python command invocation"""
    await ack()
    await respond(f"Hi <@{body['user_id']}>!")


if __name__ == "__main__":
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler.start_async())
