from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from version import __version__
from utils.file_utils import get_path


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(get_path(__file__, "ui/dialog_about.ui"), self)

        self.labelVersion.setText(f"Version: {__version__}")
        pixmap = QPixmap(get_path(__file__, "images/logo.png"))
        self.labelLogo.setPixmap(pixmap)
