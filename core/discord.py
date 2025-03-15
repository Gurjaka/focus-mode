import datetime
import requests
import os
import json
from dateutil import parser
from typing import Dict, Set
from core.config import *


class DiscordManager:
    """Handles Discord status and messaging with improved reply logic"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.base_url = "https://discord.com/api/v9"
        self.headers = {
            "Authorization": config.discord_token,
            "Content-Type": "application/json",
        }
        self.user_id = self._get_user_id()
        self.current_status = None

        # Track replied conversations, not just messages
        self.replied_channels: Set[str] = set()

        # Load persistent state if available
        self.state_file = CONFIG_DIR / "discord_state.json"
        self._load_state()

        self.last_replies: Dict[str, datetime.datetime] = {}

    def _get_user_id(self) -> str:
        try:
            resp = requests.get(f"{self.base_url}/users/@me", headers=self.headers)
            resp.raise_for_status()
            return resp.json()["id"]
        except requests.RequestException as e:
            logger.error(f"Failed to get user ID: {e}")
            raise SystemExit(1) from None

    def _load_state(self):
        """Load persistent state from file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, "r") as f:
                    state = json.load(f)
                    self.replied_channels = set(state.get("replied_channels", []))
                    logger.debug(
                        f"Loaded state with {len(self.replied_channels)} replied channels"
                    )
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            self.replied_channels = set()

    def _save_state(self):
        """Save state to file for persistence"""
        try:
            with open(self.state_file, "w") as f:
                json.dump({"replied_channels": list(self.replied_channels)}, f)
            logger.debug("Saved Discord state")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

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
        """Check for new messages and reply if needed"""
        try:
            # Reset replied channels if no longer in focus mode
            if self.current_status != "dnd":
                self._reset_replied_channels()
                return

            channels = requests.get(
                f"{self.base_url}/users/@me/channels", headers=self.headers
            ).json()

            for channel in channels:
                if channel.get("type") == 1:  # DM channel
                    self._process_channel(channel["id"])

            # Save state after processing
            self._save_state()
        except requests.RequestException as e:
            logger.error(f"Message check failed: {e}")

    def _reset_replied_channels(self):
        """Reset the replied channels when exiting focus mode"""
        if self.replied_channels:
            logger.info(f"Resetting {len(self.replied_channels)} replied channels")
            self.replied_channels.clear()
            self._save_state()

    def _process_channel(self, channel_id: str):
        """Process a single channel to check for messages needing replies"""
        try:
            # Already replied to this channel during this focus session
            if channel_id in self.replied_channels:
                logger.debug(
                    f"Already replied to channel {channel_id} during this focus session"
                )
                return

            # Check if you've replied recently in this channel
            self._update_your_last_reply(channel_id)

            messages = requests.get(
                f"{self.base_url}/channels/{channel_id}/messages?limit=5",
                headers=self.headers,
            ).json()

            # Find the most recent message that needs a reply
            for msg in messages:
                if self._should_reply(msg, channel_id):
                    self._send_reply(channel_id, msg)
                    # Add to replied channels after successful reply
                    self.replied_channels.add(channel_id)
                    logger.info(
                        f"Marked channel {channel_id} as replied for this focus session"
                    )
                    break  # Only reply once per channel check
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
        """Determine if a message should receive an auto-reply"""
        try:
            # Basic conditions
            if not all(
                [
                    msg["author"]["id"] != self.user_id,
                    self._is_recent(msg["timestamp"]),
                    not any(
                        mention.get("bot", False) for mention in msg.get("mentions", [])
                    ),
                ]
            ):
                return False

            # Check if you've replied recently to this channel outside of focus mode
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
        """Check if a message is recent enough to warrant a reply"""
        try:
            msg_time = parser.parse(timestamp)
            delta = datetime.datetime.now(datetime.timezone.utc) - msg_time
            return delta.total_seconds() < self.config.settings["max_message_age"]
        except parser.ParserError as e:
            logger.error(f"Invalid timestamp {timestamp}: {e}")
            return False

    def _send_reply(self, channel_id: str, message: Dict):
        """Send a reply to a message"""
        try:
            resp = requests.post(
                f"{self.base_url}/channels/{channel_id}/messages",
                json={"content": self.config.settings["reply_message"]},
                headers=self.headers,
            )
            resp.raise_for_status()
            logger.info(f"Replied to message from {message['author']['username']}")
        except requests.RequestException as e:
            logger.error(f"Failed to send reply: {e}")
