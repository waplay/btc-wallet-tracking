import json
import os


def get_path(file, relative_path):
    current_file_path = os.path.abspath(file)
    current_directory = os.path.dirname(current_file_path)
    return os.path.join(current_directory, relative_path)


def get_wallets():
    data_dir = os.environ.get("SNAP_USER_DATA", os.path.join(os.getcwd(), "src"))
    file_path = os.path.join(data_dir, "wallets.json")
    with open(file_path, "r") as f:
        return json.load(f)


def save_wallets(data):
    data_dir = os.environ.get("SNAP_USER_DATA", os.path.join(os.getcwd(), "src"))
    file_path = os.path.join(data_dir, "wallets.json")
    with open(file_path, "w") as f:
        json.dump(data, f)
