from collections import deque

def is_palindrome(text: str) -> bool:
    """
    Checks if a string is a palindrome using a deque.
    - Case insensitive
    - Ignores all whitespace (including tabs, line breaks)
    """

    filtered = (ch.lower() for ch in text if not ch.isspace())
    dq = deque(filtered)

    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True


if __name__ == "__main__":
    samples = [
        "Тут каток катуТ",
        "A man a plan a canal Panama",
        "Never odd or even",
        "not a palindrome",
        "а роза упала на лапу Азора",
        "  Space   ecapS ",
        "",
        "x",
    ]
    for s in samples:
        print(f"{s!r} -> {is_palindrome(s)}")
