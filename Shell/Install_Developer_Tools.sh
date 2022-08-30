# Shell script to automate new computer set up for developers using Mac

# specify directory to install
cask_args appdir: "/Applications"

# install packages + some apps
tap "homebrew/bundle"
tap "homebrew/cask"
tap "homebrew/core"
tap "schniz/tap"
brew "python"
brew "git"
brew "zsh"
brew "zsh-autosuggestions"
brew "zsh-completions"
brew "zsh-syntax-highlighting"
brew "fnm"

# Casks
cask "postman"
cask "visual-studio-code"
cask "google-chrome"
cask "zoom"
cask "slack"
cast "docker"