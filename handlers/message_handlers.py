from logging import Logger
from typing import Any, Dict, List
import time
from slack_bolt import Say

from schemas.slack_schemas import SlackMention, SlackMessage

from client.client import request as client_req
from config import BACKEND_BASE_URL


async def thread_handler(
    context_messages: List[Dict[str, Any]],
    say: Say,
    logger: Logger,
    mention: bool = False,
) -> None:
    """Handle a message in a thread"""
    print("thread_handler")
    print(context_messages)
    # print(body.event.blocks)
    # logger.info(body)
    # await say(
    #     "What's up?"
    # )  # Use say.__call__ to avoid the type checker complaining about the missing thread_ts argument
    message: str = ""

    print("Context messages = ", context_messages)
    if len(context_messages) == 1:
        # message = (
        #     f"Detected a single message in a thread: {context_messages[0]['text']}"
        # )
        message = await client_req(
            method="POST", endpoint="/maya/reply", data={"context": context_messages}
        )
    elif len(context_messages) > 1:
        # message = f"Detected {len(context_messages)} messages in the thread: {list(map(lambda x: x['text'], context_messages))}"
        message = await client_req(
            method="POST", endpoint="/maya/reply", data={"context": context_messages}
        )

    message = message.get("message", "Sorry, I didn't get that.")

    if mention or len(context_messages) > 1:
        # TODO: Write a function to send request to an endpoint that indexes messages in the core platform
        ...

    # NOTE: Log the messages to the logging endpoint in the core.
    await client_req(
        endpoint="/logs/slack",
        method="POST",
        data=[
            {
                "assistant": "Maya",
                "timestamp": time.time(),
                "operations_data": {
                    "context": context_messages,
                    "bot_reply": message,
                    "timestamp": context_messages[0]["ts"],
                    "workspace_id": context_messages[0]["team_id"],
                    "channel": context_messages[0]["event"]["channel"],
                    "is_bot_mentioned": mention,
                },
            },
        ],
    )

    await say(
        message,
        # NOTE: If there is a message in a thread, we need to reply to the thread, else we create a thread by replying to the channel message
        thread_ts=context_messages[0].get("thread_ts", context_messages[0].get("ts")),
    )
