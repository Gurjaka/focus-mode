<div align="center">

## 🔒 Focus Mode - Your Coding Sanctuary 🚀

<img alt="Focus Mode Icon" src="assets/logo.svg" width="200px"/>

**Transform your workflow with automated focus enforcement**  
*A smart assistant that protects your coding sessions by managing distractions and communications*

![GitHub Repo stars](https://img.shields.io/github/stars/Gurjaka/focus-mode?style=for-the-badge&labelColor=2e3440&color=5e81ac) ![GitHub last commit](https://img.shields.io/github/last-commit/Gurjaka/focus-mode?style=for-the-badge&labelColor=2e3440&color=5e81ac) ![GitHub repo size](https://img.shields.io/github/repo-size/Gurjaka/focus-mode?style=for-the-badge&labelColor=2e3440&color=5e81ac)

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

### Flake based systems
1. Add the input to your flake.nix:
   ```nix
   inputs = {
     focus-mode.url = "github:Gurjaka/focus-mode";
     ...
   };
   ```
   
#### NixOS

1. Then, add Focus-Mode to your packages:
    ```nix
    environment.systemPackages = with pkgs; [
      inputs.focus-mode.packages."${system}".default
    ];
    ```

2. For configuration check following [🛠️ Instructions](#️-configuration-made-simple)

#### Home Manager

1. Expose your focus-mode input to homeManagerModules:

   ```nix
   outputs = { self, nixpkgs, home-manager, focus-mode, ... }: {
     homeConfigurations.your-user = home-manager.lib.homeManagerConfiguration {
       ...
       modules = [
         focus-mode.homeManagerModules.default
         ./home.nix
       ];
     };
   };
   ```

2. Enable and configure in your home.nix:

   ```nix
   programs.focus-mode = {
     enable = true;

     # Use either token OR token file (tokenFile takes precedence)
     discordToken = "your_token_here"; # ⚠️ Do not share this for your account's safety!
     
     # In case you use Agenix encryption, this is safer way
     # discordTokenFile = "/run/agenix/discord_token";

     focus_indicator = [
       "nvim"
     ];
     check_interval = "1";
     status_dnd = "dnd";
     status_normal = "idle";
     reply_message = "I'm trying to focus now - I'll reply later! 🚀";
     max_message_age = "300";
     your_reply_window = "300";
   };
   ```

3. Apply the configuration:

   ```sh
   home-manager switch
   ```

### Basic Usage

```bash
focus-mode
```

## 🛠️ Configuration Made Simple

If you're not using Home Manager, edit `~/.config/focus-mode/config.toml` manually:

```toml
[discord]
token = "your_token_here"  # 🔑 Get from Discord client (Ctrl+Shift+I -> Network -> Filter messages -> Copy Authorization)

[settings]
focus_indicator = "nvim"  # App that indicates focus mode
check_interval = 1
status_dnd = "dnd"
status_normal = "online"
reply_message = "I'm coding right now - I'll reply later! 🚀"
max_message_age = 300
your_reply_window = 300
```

## 🌟 Why Developers Love This

> "Finally stopped getting distracted by Discord DMs during coding sessions!"
> — Jane D. (Python Dev)

> "The auto-responder saved me from endless DM distractions"
> — Mike T. (Open Source Maintainer)

## 🛣️ Roadmap

* [ ] Website blocker integration
* [ ] Browser extension integration
* [ ] Slack/Teams support
* [ ] Focus time analytics
* [ ] Mobile app companion

## 📜 License

MIT Licensed – See [LICENSE](LICENSE) for details

---

⚠️ **Important Note:**
This project is not affiliated with Discord. Use of Discord tokens may violate Discord's Terms of Service – proceed at your own risk.

Made with ❤️ by Gurjaka
