import logging
import tomli
from typing import Dict, Optional
from pathlib import Path
from typing import Union

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
# token_file = ""  # Alternative: path to file containing token (for agenix integration)

[settings]
focus_indicator = ["nvim"]  # App(s) that indicates focus mode (nvim by default)
check_interval = 1  # Seconds between checks
status_dnd = "dnd"
status_normal = "online"
reply_message = "I'm trying to focus now - I'll reply later! 🚀"
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

            # Make sure discord section exists
            if "discord" not in config:
                raise KeyError("Missing [discord] section in config")

            # Validate token configuration
            self._validate_token_config(config["discord"])

            return config
        except (tomli.TOMLDecodeError, KeyError) as e:
            logger.error(f"Invalid config: {e}")
            raise SystemExit(1) from None

    def _validate_token_config(self, discord_config: Dict):
        """Validate that token configuration is valid"""
        has_token = bool(discord_config.get("token", ""))
        has_token_file = bool(discord_config.get("token_file", ""))

        if not has_token and not has_token_file:
            raise ValueError("No Discord token or token_file specified in config")

        # If token_file is specified, check that it exists and is readable
        if has_token_file:
            token_file = Path(discord_config["token_file"])
            if not token_file.exists():
                logger.warning(f"Token file does not exist: {token_file}")
                if not has_token:
                    raise ValueError(
                        f"Token file {token_file} does not exist and no direct token provided"
                    )

    @property
    def discord_token(self) -> str:
        """Get Discord token, preferring token_file if available"""
        discord_config = self.config["discord"]

        # Check for token_file first
        token_file_path = discord_config.get("token_file", "")
        if token_file_path:
            try:
                token_file = Path(token_file_path)
                if token_file.exists():
                    logger.debug(f"Reading token from file: {token_file}")
                    return token_file.read_text().strip()
                else:
                    logger.warning(f"Token file not found: {token_file}")
            except Exception as e:
                logger.error(f"Error reading token file: {e}")

        # Fall back to direct token
        return discord_config.get("token", "")

    @property
    def settings(self) -> Dict:
        return self.config["settings"]

    @property
    def focus_indicator(self) -> Union[str, list]:
        return self.config["settings"]["focus_indicator"]
