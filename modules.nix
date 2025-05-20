{
  config,
  focus-mode,
  lib,
  ...
}: let
  cfg = config.programs.focus-mode;

  # Handle token from either direct string or file
  tokenConfig =
    if cfg.discordTokenFile != ""
    then ''token_file = "${cfg.discordTokenFile}"''
    else ''token = "${cfg.discordToken}"'';

  configFile = ''
    [discord]
    ${tokenConfig}

    [settings]
    focus_indicator = ${"[" + lib.concatStringsSep ", " (map (x: "\"${x}\"") cfg.focus_indicator) + "]"}
    check_interval = ${toString cfg.check_interval}
    status_dnd = "${cfg.status_dnd}"
    status_normal = "${cfg.status_normal}"
    reply_message = "${cfg.reply_message}"
    max_message_age = ${toString cfg.max_message_age}
    your_reply_window = ${toString cfg.your_reply_window}
  '';
in {
  options.programs.focus-mode = {
    enable = lib.mkEnableOption ''
      Focus Mode - Your Coding Sanctuary.
      A smart assistant that protects your coding sessions by managing distractions and communications.
    '';

    discordToken = lib.mkOption {
      type = lib.types.str;
      default = "";
      description = ''
        Get from Discord website (Ctrl+Shift+I -> Network -> Filter messages -> Copy Authorization)
      '';
    };

    discordTokenFile = lib.mkOption {
      type = lib.types.path;
      default = "";
      example = "/run/agenix/discord_token";
      description = ''
        Path to file containing Discord token (useful with agenix for secrets management).
        Takes precedence over discordToken if both are specified.
      '';
    };

    focus_indicator = lib.mkOption {
      type = lib.types.listOf lib.types.str;
      default = "nvim";
      example = [
        "nvim"
        "code"
        ".zathura"
        "gimp"
        "libreoffice"
      ];
      description = ''
        App(s) that indicates focus mode (nvim by default)
      '';
    };

    check_interval = lib.mkOption {
      type = lib.types.str;
      default = "1";
      description = ''
        Seconds between checking DMs
      '';
    };

    status_dnd = lib.mkOption {
      type = lib.types.str;
      default = "dnd";
      description = ''
        Discord status that should be set during DND
      '';
    };

    status_normal = lib.mkOption {
      type = lib.types.str;
      default = "online";
      description = ''
        Discord status that should normally be set.
      '';
    };

    reply_message = lib.mkOption {
      type = lib.types.str;
      default = "I'm focusing right now - I'll reply later! 🚀";
      description = ''
        A reply message that should automatically be sent during focus session.
      '';
    };

    max_message_age = lib.mkOption {
      type = lib.types.str;
      default = "300";
      description = ''
        Check message age before replying to dm.
        Used to prevent spam.
      '';
    };

    your_reply_window = lib.mkOption {
      type = lib.types.str;
      default = "300";
      description = ''
        Don't auto-reply if you've replied within this many seconds.
      '';
    };
  };

  config = lib.mkIf cfg.enable {
    home.packages = [focus-mode];
    xdg.configFile."focus-mode/config.toml".text = configFile;
  };
}
