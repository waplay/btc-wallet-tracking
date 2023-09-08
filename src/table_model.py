from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt5.QtGui import QBrush

class WalletsTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.headers = ["Name", "Address", "BTC", "USD", "Change (BTC)"]

    def refresh(self, data):
        self.layoutAboutToBeChanged.emit()
        self.data = data
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.ForegroundRole:
            row = index.row()
            if index.column() == len(self.headers) - 1:
                value = self.data[row]["change"] / 100000000
                if value > 0:
                    return QBrush(Qt.green)
                elif value < 0:
                    return QBrush(Qt.red)
                else:
                    return QBrush(Qt.blue)

        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                return self.data[row]["name"]
            elif column == 1:
                return self.data[row]["address"]
            elif column == 2:
                return "{:,.2f}".format(
                    self.data[row]["balance"]["final_balance"] / 100000000
                )
            elif column == 3:
                return "{:,.2f}".format(self.data[row]["balance"]["final_balance_usd"])
            elif column == 4:
                return "{:,.2f}".format(self.data[row]["change"] / 100000000)
                
        return QVariant()

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()

        if column == self.headers.index("BTC"):
            self.data = sorted(
                self.data,
                key=lambda item: item["balance"]["final_balance"],
                reverse=order == Qt.DescendingOrder,
            )
        elif column == self.headers.index("USD"):
            self.data = sorted(
                self.data,
                key=lambda item: float(
                    item["balance"]["final_balance_usd"]
                ),
                reverse=order == Qt.DescendingOrder,
            )
        elif column == self.headers.index("Change (BTC)"):
            self.data = sorted(
                self.data,
                key=lambda item: item["change"],
                reverse=order == Qt.DescendingOrder,
            )
        elif column == self.headers.index("Name"):
            self.data = sorted(
                self.data,
                key=lambda item: item["name"],
                reverse=order == Qt.DescendingOrder,
            )
        elif column == self.headers.index("Address"):
            self.data = sorted(
                self.data,
                key=lambda item: item["address"],
                reverse=order == Qt.DescendingOrder,
            )
        else:
            self.data = sorted(
                self.data,
                key=lambda item: item[self.headers[column]],
                reverse=order == Qt.DescendingOrder,
            )

        self.layoutChanged.emit()