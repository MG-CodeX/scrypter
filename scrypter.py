import argparse
import sys

from crypto import encrypt_file, decrypt_file, generate_key

def main():
    """
    Parse command-line arguments and execute the selected command.
    """

    parser = argparse.ArgumentParser(
        prog="Scrypter", 
        description=(
            "Scrypter: Encrypt, decrypt files and manage Fernet keys "
            "easily from the command line."
        )
    )

    subparsers = parser.add_subparsers(
            dest="command", 
            required=True
    )

    encrypt_parser = subparsers.add_parser(
            "encrypt", 
            description=(
                "Encrypt a file using a Fernet key. "
                "The output will be saved with a '.enc' extension."
            ), 
            help="Encrypt a file using a key"
    )

    encrypt_parser.add_argument(
            "file", 
            help="Path to the file you want to encrypt"
    )

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

    decrypt_parser.add_argument(
            "file", 
            help="Path to the encrypted file"
    )

    decrypt_parser.add_argument(
            "key", 
            help="Path to the key file used for decryption"
    )

    decrypt_parser.add_argument(
        "-f", "--force", 
        action="store_true", 
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

    key_parser.add_argument(
            "path", 
            help="Path to save the generated key file"
    )

    key_parser.add_argument(
        "-f", "--force", 
        action="store_true", 
        help="Overwrite existing key file without prompting"
    )
    key_parser.set_defaults(func=generate_key)

    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("Operation Cancelled")
        sys.exit(1)
