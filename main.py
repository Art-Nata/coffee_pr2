import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QTableWidgetItem


class DBCoffee(QWidget):
    def __init__(self):
        super(DBCoffee, self).__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.open_db()
        self.addButton.clicked.connect(self.add)
        self.editButton.clicked.connect(self.edit)

    def open_db(self):

        query = """SELECT
                      coffee_specifications.ID,
                      coffee_specifications.name,
                      degree_of_roasting.degree,
                      type_coffee.type_coffee,
                      coffee_specifications.description,
                      coffee_specifications.price,
                      coffee_specifications.packing_volume
                    FROM coffee_specifications
                    LEFT JOIN degree_of_roasting ON coffee_specifications.id_degree = degree_of_roasting.id
                    LEFT JOIN type_coffee ON coffee_specifications.id_type_coffee = type_coffee.id
                """
        rez = self.con.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(len(rez[0]))
        self.tableWidget.setRowCount(len(rez))
        self.tableWidget.setHorizontalHeaderLabels(["ID", 'Название', 'Степень обжарки', 'Молотый', 'Описание',
                                                    'Цена', 'Объём'])
        for i, row1 in enumerate(rez):
            for j, vol in enumerate(row1):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(vol)))
        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.con.close()

    def add(self):
        wnd1.show()

    def edit(self):
        wnd1.show()


class AddEditForm(QWidget):
    def __init__(self):
        super(AddEditForm, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.lineEdit_ID.setEnabled(False)
        self.comboBox_type.clear()
        self.comboBox_type.addItems(['молотый', 'в зёрнах'])



def except_hoock(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hoock
    app = QApplication(sys.argv)
    wnd = DBCoffee()
    wnd1 = AddEditForm()
    wnd.show()
    sys.exit(app.exec())
