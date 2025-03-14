import time
import subprocess
from core.config import *
from core.discord import *
from core.focus import *


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
    enforcer = FocusEnforcer(config)

    try:
        while True:
            if is_nvim_running():
                discord.set_status(config.settings["status_dnd"])
                discord.check_messages()
                enforcer.block_websites()
                time.sleep(2)
            else:
                discord.set_status(config.settings["status_normal"])
                enforcer.unblock_websites()

            time.sleep(config.settings["check_interval"])

    except KeyboardInterrupt:
        enforcer.unblock_websites()
        discord.set_status(config.settings["status_normal"])
        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()
