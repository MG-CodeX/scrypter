from cryptography.fernet import Fernet, InvalidToken
import argparse
import os
import sys

def confirm_overwrite(path):
    """
    Prompt the user to confirm overwriting an existing file.

    Args:
        path (str): The path of the existing file.

    Returns:
        bool: True if the user confirms overwrite, False otherwise.
    """

    while True:
        choice = input(f"{path} already exists, overwrite? (y/n): ")
        match choice.lower():
            case "y": return True
            case "n": return False
            case _: print("Invalid choice")

def create_encrypted_file(path, data):
    """
    Write encrypted data to a file.

    Args:
        path (str): Path where the encrypted file will be created.
        data (bytes): Encrypted data to write.

    Raises:
        SystemExit: If the file cannot be created due to an OS error.
    """

    try:
        with open(path, "wb") as f:
            f.write(data)
        print("File encrypted successfully")
        sys.exit(0)
    except OSError:
        print("Unable to create encrypted file")
        sys.exit(1)

def create_decrypted_file(path, data):
    """
    Write decrypted data to a file.

    Args:
        path (str): Path where the decrypted file will be created.
        data (bytes): Decrypted data to write.

    Raises:
        SystemExit: If the file cannot be created due to an OS error.
    """

    try:
        with open(path, "wb") as f:
            f.write(data)
        print("File decrypted successfully")
        sys.exit(0)
    except OSError:
        print("Unable to create decrypted file")
        sys.exit(1)

def create_key_file(path, key):
    """
    Write a Fernet key to a file.

    Args:
        path (str): Path where the key file will be created.
        key (bytes): Fernet key to write.

    Raises:
        SystemExit: If the key file cannot be created due to an OS error.
    """

    try:
        with open(path, "wb") as f:
            f.write(key)
        print("Key created successfully")
        sys.exit(0)
    except OSError:
        print("Unable to create key file")
        sys.exit(1)

def encrypt_file(args):
    """
    Encrypt a file using a Fernet key.

    Prompts the user if the encrypted file already exists unless --force is used.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            file (str): Path to the file to encrypt.
            key (str): Path to the key file.
            force (bool): Whether to overwrite existing files without prompting.

    Raises:
        SystemExit: If the file or key path doesn't exist, or if encryption fails.
    """

    file_path = os.path.abspath(args.file)
    key_path = os.path.abspath(args.key)

    if not os.path.exists(file_path):
        print("File path doesn't exist")
        sys.exit(1)
    if not os.path.exists(key_path):
        print("Key path doesn't exist") 
        sys.exit(1)

    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except OSError:
        print("Unable to access key")
        sys.exit(1)
    
    try:
        fernet = Fernet(key)
    except ValueError:
        print("Corrupted or empty key")
        sys.exit(1)

    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except OSError:
        print("Unable to access file")
        sys.exit(1)

    encrypted_data = fernet.encrypt(data)
    encrypted_file_path = file_path + ".enc"

    if not os.path.exists(encrypted_file_path) or args.force:
        create_encrypted_file(encrypted_file_path, encrypted_data)
    elif confirm_overwrite(encrypted_file_path):
        create_encrypted_file(encrypted_file_path, encrypted_data)
    else:
        print("Aborting...")
        sys.exit(1)

def decrypt_file(args):
    """
    Decrypt an encrypted file using a Fernet key.

    Prompts the user if the decrypted file already exists unless --force is used.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            file (str): Path to the encrypted file.
            key (str): Path to the key file.
            force (bool): Whether to overwrite existing files without prompting.

    Raises:
        SystemExit: If the file or key path doesn't exist, if the key is invalid,
                    or if decryption fails.
    """

    file_path = os.path.abspath(args.file)
    key_path = os.path.abspath(args.key)

    if not os.path.exists(file_path):
        print("File path doesn't exist")
        sys.exit(1)
    if not os.path.exists(key_path):
        print("Key path doesn't exist") 
        sys.exit(1)

    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except OSError:
        print("Unable to access key")
        sys.exit(1)

    try:
        fernet = Fernet(key)
    except ValueError:
        print("Corrupted or empty key")
        sys.exit(1)

    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except OSError:
        print("Unable to access file")
        sys.exit(1)

    try:
        decrypted_data = fernet.decrypt(data)
    except InvalidToken:
        print("Invalid key")
        sys.exit(1)
        
    if file_path.endswith(".enc"):
        decrypted_file_path = file_path.removesuffix(".enc")
    else:
        print("Unsupported file type")
        sys.exit(1)

    if not os.path.exists(decrypted_file_path) or args.force:
        create_decrypted_file(decrypted_file_path, decrypted_data)
    elif confirm_overwrite(decrypted_file_path):
        create_decrypted_file(decrypted_file_path, decrypted_data)
    else:
        print("Aborting...")
        sys.exit(1)

def generate_key(args):
    """
    Generate a new Fernet key and write it to a file.

    Prompts the user if the key file already exists unless --force is used.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            path (str): Path to the key file to create.
            force (bool): Whether to overwrite existing key files without prompting.

    Raises:
        SystemExit: If the key file cannot be created or the operation is aborted.
    """

    key_path = os.path.abspath(args.path)
    key = Fernet.generate_key()

    if not os.path.exists(key_path) or args.force:
        create_key_file(key_path, key)
    elif confirm_overwrite(key_path):
        create_key_file(key_path, key)
    else:
        print("Aborting...")
        sys.exit(1)

def main():
    """
    Parse command-line arguments and dispatch to the appropriate function.

    Subcommands supported:
        - encrypt: Encrypt a file with a key.
        - decrypt: Decrypt a file with a key.
        - gen_key: Generate a new Fernet key.

    Raises:
        SystemExit: If the arguments are invalid or the user interrupts the program.
    """

    parser = argparse.ArgumentParser(
        prog="Scrypter", 
        description=(
            "Scrypter: Encrypt, decrypt files and manage Fernet keys "
            "easily from the command line."
        )
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    encrypt_parser = subparsers.add_parser(
        "encrypt", 
        description=(
            "Encrypt a file using a Fernet key. "
            "The output will be saved with a '.enc' extension."
        ), 
        help="Encrypt a file using a key"
    )
    encrypt_parser.add_argument("file", help="Path to the file you want to encrypt")
    encrypt_parser.add_argument("key", help="Path to the key file used for encryption")
    encrypt_parser.add_argument(
        "-f", "--force", action="store_true", 
        help="Overwrite existing encrypted file without prompting"
    )
    encrypt_parser.set_defaults(func=encrypt_file)

    decrypt_parser = subparsers.add_parser(
        "decrypt", 
        description=(
            "Decrypt an encrypted file using a Fernet key. "
            "The '.enc' suffix will be removed from the output file."
        ), 
        help="Decrypt a file using a key"
    )
    decrypt_parser.add_argument("file", help="Path to the encrypted file")
    decrypt_parser.add_argument("key", help="Path to the key file used for decryption")
    decrypt_parser.add_argument(
        "-f", "--force", action="store_true", 
        help="Overwrite existing decrypted file without prompting"
    )
    decrypt_parser.set_defaults(func=decrypt_file)

    key_parser = subparsers.add_parser(
        "gen_key", 
        description=(
            "Generate a new Fernet key and save it to a file. "
            "Use --force to overwrite existing key files."
        ), 
        help="Generate a new Fernet key"
    )
    key_parser.add_argument("path", help="Path to save the generated key file")
    key_parser.add_argument(
        "-f", "--force", action="store_true", 
        help="Overwrite existing key file without prompting"
    )
    key_parser.set_defaults(func=generate_key)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Operation Cancelled")
        sys.exit(1)
