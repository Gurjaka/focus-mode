{
  description = "Python development flake template";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    supportedSystems = ["x86_64-linux"];
    forAllSystems = function:
      nixpkgs.lib.genAttrs supportedSystems (
        system: function nixpkgs.legacyPackages.${system}
      );
  in {
    formatter = forAllSystems (pkgs: pkgs.alejandra);

    packages = forAllSystems (pkgs: {
      default = self.packages.${pkgs.system}.focus-mode;

      focus-mode = pkgs.python3Packages.callPackage ./default.nix {};
    });

    devShells = forAllSystems (
      pkgs: let
        python-deps = ps:
          with ps; [
            pip
            requests
            tomli
            python-dateutil
          ];
      in {
        default =
          pkgs.mkShell
          {
            packages = with pkgs; [
              (python3.withPackages python-deps)
              black
            ];
          };
      }
    );
  };
}
