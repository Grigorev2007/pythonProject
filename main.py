import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QListWidget, QPushButton


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        price = 0
        uic.loadUi("project.ui", self)
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        result = cur.execute("""
        SELECT Thing FROM Things""").fetchall()
        for i in range(len(result)):
            self.listWidget.addItem(result[i][0])
        for i in range(len(result)):
            price += int(cur.execute(f'''
        SELECT Quantity, Price FROM Things where thing like \"{result[i][0]}\"''').fetchall()[0][0]) * int(cur.execute(f'''
        SELECT Quantity, Price FROM Things where thing like \"{result[i][0]}\"''').fetchall()[0][1])
        cur.close()
        con.close()
        self.label_2.setText(str(price))
        self.pushButton.clicked.connect(self.payment)
        self.pushButton_3.clicked.connect(self.adding)
        self.listWidget.itemDoubleClicked.connect(self.showItem)
        self.pushButton_4.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.list_of_things)
        if self.label_2.text() == "0":
            self.label_3.setText("Добавьте что-то в корзину для оплаты")
        self.pushButton_2.clicked.connect(self.null)

    def showItem(self):
        a = self.listWidget.currentItem().text()
        uic.loadUi('project_2.ui', self)
        if len(a) >= 2:
            if a[-2] == " ":
                a = a[:-2]
        self.pushButton.clicked.connect(self.back)
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        result = cur.execute(f'''
                SELECT Quantity FROM Things
                WHERE Thing = \"{a}\" ''').fetchall()
        n = int(result[0][0])
        result = cur.execute(f'''
            SELECT Price FROM Things
            WHERE Thing = \"{a}\" ''').fetchall()
        self.label_5.setText(str(result[0][0]))
        result = cur.execute(f'''
            SELECT Image FROM Images
            WHERE Thing = \"{a}\" ''').fetchall()
        pixmap = QPixmap(result[0][0])
        self.label_6.setPixmap(pixmap)
        cur.close()
        con.close()
        self.spinBox.setValue(n)
        self.label_2.setText(a)

    def back(self):
        price = 0
        item = self.label_2.text()
        kolvo = int(self.spinBox.value())
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        cur.execute(f'''
        UPDATE Things
        SET Quantity = \"{kolvo}\"\
        WHERE Thing = \"{item}\"
        ''')
        con.commit()
        uic.loadUi("project.ui", self)
        result = cur.execute("""
        SELECT Thing FROM Things""").fetchall()
        for i in range(len(result)):
            self.listWidget.addItem(result[i][0])
        for i in range(len(result)):
            price += int(cur.execute(f'''
                SELECT Quantity, Price FROM Things 
                where thing like \"{result[i][0]}\"''').fetchall()[0][0]) * int(
                cur.execute(f'''
                SELECT Quantity, Price FROM Things 
                where thing like \"{result[i][0]}\"''').fetchall()[0][1])
        cur.close()
        con.close()
        self.label_2.setText(str(price))
        self.pushButton.clicked.connect(self.payment)
        self.pushButton_3.clicked.connect(self.adding)
        self.listWidget.itemDoubleClicked.connect(self.showItem)
        self.pushButton_4.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.list_of_things)
        if self.label_2.text() == "0":
            self.label_3.setText("Добавьте что-то в корзину для оплаты")
        self.pushButton_2.clicked.connect(self.null)

    def back2(self):
        price = 0
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        a = self.lineEdit.text()
        b = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        cur.execute(f'''
                INSERT INTO Things VALUES (\"{a}\", '0', \"{b}\")
                ''')
        con.commit()
        cur.execute(f'''
                INSERT INTO Images VALUES (\"{a}\", \"{c}\")
                ''')
        con.commit()
        uic.loadUi("project.ui", self)
        result = cur.execute("""
                SELECT Thing FROM Things""").fetchall()
        for i in range(len(result)):
            self.listWidget.addItem(result[i][0])
        for i in range(len(result)):
            price += int(cur.execute(f'''
                        SELECT Quantity, Price FROM Things 
                        where thing like \"{result[i][0]}\"''').fetchall()[0][0]) * int(
                cur.execute(f'''
                        SELECT Quantity, Price FROM Things 
                        where thing like \"{result[i][0]}\"''').fetchall()[0][1])
        cur.close()
        con.close()
        self.label_2.setText(str(price))
        self.pushButton.clicked.connect(self.payment)
        self.pushButton_3.clicked.connect(self.adding)
        self.listWidget.itemDoubleClicked.connect(self.showItem)
        self.pushButton_4.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.list_of_things)
        if self.label_2.text() == "0":
            self.label_3.setText("Добавьте что-то в корзину для оплаты")
        self.pushButton_2.clicked.connect(self.null)

    def back3(self):
        price = 0
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        a = self.lineEdit.text()
        if a == "Карандаш" or a == "Скотч" or a == "Ножницы" or a == "Линейка" or a == "Маркер" or  a == "Ручка":
            self.label_2.setText("К сожалению, Вы не можете это удалить(")
            self.delete
        else:
            cur.execute(f'''
                DELETE FROM Things WHERE Thing = \"{a}\"
                ''')
            con.commit()
            cur.execute(f'''
                DELETE FROM Images WHERE Thing = \"{a}\"
                ''')
            con.commit()
            uic.loadUi("project.ui", self)
            result = cur.execute("""
                SELECT Thing FROM Things""").fetchall()
            for i in range(len(result)):
                self.listWidget.addItem(result[i][0])
            for i in range(len(result)):
                price += int(cur.execute(f'''
                        SELECT Quantity, Price FROM Things 
                        where thing like \"{result[i][0]}\"''').fetchall()[0][0]) * int(
                    cur.execute(f'''
                        SELECT Quantity, Price FROM Things 
                        where thing like \"{result[i][0]}\"''').fetchall()[0][1])
            cur.close()
            con.close()
            self.label_2.setText(str(price))
            self.pushButton.clicked.connect(self.payment)
            self.pushButton_3.clicked.connect(self.adding)
            self.listWidget.itemDoubleClicked.connect(self.showItem)
            self.pushButton_4.clicked.connect(self.delete)
            if self.label_2.text() == "0":
                self.label_3.setText("Добавьте что-то в корзину для оплаты")
            self.pushButton_5.clicked.connect(self.list_of_things)
            self.pushButton_2.clicked.connect(self.null)

    def back4(self):
        price = 0
        uic.loadUi("project.ui", self)
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        result = cur.execute("""
                SELECT Thing FROM Things""").fetchall()
        for i in range(len(result)):
            self.listWidget.addItem(result[i][0])
        for i in range(len(result)):
            price += int(cur.execute(f'''
                SELECT Quantity, Price FROM Things where thing like \"{result[i][0]}\"''').fetchall()[0][0]) * int(
                cur.execute(f'''
                SELECT Quantity, Price FROM Things where thing like \"{result[i][0]}\"''').fetchall()[0][1])
        cur.close()
        con.close()
        self.label_2.setText(str(price))
        self.pushButton.clicked.connect(self.payment)
        self.pushButton_3.clicked.connect(self.adding)
        self.listWidget.itemDoubleClicked.connect(self.showItem)
        self.pushButton_4.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.list_of_things)
        if self.label_2.text() == "0":
            self.label_3.setText("Добавьте что-то в корзину для оплаты")
        self.pushButton_2.clicked.connect(self.null)

    def payment(self):
        counter = 0
        if len(self.lineEdit.text()) == 16:
            for i in range(16):
                if not (self.lineEdit.text()[i].isdigit() is True):
                    counter += 1
            if counter == 0:
                self.label_4.setText("Успешно!")
            else:
                self.label_4.setText("Похоже, не всё, что Вы ввели - цифры.")
        else:
            self.label_4.setText("Упс! Проверьте, что цифр 16!")
        counter = 0

    def null(self):
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        cur.execute(f'''
        UPDATE Things
        SET Quantity = 0
        ''')
        con.commit()
        self.label_2.setText('0')
        self.label_3.setText("Добавьте что-то в корзину для оплаты")
        cur.close()
        con.close()

    def adding(self):
        uic.loadUi("project_3.ui", self)
        self.pushButton.clicked.connect(self.back2)

    def delete(self):
        uic.loadUi("project_4.ui", self)
        self.pushButton.clicked.connect(self.back3)

    def list_of_things(self):
        uic.loadUi("project_5.ui", self)
        self.pushButton.clicked.connect(self.back4)
        self.listWidget.itemDoubleClicked.connect(self.showItem)
        con = sqlite3.connect("Project.sqlite")
        cur = con.cursor()
        result = cur.execute("""
            SELECT Thing, Quantity FROM Things
            WHERE Quantity NOT LIKE 0""").fetchall()
        for i in range(len(result)):
            self.listWidget.addItem(result[i][0] + ' ' + str(result[i][1]))
        cur.close()
        con.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())