import logging
import tomli
from typing import Dict
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "focus-mode"
LOG_DIR = Path.home() / ".local" / "log"
LOG_FILE = LOG_DIR / "focus-mode.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE)],
)
logger = logging.getLogger("FocusMode")


class ConfigManager:
    """Handles TOML configuration file"""

    _default_config = """\
[discord]
token = ""  # Get from Discord website (Ctrl+Shift+I -> Network -> Filter messages -> Copy Authorization)

[settings]
focus_indicator = "nvim"  # App that indicates focus mode (nvim by default)
check_interval = 1  # Seconds between checks
status_dnd = "dnd"
status_normal = "online"
reply_message = "I'm focusing right now - I'll reply later! 🚀"
max_message_age = 300  # 5 minutes in seconds
your_reply_window = 300  # Don't auto-reply if you've replied within this many seconds
    """

    def __init__(self):
        self.config_path = CONFIG_DIR / "config.toml"
        self._ensure_config()
        self.config = self._load_config()

    def _ensure_config(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self.config_path.write_text(self._default_config)
            self.config_path.chmod(0o600)
            logger.info(f"Created default config at {self.config_path}")
            raise SystemExit("Please configure your Discord token and settings")

    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, "rb") as f:
                config = tomli.load(f)

            if not config["discord"].get("token"):
                raise ValueError("Discord token missing in config")

            return config
        except (tomli.TOMLDecodeError, KeyError) as e:
            logger.error(f"Invalid config: {e}")
            raise SystemExit(1) from None

    @property
    def discord_token(self) -> str:
        return self.config["discord"]["token"]

    @property
    def blocklist(self) -> list:
        return self.config["blocklist"]["websites"]

    @property
    def settings(self) -> Dict:
        return self.config["settings"]

    @property
    def focus_indicator(self) -> str:
        return self.config["settings"]["focus_indicator"]
