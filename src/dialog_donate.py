import webbrowser
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from utils.file_utils import get_path


class DonateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(get_path(__file__, "ui/dialog_donate.ui"), self)

        self.btnDonate.clicked.connect(self.onDonateClicked)
        self.btnClose.clicked.connect(self.close)

    def onDonateClicked(self):
        webbrowser.open("https://nowpayments.io/donation/waplay")
