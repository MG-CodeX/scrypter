import os

def confirm_overwrite(path):
    """
    Ask the user whether to overwrite an existing file.

    Loops until the user enters 'y' or 'n'.

    Returns:
        bool: True if overwrite is confirmed, False otherwise.
    """

    while True:
        choice = input(f"{path} already exists, overwrite? (y/n): ")
        match choice.lower():
            case "y": return True
            case "n": return False
            case _: print("Invalid choice")

def write_file(path, data):
    """
    Write binary data to a file.

    Returns:
        int: 0 on success, 1 on OS error.
    """

    try:
        with open(path, "wb") as f:
            f.write(data)
        return 0
    except OSError:
        return 1
