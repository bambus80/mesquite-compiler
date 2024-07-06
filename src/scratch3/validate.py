keys = [  # TODO: Expand key selection to all keys detectable by Scratch
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'backspace',
    'enter', 'shift', 'up', 'down', 'left', 'right',
]


def is_valid_key(key: str) -> bool:
    return key in keys
