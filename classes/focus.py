import subprocess
from classes.config import *


class FocusEnforcer:
    """Manages website blocking"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.blocked = False

    def block_websites(self):
        if not self.blocked:
            try:
                for site in self.config.blocklist:
                    subprocess.run(
                        [
                            "sudo",
                            "iptables",
                            "-A",
                            "OUTPUT",
                            "-d",
                            site,
                            "-j",
                            "REJECT",
                        ],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                self.blocked = True
                logger.info("Websites blocked successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to block websites: {e}")

    def unblock_websites(self):
        if self.blocked:
            try:
                subprocess.run(
                    ["sudo", "iptables", "-F"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.blocked = False
                logger.info("Websites unblocked")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to unblock websites: {e}")
