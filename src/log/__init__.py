def log_warning(msg: str) -> None:
    print(f"\033[38;2;255;165;0mWARNING:\033[0m {msg}")


def log_error(msg: str) -> None:
    print(f"\033[31mERROR:\033[0m {msg}")