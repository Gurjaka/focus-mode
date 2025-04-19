{
  lib,
  buildPythonApplication,
  setuptools,
  requests,
  python-dateutil,
  tomli,
}:
buildPythonApplication rec {
  pname = "focus-mode";
  version = "0.0.1+${src.shortRev or "dev"}";
  pyproject = true;

  src = ./.;

  build-system = [
    setuptools
  ];

  dependencies = [
    requests
    python-dateutil
    tomli
  ];

  meta = {
    changelog = "https://github.com/Gurjaka/focus-mode";
    homepage = "https://github.com/Gurjaka/focus-mode";
    description = "A productivity tool that automatically sets your Discord status to 'Do Not Disturb' when Neovim is active, sends auto-replies to incoming messages, and blocks distracting websites to maintain focus during coding sessions.";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [
      gurjaka
    ];
  };
}
