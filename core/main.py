import time
import subprocess
from core.config import *
from core.discord import *


def is_nvim_running() -> bool:
    try:
        result = subprocess.run(["pgrep", "nvim"], capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.SubprocessError as e:
        logger.error(f"Process check failed: {e}")
        return False


def main():
    config = ConfigManager()
    discord = DiscordManager(config)

    try:
        while True:
            if is_nvim_running():
                discord.set_status(config.settings["status_dnd"])
                discord.check_messages()
            else:
                discord.set_status(config.settings["status_normal"])

            time.sleep(config.settings["check_interval"])

    except KeyboardInterrupt:
        discord.set_status(config.settings["status_normal"])
        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()
