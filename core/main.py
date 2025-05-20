import threading
import time
import subprocess
from core.config import *
from core.discord import *


def is_indicator_running(indicator) -> bool:
    if indicator == None:
        logger.error(f"Focus indicator not found! Exitting...")

    for i in indicator:
        try:
            result = subprocess.run(["pgrep", f"{i}"], capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except subprocess.SubprocessError as e:
            logger.error(f"Process check failed for {i}: {e}")
            return False

    return False


def main():
    config = ConfigManager()
    discord = DiscordManager(config)
    indicator = config.focus_indicator

    if not isinstance(indicator, list) or not all(
        isinstance(i, str) for i in indicator
    ):
        raise TypeError(
            "focus_indicator must be a list of strings, e.g. ['nvim', 'zathura']"
        )

    def dm_check_loop():
        while True:
            if discord.current_status == config.settings["status_dnd"]:
                discord.check_messages()
            time.sleep(config.settings["check_interval"])

    threading.Thread(target=dm_check_loop, daemon=True).start()

    try:
        while True:
            if is_indicator_running(indicator):
                discord.set_status(config.settings["status_dnd"])
            else:
                discord.set_status(config.settings["status_normal"])

            time.sleep(config.settings["check_interval"])

    except KeyboardInterrupt:
        discord.set_status(config.settings["status_normal"])
        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()
