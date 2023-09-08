import json
import requests

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox

from utils.file_utils import get_path, get_path_wallets


class DialogAdd(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi(get_path(__file__, "ui/dialog_add.ui"), self)

        self.parent = parent

    def accept(self):
        address = self.inputWallet.text()
        name = self.inputName.text()

        # Check if address is valid
        url = f"https://blockchain.info/multiaddr?active={address}&n=0"
        response = requests.get(url)
        if not response.json().get("addresses"):
            QMessageBox.warning(self, "Invalid Address", "The provided address is not valid")
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
                    "final_balance_usd": 0
                },
                "change": 0
            }

            with open(get_path_wallets(__file__), "r") as f:
                data = json.load(f)

            data["addresses"].append(wallet)

            with open(get_path_wallets(__file__), "w") as f:
                json.dump(data, f)

            self.parent.refresh_data()
            self.close()