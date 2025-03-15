<div align="center">

## 🔒 Focus Mode - Your Coding Sanctuary 🚀

![GitHub Repo stars](https://img.shields.io/github/stars/Gurjaka/focus-mode?style=for-the-badge&labelColor=2e3440&color=5e81ac) ![GitHub last commit](https://img.shields.io/github/last-commit/Gurjaka/focus-mode?style=for-the-badge&labelColor=2e3440&color=5e81ac) ![GitHub repo size](https://img.shields.io/github/repo-size/Gurjaka/focus-mode?style=for-the-badge&labelColor=2e3440&color=5e81ac)

**Transform your workflow with automated focus enforcement**  
*A smart assistant that protects your coding sessions by managing distractions and communications*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!--[![PyPI Version](https://img.shields.io/pypi/v/focus-mode?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/focus-mode/)-->
<!--[![Build Status](https://img.shields.io/github/actions/workflow/status/Gurjaka/focus-mode/build.yml?logo=github)](https://github.com/Gurjaka/focus-mode/actions)-->

</div>

## ✨ Features That Supercharge Your Productivity

- 🛡️ **Auto-DND Mode**  
  _Instant Discord status updates when Neovim launches_
- 🤖 **Smart Auto-Responder**  
  _Polite replies to DMs without breaking flow_
- ⏱️ **Intelligent Cooldown**  
  _Prevents spam with per-channel reply limits_

## 🚀 Getting Started in 60 Seconds

### Prerequisites
- Python 3.11+
- Discord account

## 📥 Installation

### NixOS or Home Manager

1. Add the following to your `flake.nix`:

    ```nix
    inputs = {
      focus-mode.url = "github:Gurjaka/focus-mode";
      ...
    }
    ```

2. Then, add Zen Browser to your packages:
    > For system wide installation in *configuration.nix*
    ```nix
    environment.systemPackages = with pkgs; [
      inputs.focus-mode.packages."${system}".default
    ];
    ```

    > For user level installation in *home.nix*
    ```nix
    home.packages = with pkgs; [
      inputs.focus-mode.packages."${system}".default
    ];
    ```

### Traditional distros

    # Install with pip
    pip install focus-mode

    # Or get the bleeding edge version
    pip install git+https://github.com/Gurjaka/focus-mode.git

### Basic Usage
```bash
focus-mode
```

## 🛠️ Configuration Made Simple

edit `~/.config/focus-mode/config.toml`:
```toml
[discord]
token = "your_token_here"  # 🔑 Get from Discord client (Ctrl+Shift+I -> Filter science -> Copy Authorization)
[settings]
focus_indicator = "nvim"  # App that indicates focus mode (nvim by default)
check_interval = 1  # Seconds between checks
status_dnd = "dnd"
status_normal = "online"
reply_message = "I'm coding right now - I'll reply later! 🚀"
max_message_age = 300  # 5 minutes in seconds
your_reply_window = 300 # Don't auto-reply if you've replied within this many seconds
```


## 🌟 Why Developers Love This

*"Finally stopped getting distracted by Discord DMs during coding sessions!" - Jane D. (Python Dev)*

*"The auto-responder saved me from endless DM distractions" - Mike T. (Open Source Maintainer)*

## 🛣️ Roadmap

- [ ] Website blocker integration
- [ ] Browser extension integration
- [ ] Slack/Teams support
- [ ] Focus time analytics
- [ ] Mobile app companion

<!--## 🤝 Contributing-->
<!---->
<!--We welcome code warriors! Please read our:-->
<!--- [Contribution Guidelines](CONTRIBUTING.md)-->
<!--- [Code of Conduct](CODE_OF_CONDUCT.md)-->
<!--- [Security Policy](SECURITY.md)-->

## 📜 License

MIT Licensed - See [LICENSE](LICENSE) for details

---

**⚠️ Important Note:**  
This project is not affiliated with Discord. Use of Discord tokens may violate Discord's Terms of Service - proceed at your own risk.

Made with ❤️  by Gurjaka
