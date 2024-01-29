import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QAbstractItemView
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

CON = sqlite3.connect('coffee.sqlite')


class DBCoffee(QWidget):
    def __init__(self):
        super(DBCoffee, self).__init__()
        uic.loadUi('main.ui', self)
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
        rez = CON.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(len(rez[0]))
        self.tableWidget.setRowCount(len(rez))
        self.tableWidget.setHorizontalHeaderLabels(["ID", 'Название', 'Степень обжарки', 'Молотый', 'Описание',
                                                    'Цена', 'Объём'])
        for i, row1 in enumerate(rez):
            for j, vol in enumerate(row1):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(vol)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        CON.close()

    def add(self):
        wnd1.show()

    def edit(self):
        wnd1.show()


class AddEditForm(QWidget):
    def __init__(self, con):
        super(AddEditForm, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.lineEdit_ID.setEnabled(False)
        self.params = {}
        self.params_type = {}
        self.con1 = con
        self.select_degree()
        self.select_type()
        self.okButton.clicked.connect(self.run)

    def select_degree(self):
        req = "SELECT * from degree_of_roasting"
        cur1 = self.con1.cursor()
        for value, key in cur1.execute(req).fetchall():
            self.params[key] = value
        self.comboBox.addItems(list(self.params.keys()))

    def select_type(self):
        req = "SELECT * from type_coffee"
        cur1 = self.con1.cursor()
        for value, key in cur1.execute(req).fetchall():
            self.params_type[key] = value
        self.comboBox_type.addItems(list(self.params_type.keys()))

    def run(self):
        name = self.lineEdit_name.text()
        degree = self.comboBox.currentText()
        type_coffee = self.comboBox_type.currentText()
        text = self.textEdit.toPlainText()
        price = self.lineEdit_price.text()
        volue_1 = self.lineEdit_volue.text()
        for vol, key in self.params.items():
            if vol == degree:
                id_degree = key
        for volue, key in self.params_type.items():
            if volue == type_coffee:
                id_type_coffee = key

        req = f"INSERT INTO coffee_specifications(name, id_degree, id_type_coffee, description, " \
              f"price, packing_volume) "\
              f"VALUES ('{name}', '{id_degree}', '{id_type_coffee}', '{text}', '{price}', '{volue_1}')"

        cur1 = self.con1.cursor()
        cur1.execute(req)
        self.con1.commit()

        self.lineEdit_name.clear()
        self.textEdit.clear()
        self.lineEdit_price.clear()
        self.lineEdit_volue.clear()

        wnd1.close()




def except_hoock(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hoock
    app = QApplication(sys.argv)
    wnd = DBCoffee()
    wnd1 = AddEditForm(CON)
    wnd.show()
    sys.exit(app.exec())
