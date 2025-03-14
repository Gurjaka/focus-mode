import datetime
import requests
from dateutil import parser
from core.config import *


class DiscordManager:
    """Handles Discord status and messaging"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.base_url = "https://discord.com/api/v9"
        self.headers = {
            "Authorization": config.discord_token,
            "Content-Type": "application/json",
        }
        self.user_id = self._get_user_id()
        self.current_status = None
        self.replied_messages: Set[str] = set()
        self.last_replies: Dict[str, datetime.datetime] = (
            {}
        )  # Channel ID -> timestamp of your last reply

    def _get_user_id(self) -> str:
        try:
            resp = requests.get(f"{self.base_url}/users/@me", headers=self.headers)
            resp.raise_for_status()
            return resp.json()["id"]
        except requests.RequestException as e:
            logger.error(f"Failed to get user ID: {e}")
            raise SystemExit(1) from None

    def set_status(self, status: str) -> bool:
        if self.current_status == status:
            logger.debug(f"Status already set to {status}, skipping")
            return True
        try:
            resp = requests.patch(
                f"{self.base_url}/users/@me/settings",
                json={"status": status},
                headers=self.headers,
            )
            resp.raise_for_status()
            logger.info(f"Status updated to {status}")
            self.current_status = status
            return True
        except requests.RequestException as e:
            logger.error(f"Status update failed: {e}")
            return False

    def check_messages(self):
        try:
            channels = requests.get(
                f"{self.base_url}/users/@me/channels", headers=self.headers
            ).json()

            for channel in channels:
                if channel.get("type") == 1:  # DM channel
                    self._process_channel(channel["id"])
        except requests.RequestException as e:
            logger.error(f"Message check failed: {e}")

    def _process_channel(self, channel_id: str):
        try:
            # Check if you've replied recently in this channel
            self._update_your_last_reply(channel_id)

            messages = requests.get(
                f"{self.base_url}/channels/{channel_id}/messages?limit=5",
                headers=self.headers,
            ).json()

            for msg in messages:
                if self._should_reply(msg, channel_id):
                    self._send_reply(channel_id, msg)
        except requests.RequestException as e:
            logger.error(f"Failed to process channel {channel_id}: {e}")

    def _update_your_last_reply(self, channel_id: str):
        """Check and update when you last replied in this channel"""
        try:
            messages = requests.get(
                f"{self.base_url}/channels/{channel_id}/messages?limit=10",
                headers=self.headers,
            ).json()

            # Look for your messages
            for msg in messages:
                if msg["author"]["id"] == self.user_id:
                    # Found your message
                    last_reply_time = parser.parse(msg["timestamp"])
                    self.last_replies[channel_id] = last_reply_time
                    logger.debug(
                        f"Found your last reply in channel {channel_id} at {last_reply_time}"
                    )
                    break
        except requests.RequestException as e:
            logger.error(f"Failed to check your replies in channel {channel_id}: {e}")

    def _should_reply(self, msg: Dict, channel_id: str) -> bool:
        try:
            # Basic conditions
            if not all(
                [
                    msg["id"] not in self.replied_messages,
                    msg["author"]["id"] != self.user_id,
                    self._is_recent(msg["timestamp"]),
                    not any(
                        mention.get("bot", False) for mention in msg.get("mentions", [])
                    ),
                ]
            ):
                return False

            # Check if you've replied recently to this channel
            if channel_id in self.last_replies:
                now = datetime.datetime.now(datetime.timezone.utc)
                time_since_reply = (now - self.last_replies[channel_id]).total_seconds()

                # Don't auto-reply if you've replied within the configured window
                your_reply_window = self.config.settings.get(
                    "your_reply_window", 300
                )  # Default 5 minutes
                if time_since_reply < your_reply_window:
                    logger.debug(
                        f"Skipping auto-reply as you replied {time_since_reply:.1f}s ago"
                    )
                    return False

            return True
        except KeyError:
            return False

    def _is_recent(self, timestamp: str) -> bool:
        try:
            msg_time = parser.parse(timestamp)
            delta = datetime.datetime.now(datetime.timezone.utc) - msg_time
            return delta.total_seconds() < self.config.settings["max_message_age"]
        except parser.ParserError as e:
            logger.error(f"Invalid timestamp {timestamp}: {e}")
            return False

    def _send_reply(self, channel_id: str, message: Dict):
        try:
            resp = requests.post(
                f"{self.base_url}/channels/{channel_id}/messages",
                json={"content": self.config.settings["reply_message"]},
                headers=self.headers,
            )
            resp.raise_for_status()
            self.replied_messages.add(message["id"])
            logger.info(f"Replied to message from {message['author']['username']}")
        except requests.RequestException as e:
            logger.error(f"Failed to send reply: {e}")
