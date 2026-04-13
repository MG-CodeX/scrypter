import os
from cryptography.fernet import Fernet, InvalidToken

from file_ops import *

def encrypt_file(args):
    """
    Encrypt a file using a Fernet key and save it as a .enc file.

    Handles file validation, encryption, and overwrite logic.
    """

    file_path = os.path.abspath(args.file)
    key_path = os.path.abspath(args.key)

    if not os.path.isfile(file_path):
        print("File path doesn't exist")
        return 1
    if not os.path.isfile(key_path):
        print("Key path doesn't exist") 
        return 1

    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except OSError:
        print("Unable to access key")
        return 1

    try:
        fernet = Fernet(key)
    except ValueError:
        print("Corrupted or empty key")
        return 1

    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except OSError:
        print("Unable to access file")
        return 1

    encrypted_data = fernet.encrypt(data)
    encrypted_file_path = file_path + ".enc"

    if not os.path.isfile(encrypted_file_path) or args.force:
        status = write_file(encrypted_file_path, encrypted_data)
        if status == 0:
            print("File encrypted successfully")
            return status
        else:
            print("Couldn't create encrypted file")
            return status
    elif confirm_overwrite(encrypted_file_path):
        status = write_file(encrypted_file_path, encrypted_data)
        if status == 0:
            print("File encrypted successfully")
            return status
        else:
            print("Couldn't create encrypted file")
            return status
    else:
        print("Aborting...")
        return 1

def decrypt_file(args):
    """
    Decrypt a .enc file using a Fernet key.

    Can either print the output or write it to a file.
    Handles invalid keys and decoding errors.
    """

    file_path = os.path.abspath(args.file)
    key_path = os.path.abspath(args.key)

    if not os.path.isfile(file_path):
        print("File path doesn't exist")
        return 1
    if not os.path.isfile(key_path):
        print("Key path doesn't exist") 
        return 1

    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except OSError:
        print("Unable to access key")
        return 1

    try:
        fernet = Fernet(key)
    except ValueError:
        print("Corrupted or empty key")
        return 1
    
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except OSError:
        print("Unable to access file")
        return 1

    try:
        decrypted_data = fernet.decrypt(data)
    except InvalidToken:
        print("Invalid key")
        return 1

    if file_path.endswith(".enc"):
        decrypted_file_path = file_path.removesuffix(".enc")
    else:
        print("Unsupported file type")
        return 1

    if not os.path.isfile(decrypted_file_path) or args.force:
        status = write_file(decrypted_file_path, decrypted_data)
        if status == 0:
            print("File decrypted successfully")
            return status
        else:
            print("Couldn't create decrypted file")
            return status
    elif confirm_overwrite(decrypted_file_path):
        status = write_file(decrypted_file_path, decrypted_data)
        if status == 0:
            print("File decrypted successfully")
            return status
        else:
            print("Couldn't create decrypted file")
            return status
    else:
        print("Aborting...")
        return 1

def generate_key(args):
    """
    Generate a new Fernet key and write it to disk.

    Respects overwrite confirmation unless --force is used.
    """

    key_path = os.path.abspath(args.path)
    key = Fernet.generate_key()

    if not os.path.isfile(key_path) or args.force:
        status = write_file(key_path, key)
        if status == 0:
            print("Key file created successfully")
            return status
        else:
            print("Couldn't create key file")
            return status
    elif confirm_overwrite(key_path):
        status = write_file(key_path, key)
        if status == 0:
            print("Key file created successfully")
            return status
        else:
            print("Couldn't create key file")
            return status
    else:
        print("Aborting...")
        return 1
