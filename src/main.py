#!/usr/bin/env python3

# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# pip freeze > requirements.txt

import datetime
import os
import shutil
import sys
import requests
import time

# Need for snap
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView, QAction
from PyQt5.QtGui import QIcon

from utils.file_utils import get_path, save_wallets, get_wallets
from dialog_about import AboutDialog
from dialog_add import DialogAdd
from dialog_donate import DonateDialog
from table_model import WalletsTableModel

SATOSHI = 100000000

# Need for snap.
if "SNAP" in os.environ:
    snap_data_file = os.path.join(os.environ["SNAP_USER_DATA"], "wallets.json")
    snap_file = os.path.join(os.environ["SNAP"], "wallets.json")

    if not os.path.exists(snap_data_file):
        shutil.copyfile(snap_file, snap_data_file)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_path(__file__, "ui/main.ui"), self)
        self.setWindowIcon(QIcon(get_path(__file__, "images/logo.png")))
        self.btnAdd.clicked.connect(self.add_wallet)
        self.btnDelete.clicked.connect(self.delete_wallet)
        self.btnDelete.setEnabled(False)
        self.btnRefresh.clicked.connect(self.refresh_data)

        self.data = None

        self.update_wallet_data()

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.clicked.connect(self.show_details)

        # Create WalletsTableModel instance with data and headers
        self.model = WalletsTableModel(self.data["addresses"])

        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().sectionClicked.connect(self.sortByColumn)

        about = QAction("About", self)
        donate = QAction("Donate", self)
        about.triggered.connect(self.showAboutDialog)
        donate.triggered.connect(self.showDonateDialog)
        self.menubar.addAction(about)
        self.menubar.addAction(donate)

    def showAboutDialog(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def showDonateDialog(self):
        dialog = DonateDialog(self)
        dialog.exec_()

    def refresh_data(self):
        self.tableView.clearSelection()
        self.show_details(reset=True)

        self.update_wallet_data()
        self.model.refresh(self.data["addresses"])

    def update_wallet_data(self):
        """
        Updates the wallet data by retrieving the latest information from external APIs
        and updating the corresponding data in the "wallets.json" file.
        """
        # Read the wallet data from the "wallets.json" file
        data = get_wallets()
        addresses = [wallet["address"] for wallet in data["addresses"]]

        # Retrieve the current price of BTC/USDT from the Binance API
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        
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
            price = response.json()["price"]
            data["price"] = float(price)

        # Create a string of addresses separated by "|" for the API request
        address_str = "|".join(addresses)
        url = f"https://blockchain.info/multiaddr?active={address_str}&n=0"
        response = requests.get(url)
        result = response.json()

        # Update the wallet data with the latest information for each address
        for address_data in result["addresses"]:
            address = address_data["address"]
            total_received = address_data["total_received"]
            total_sent = address_data["total_sent"]
            n_tx = address_data["n_tx"]
            final_balance = address_data["final_balance"]
            final_balance_usd = final_balance / 100000000 * data["price"]

            for wallet in data["addresses"]:
                if wallet["address"] == address:
                    change = final_balance - wallet["balance"]["final_balance"]

                    wallet["balance"]["final_balance"] = final_balance
                    wallet["balance"]["final_balance_usd"] = final_balance_usd
                    wallet["balance"]["n_tx"] = n_tx
                    wallet["balance"]["total_received"] = total_received
                    wallet["balance"]["total_sent"] = total_sent
                    wallet["change"] = change
                    break

        save_wallets(data)

        # Update the model with the updated data
        self.data = data
        self.labelPrice.setText("{:,.2f}".format(self.data["price"]))

    def sortByColumn(self, column):
        self.tableView.clearSelection()
        self.show_details(reset=True)

        order = self.tableView.horizontalHeader().sortIndicatorOrder()
        self.tableView.sortByColumn(column, order)

    def show_details(self, index=None, reset=False):
        if reset:
            self.labelAddress.setText("")
            self.labelFinalBalance.setText("")
            self.labelTotalTnx.setText("")
            self.labelTotalReceived.setText("")
            self.labelTotalSent.setText("")
            self.labelLastTnx.setText("")

            self.btnDelete.setEnabled(False)
            return

        address_data = self.model.data[index.row()]
        self.labelAddress.setText(address_data["address"])
        final_balance = address_data["balance"]["final_balance"]
        self.labelFinalBalance.setText("{:,.2f}".format(final_balance / SATOSHI))
        self.labelTotalTnx.setText(str(address_data["balance"]["n_tx"]))
        total_received = address_data["balance"]["total_received"]
        self.labelTotalReceived.setText("{:,.2f}".format(total_received / SATOSHI))
        total_sent = address_data["balance"]["total_sent"]
        self.labelTotalSent.setText("{:,.2f}".format(total_sent / SATOSHI))
        self.labelLastTnx.setText(str(self.last_tnx(address_data["address"])))

        self.btnDelete.setEnabled(True)

    def add_wallet(self):
        self.tableView.clearSelection()
        self.show_details(reset=True)

        dialog_add = DialogAdd(self)
        dialog_add.exec_()

    def delete_wallet(self):
        self.tableView.clearSelection()
        self.show_details(reset=True)

        index = self.tableView.selectionModel().currentIndex()
        if index.isValid():
            returnValue = self.show_confirmation_dialog(
                "Are you sure you want to delete this wallet?"
            )
            if returnValue == QMessageBox.Yes:
                self.remove_wallet(index.row())

    def show_confirmation_dialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        return msgBox.exec()

    def remove_wallet(self, row):
        del self.data["addresses"][row]
        self.model.refresh(self.data["addresses"])
        self.show_details(reset=True)

        save_wallets(self.data)

    def last_tnx(self, address):
        response = requests.get(
            f"https://blockchain.info/multiaddr?active={address}&n=1"
        )

        if response.status_code == 200:
            data = response.json()
            last_transaction = data["txs"][0]

            timestamp = last_transaction["time"]
            date = datetime.datetime.fromtimestamp(timestamp)

            return date
        else:
            print(f"Failed to get last_tnx, status code: {response.status_code}")
            return "Error"


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
