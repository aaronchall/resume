{ pkgs ? import <nixpkgs> {} }:
with pkgs;
  mkShell {
    buildInputs = [
      texlive.combined.scheme-full
      vim
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
