{
  description = "Python resume builder (pandoc + TeX Live)";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";  # adjust if needed
    pkgs = import nixpkgs { inherit system; };
    tex = pkgs.texlive.combine {
      inherit (pkgs.texlive)
        scheme-basic
        babel
        geometry
        lastpage
        enumitem
        titlesec
        hyperref
        lm
        cm-super;
    };
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        pkgs.python3
        pkgs.pandoc
        tex
      ];
    };
    packages.${system}.default = pkgs.stdenv.mkDerivation {
      pname = "resume";
      version = "1.0";
      src = ./.;
      buildInputs = [
        pkgs.python3
        pkgs.pandoc
        tex
      ];
      # No unpack/configure needed beyond defaults
      buildPhase = ''
        # suggested to fix nix build:
        export HOME=$TMPDIR
        export TEXMFVAR=$TMPDIR/texmf-var
        export TEXMFCONFIG=$TMPDIR/texmf-config
        # Ensure Python can import your module from src
        export PYTHONPATH=$PWD
        python -m resume
      '';
      installPhase = ''
        mkdir -p $out
        cp resumedev.pdf $out/
      '';
    };

    #packages.x86_64-linux.resume = self.packages.${system}.default;
  };
}
