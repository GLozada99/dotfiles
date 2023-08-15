# Lines configured by zsh-newuser-install
setopt autocd extendedglob notify
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/glozada/.zshrc'

# Setting history file
HISTSIZE=12000
SAVEHIST=10000
HISTFILE=~/.histfile
setopt INC_APPEND_HISTORY
setopt SHARE_HISTORY
unsetopt nomatch
autoload -Uz compinit
compinit

# Source Aliases
[[ -f ~/.aliasrc ]] && . ~/.aliasrc

# Moving through terminal
bindkey '^[[1;5D' backward-word
bindkey '^[[1;5C' forward-word

# Pluggins
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors "${(@s.:.)LS_COLORS}"
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
plugins=(git z sudo zsh-completions osx)


# Start Starship
eval "$(starship init zsh)"
# End of lines added by compinstall

my-backward-delete-word() {
    local WORDCHARS=${WORDCHARS/\//}
    zle backward-delete-word
}
zle -N my-backward-delete-word
bindkey '^W' my-backward-delete-word

welc "Welcome Gus"

fpath+=~/.zfunc

source_files
