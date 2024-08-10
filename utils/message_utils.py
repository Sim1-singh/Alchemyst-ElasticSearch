import json
from typing import Any, Dict, List

from slack_sdk.web.async_client import AsyncWebClient

from schemas.slack_schemas import (
    SlackChannelMessageEvent,
    SlackMention,
    SlackMessage,
    SlackThreadMessageEvent,
)


def is_message_in_thread(body: SlackMention | SlackMessage) -> bool:
    """Check if the message is in a thread"""
    event = body.event

    if isinstance(event, SlackThreadMessageEvent):
        return True

    return False


def is_message_a_mention(body: SlackMention | SlackMessage) -> bool:
    """Check if the message is a mention"""
    event = body.event

    if isinstance(event, SlackThreadMessageEvent) and event.text.startswith("<@"):
        return True
    elif (
        isinstance(event, SlackChannelMessageEvent)
        and event.text is not None
        and event.text.startswith("<@")
    ):
        return True

    return False


async def get_all_messages_in_thread(
    client: AsyncWebClient, body: SlackMention | SlackMessage
) -> Dict[str, List[Any] | bool]:
    """Get all messages in a thread. If there is no thread, just return a list with the message"""
    print("Getting messages in thread")

    event = body.event
    thread_ts = event.thread_ts if isinstance(event, SlackThreadMessageEvent) else None

    if thread_ts is None:
        print("Returning single message")
        return {
            "thread": False,
            "messages": [
                {
                    "text": event.text,
                    "user": event.user,
                    "ts": event.ts,
                    "blocks": event.blocks,
                    "team": event.team,
                    "channel": event.channel,
                    "event_ts": event.event_ts,
                }
            ],
        }

    messages = []

    cursor = ""

    while True:
        response = await client.conversations_replies(
            channel=event.channel, ts=thread_ts, cursor=cursor
        )
        print(f"Response received with cursor value = {cursor}")
        print(response)
        if response["ok"]:
            messages.extend(response["messages"])

            if response["has_more"]:
                cursor = response["response_metadata"]["next_cursor"]
            else:
                break
        else:
            break

    return {"thread": True, "messages": messages}
