import requests

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox

from utils.file_utils import get_path, save_wallets, get_wallets


class DialogAdd(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi(get_path(__file__, "ui/dialog_add.ui"), self)

        self.parent = parent

    def accept(self):
        address = self.inputWallet.text()
        name = self.inputName.text()

        # Check if adress not dublicate
        data = get_wallets()
        if any(wallet["address"] == address for wallet in data["addresses"]):
            QMessageBox.warning(
                self, "Duplicate Address", "The provided address is already in use"
            )
            return

        # Check if address is valid
        url = f"https://blockchain.info/multiaddr?active={address}&n=0"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        except requests.RequestException as e:
            print(f"An error occurred while making a request to the server: {e}")
            QMessageBox.warning(
                self, "Error", "An error occurred while making a request to the server"
            )
            return
        else:
            if not response.json().get("addresses"):
                QMessageBox.warning(
                    self, "Invalid Address", "The provided address is not valid"
                )
                return

        if address:
            wallet = {
                "address": address,
                "name": name,
                "balance": {
                    "final_balance": 0,
                    "n_tx": 0,
                    "total_received": 0,
                    "total_sent": 0,
                    "final_balance_usd": 0,
                },
                "change": 0,
            }

            data = get_wallets()

            data["addresses"].append(wallet)

            save_wallets(data)

            self.parent.refresh_data()
            self.close()
