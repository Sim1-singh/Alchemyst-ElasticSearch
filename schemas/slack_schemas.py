# import dataclasses as dc
from typing import Any, List, Optional

from pydantic import BaseModel


# @dc.dataclass
class SlackAuthorization(BaseModel):
    """DTO for a Slack authorization"""

    enterprise_id: Optional[str]
    team_id: str
    user_id: str
    is_bot: bool
    is_enterprise_install: bool


# @dc.dataclass
class BlockType(BaseModel):
    """DTO for a Slack block type"""

    type: str
    block_id: Optional[str]
    elements: Optional[List["BlockType"]]
    user_id: Optional[str]
    text: Optional[str]


# @dc.dataclass
class SlackMentionEvent(BaseModel):
    """DTO for a Slack mention event"""

    client_msg_id: str
    type: str
    text: str
    user: str
    ts: str
    blocks: List[Any]
    team: str
    channel: str
    event_ts: str


# @dc.dataclass
class SlackMention(BaseModel):
    """DTO for a Slack mention"""

    token: str
    team_id: str
    api_app_id: str
    event: SlackMentionEvent
    type: str
    event_id: str
    event_time: int
    authorizations: List[SlackAuthorization]
    is_ext_shared_channel: bool
    event_context: str


# @dc.dataclass
class SlackThreadMessageEvent(BaseModel):
    """DTO for a Slack message event"""

    client_msg_id: str
    type: str
    text: str
    user: str
    ts: str
    blocks: List[Any]
    team: str
    channel: str
    event_ts: str
    channel_type: str
    thread_ts: Optional[str]
    parent_user_id: Optional[str]


class SlackChannelMessageEvent(BaseModel):
    """DTO for a Slack message event"""

    client_msg_id: str
    type: str
    text: str
    user: str
    ts: str
    blocks: List[Any]
    team: str
    channel: str
    event_ts: str
    channel_type: str


# @dc.dataclass
class SlackMessage(BaseModel):
    """DTO for a Slack message"""

    token: str
    team_id: str
    context_team_id: Optional[str]
    context_enterprise_id: Optional[str]
    api_app_id: Optional[str]
    event: SlackThreadMessageEvent | SlackChannelMessageEvent
    type: str
    event_id: str
    event_time: int
    authorizations: List[SlackAuthorization]
    is_ext_shared_channel: bool
    event_context: str
