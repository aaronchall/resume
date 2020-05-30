{ pkgs ? import <nixpkgs> {} }:
with pkgs;
  mkShell {
    buildInputs = [
      python39
      texlive.combined.scheme-full
      vim
      which
      entr
      ncurses # for tput
      tree
    ];
    shellHook = ''
      if [ -f "$HOME/.bashrc" ]; then 
          source "$HOME/.bashrc";
      else 
          source /etc/bashrc;
      fi
    '';
  }
