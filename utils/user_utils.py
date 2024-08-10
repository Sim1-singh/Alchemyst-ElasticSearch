"""
This file contains functions that are used to get user information from Slack, and other user utilities
"""

from slack_sdk.web.async_client import AsyncWebClient

from schemas.slack_schemas import SlackMessage


async def get_username_from_user_id(client: AsyncWebClient, user_id):
    """Get username from user id"""
    response = await client.users_info(user=user_id)
    if response["ok"]:
        return response["user"]["name"]
    else:
        return None


async def get_user_id_from_message(message: SlackMessage):
    """Get user id from message"""
    return message.event.user


async def get_user_id_from_username(client: AsyncWebClient, username):
    """Get user id from username"""
    response = await client.users_list()
    if response.status_code == 200:
        for member in response.data["members"]:
            if member["name"] == username:
                return member["id"]
    else:
        return None
