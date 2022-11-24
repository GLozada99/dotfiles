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

autoload -Uz compinit
compinit

# Source Aliases
[[ -f ~/.aliasrc ]] && . ~/.aliasrc

# Moving through terminal
bindkey '^[[1;5D' backward-word
bindkey '^[[1;5C' forward-word

# Pluggins
source /home/glozada/.local/bin/zsh-z.plugin.zsh
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors "${(@s.:.)LS_COLORS}"
plugins=(git z sudo zsh-completions)


# Start Starship
eval "$(starship init zsh)"
# End of lines added by compinstall

welc "Welcome Gus"
