from libqtile.config import Match

KP = {
    '1': 'KP_End',
    '2': 'KP_Down',
    '3': 'KP_Next',
    '4': 'KP_Left',
    '5': 'KP_Begin',
    '6': 'KP_Right',
    '7': 'KP_Home',
    '8': 'KP_Up',
    '9': 'KP_Prior',
    '0': 'KP_Insert',
}

GROUP_NAMES = [
    {'key_name': KP['1'], 'name': 'CMD1', 'matches': ["Alacritty"]},
    {'key_name': KP['2'], 'name': 'CHAT', 'matches': ["TelegramDesktop", "Pavucontrol"]},
    {'key_name': KP['3'], 'name': 'WWW1', 'matches': ["Brave-browser"]},
    {'key_name': KP['4'], 'name': 'WWW2', 'matches': ["Firefox"]},
    {'key_name': KP['5'], 'name': 'WWW3', 'matches': ["Brave-browser"]},
    {'key_name': KP['6'], 'name': 'WORK', 'matches': ["openfortiGUI", "Slack", "1Password", "Postman"]},
    {'key_name': KP['7'], 'name': 'DEV', 'matches': ["Alacritty", "Code", "jetbrains-pycharm"]},
    {'key_name': KP['8'], 'name': 'DOCS', 'matches': []},
    {'key_name': KP['9'], 'name': 'CMD2', 'matches': ["Alacritty"]},
]
