import threading
import time
import subprocess
from core.config import *
from core.discord import *


def is_indicator_running() -> bool:
    config = ConfigManager()
    try:
        indicator = config.focus_indicator
        result = subprocess.run(
            ["pgrep", f"{indicator}"], capture_output=True, text=True
        )
        return result.returncode == 0
    except subprocess.SubprocessError as e:
        logger.error(f"Process check failed: {e}")
        return False


def main():
    config = ConfigManager()
    discord = DiscordManager(config)

    def dm_check_loop():
        while True:
            if discord.current_status == config.settings["status_dnd"]:
                discord.check_messages()
            time.sleep(config.settings["check_interval"])

    threading.Thread(target=dm_check_loop, daemon=True).start()
    try:
        while True:
            if is_indicator_running():
                discord.set_status(config.settings["status_dnd"])
            else:
                discord.set_status(config.settings["status_normal"])

            time.sleep(config.settings["check_interval"])

    except KeyboardInterrupt:
        discord.set_status(config.settings["status_normal"])
        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()
