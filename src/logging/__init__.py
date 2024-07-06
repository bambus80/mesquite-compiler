from typing import Optional


# TODO: Better logging of compiler warnings and errors (with specific indexes if possible)
def log_warning(msg: str, line: Optional[str] = None, idx: Optional[int] = None) -> None:
    print(f"\033[38;2;255;165;0mWARNING:\033[0m {msg}")
    if line and idx:
        print(f"    {idx} | {line}")


def log_error(msg: str, line: Optional[str] = None, idx: Optional[int] = None) -> None:
    print(f"\033[31mERROR:\033[0m {msg}")
    if line and idx:
        print(f"    {idx} | {line}")