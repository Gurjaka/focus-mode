## 🔒 Focus Mode - Your Coding Sanctuary 🚀

**Transform your workflow with automated focus enforcement**  
*A smart assistant that protects your coding sessions by managing distractions and communications*

<!--[![PyPI Version](https://img.shields.io/pypi/v/focus-mode?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/focus-mode/)-->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!--[![Build Status](https://img.shields.io/github/actions/workflow/status/Gurjaka/focus-mode/build.yml?logo=github)](https://github.com/Gurjaka/focus-mode/actions)-->

## ✨ Features That Supercharge Your Productivity

- 🛡️ **Auto-DND Mode**  
  _Instant Discord status updates when Neovim launches_
- 🤖 **Smart Auto-Responder**  
  _Polite replies to DMs without breaking flow_
- 🚫 **Website Blocker**  
  _Ban time-sink sites during work sessions_
- ⏱️ **Intelligent Cooldown**  
  _Prevents spam with per-channel reply limits_

## 🚀 Getting Started in 60 Seconds

### Prerequisites
- Python 3.11+
- Discord account

### Installation
```bash
# Install with pip
pip install focus-mode

# Or get the bleeding edge version
pip install git+https://github.com/Gurjaka/focus-mode.git
```

### Basic Usage
```bash
focus-mode
```

## 🛠️ Configuration Made Simple

edit `~/.config/focus-mode/config.toml`:
```toml
[discord]
token = "your_token_here"  # 🔑 Get from Discord Developer Portal

[blocklist]
websites = [
    "reddit.com", 
    "twitter.com",
    "youtube.com"
]

[settings]
check_interval = 5  # ⏱️ Seconds between checks
reply_message = "👨💻 Deep in code - I'll respond later!" 
```


## 🌟 Why Developers Love This

_"Finally cured my Twitter addiction during coding sessions!"_ - Jane D. (Python Dev)  

_"The auto-responder saved me from endless DM distractions"_ - Mike T. (Open Source Maintainer)

## 🛣️ Roadmap

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

Made with ❤️ by Gurjaka | [Buy Me Coffee ☕](https://buymeacoffee.com/yourprofile)
