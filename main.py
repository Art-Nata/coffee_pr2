import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QAbstractItemView
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from main_window import Ui_Form
from addEditCoffeeForm import Ui_addCoffee

CON = sqlite3.connect('data/coffee.sqlite')
str_list = []
is_edd: bool = True


class DBCoffee(QWidget, Ui_Form):
    def __init__(self):
        super(DBCoffee, self).__init__()
        self.setupUi(self)
        self.open_db()
        self.tableWidget.clicked.connect(self.list_str)
        self.addButton.clicked.connect(self.add)
        self.editButton.clicked.connect(self.edit)

    def open_db(self):
        # отображение таблицы в окне
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
                    ORDER BY coffee_specifications.ID
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

    def list_str(self):
        # получаем список из текущей строки
        global str_list
        str_list = []
        for i in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(self.tableWidget.currentRow(), i)
            l = item.text()
            str_list.append(l)

    def add(self):
        # добавление новой строки
        global is_edd
        is_edd = True
        self.wnd_add = AddEditForm()
        self.wnd_add.show()
        self.open_db()
        self.update()

    def edit(self):
        # редактирование выделенной строки
        global is_edd
        is_edd = False
        self.wnd_add = AddEditForm()
        self.wnd_add.show()
        self.open_db()
        self.update()


class AddEditForm(QWidget, Ui_addCoffee):
    def __init__(self):
        super(AddEditForm, self).__init__()
        self.setupUi(self)
        self.lineEdit_ID.setEnabled(False)
        self.params = {}
        self.params_type = {}
        self.con1 = CON
        self.open_wnd()
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

    def open_wnd(self):
        global str_list, is_edd
        self.select_degree()
        self.select_type()

        if not is_edd:
            if str_list:
                id, name_in, degree_in, type_coffee_in, text_in, price_in, volue_1_in = str_list
                self.lineEdit_ID.setText(id)
                self.lineEdit_name.setText(name_in)
                self.textEdit.insertPlainText(text_in)
                self.lineEdit_price.setText(price_in)
                self.lineEdit_volue.setText(volue_1_in)
        else:
            self.lineEdit_name.clear()
            self.textEdit.clear()
            self.lineEdit_price.clear()
            self.lineEdit_volue.clear()

    def run(self):
        global is_edd, str_list

        name = self.lineEdit_name.text()
        degree = self.comboBox.currentText()
        type_coffee = self.comboBox_type.currentText()
        text = self.textEdit.toPlainText()
        price = self.lineEdit_price.text()
        volue_t = self.lineEdit_volue.text()
        for vol, key in self.params.items():
            if vol == degree:
                id_degree = key
        for volue, key in self.params_type.items():
            if volue == type_coffee:
                id_type_coffee = key

        if is_edd:

            req = f"INSERT INTO coffee_specifications(name, id_degree, id_type_coffee, description, " \
                  f"price, packing_volume) " \
                  f"VALUES ('{name}', '{id_degree}', '{id_type_coffee}', '{text}', '{price}', '{volue_t}')"
        else:
            id_curr = str_list[0]
            req = f"UPDATE coffee_specifications " \
                  f"SET name = '{name}', id_degree = '{id_degree}', id_type_coffee = '{id_type_coffee}', " \
                  f"description = '{text}', price = '{price}', packing_volume = '{volue_t}'" \
                  f"WHERE ID = '{id_curr}'"

        cur = self.con1.cursor()
        cur.execute(req)
        self.con1.commit()
        self.close()


def except_hoock(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hoock
    app = QApplication(sys.argv)
    wnd = DBCoffee()
    wnd.show()
    sys.exit(app.exec())
