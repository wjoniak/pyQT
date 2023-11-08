import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QCalendarWidget, QTableView, \
    QDialog, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSpinBox, QTextEdit, QFormLayout,QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        statusbar = self.statusBar()

        clientMenu = menubar.addMenu('Klienci')
        calendarMenu = menubar.addMenu('Terminarz')
        trainingMenu = menubar.addMenu('Treningi')
        helpMenu = menubar.addMenu('Pomoc')

        calendarAction = QAction(QIcon('icons/icons8-calendar-48.png'), 'widok miesiąca', self)
        calendarAction.triggered.connect(self.showCalendar)
        calendarMenu.addAction(calendarAction)

        tableAction = QAction(QIcon('icons/icons8-schedule-48.png'),'widok dnia', self)
        tableAction.triggered.connect(self.showTableView)
        calendarMenu.addAction(tableAction)

        modalAction = QAction(QIcon('icons/icons8-add-user-48.png'),'nowy klient', self)
        modalAction.triggered.connect(self.showModalDialog)
        clientMenu.addAction(modalAction)

        clientsAction = QAction(QIcon('icons/icons8-male-female-user-group-48.png'),'lista klientów', self)
        clientsAction.triggered.connect(self.showClientsView)
        clientMenu.addAction(clientsAction)



        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Menu Example')
        self.show()

    def showCalendar(self):
        calendar = QCalendarWidget(self)
        self.setCentralWidget(calendar)

    def showTableView(self):
        tableview = QTableView(self)
        self.setCentralWidget(tableview)

    def showModalDialog(self):
        dialog = QDialog(self)
        layout = QFormLayout()

        nameInput = QLineEdit(self)
        layout.addRow('Imię i nazwisko:', nameInput)

        phoneInput = QLineEdit(self)
        layout.addRow('Telefon:', phoneInput)

        descriptionInput = QTextEdit(self)
        layout.addRow('Opis problemu:', descriptionInput)

        ageSpinBox = QSpinBox(self)
        ageSpinBox.setMinimum(0)
        ageSpinBox.setMaximum(150)
        ageSpinBox.setValue(10)
        layout.addRow('Wiek:', ageSpinBox)

        buttonsLayout = QHBoxLayout()
        saveButton = QPushButton('Zapisz', self)

        def save():
            name = nameInput.text()
            if not name:
                self.showAlert('Imię i nazwisko nie może być puste.')
                return

            connection = sqlite3.connect('baza_danych.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM klienci WHERE imie_nazwisko = ?', (name,))
            existing_record = cursor.fetchone()
            connection.close()

            if existing_record:
                self.showAlert('Osoba o takim imieniu i nazwisku jest już na liście klientów.')
            else:
                self.addToDatabase(name, phoneInput.text(), descriptionInput.toPlainText(), ageSpinBox.value(), dialog)

        saveButton.clicked.connect(save)
        cancelButton = QPushButton('Anuluj', self)
        cancelButton.clicked.connect(dialog.reject)
        buttonsLayout.addWidget(saveButton)
        buttonsLayout.addWidget(cancelButton)

        layout.addRow(buttonsLayout)

        dialog.setLayout(layout)
        dialog.setWindowTitle('Dodaj Klienta')
        dialog.setModal(True)
        dialog.exec()

    def showAlert(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle('Błąd')
        msg.exec_()

    def addToDatabase(self, name, phone, description, age, dialog):
        connection = sqlite3.connect('baza_danych.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO klienci (imie_nazwisko, telefon,wiek, opis_problemu ) VALUES (?, ?, ?, ?)',
                       (name, phone, age, description ))

        connection.commit()
        connection.close()

        dialog.accept()
        self.showClientsView()

    def showClientsView(self):
        connection = sqlite3.connect('baza_danych.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM klienci')
        data = cursor.fetchall()

        table = QTableWidget(self)
        table.setColumnCount(6)  # Dodatkowa kolumna na przyciski
        table.setHorizontalHeaderLabels(['Imię i nazwisko', 'Telefon', 'Wiek', 'Opis problemu', '', ''])

        for row in data:
            table.insertRow(table.rowCount())

            # Dodawanie przycisków "Edytuj dane" i "Dodaj płatność"
            editButton = QPushButton('Edytuj dane', self)
            editButton.clicked.connect(lambda _, id=row[0]: self.editClientData(id))
            table.setCellWidget(table.rowCount() - 1, 4, editButton)

            paymentButton = QPushButton('Dodaj płatność', self)
            paymentButton.clicked.connect(lambda _, id=row[0]: self.addPayment(id))
            table.setCellWidget(table.rowCount() - 1, 5, paymentButton)

            for column, item in enumerate(row[1:]):  # Rozpoczynamy od drugiej kolumny, pomijając ID
                table.setItem(table.rowCount() - 1, column, QTableWidgetItem(str(item)))

        connection.close()

        self.setCentralWidget(table)

    def editClientData(self, client_id):
        dialog = QDialog(self)
        layout = QFormLayout()

        connection = sqlite3.connect('baza_danych.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM klienci WHERE id = ?', (client_id,))
        data = cursor.fetchone()

        nameInput = QLineEdit(self)
        nameInput.setText(data[1])
        layout.addRow('Imię i nazwisko:', nameInput)

        phoneInput = QLineEdit(self)
        phoneInput.setText(str(data[2]))  # Konwersja na str przed ustawieniem
        layout.addRow('Telefon:', phoneInput)

        descriptionInput = QTextEdit(self)
        descriptionInput.setPlainText(str(data[3]))
        layout.addRow('Opis problemu:', descriptionInput)

        ageSpinBox = QSpinBox(self)
        ageSpinBox.setMinimum(0)
        ageSpinBox.setMaximum(150)
        descriptionInput.setPlainText(str(data[4]))
        layout.addRow('Wiek:', ageSpinBox)

        buttonsLayout = QHBoxLayout()
        saveButton = QPushButton('Zapisz', self)
        saveButton.clicked.connect(lambda: self.updateClientData(client_id, nameInput.text(), phoneInput.text(),
                                                                 descriptionInput.toPlainText(), ageSpinBox.value(),
                                                                 dialog))
        cancelButton = QPushButton('Anuluj', self)
        cancelButton.clicked.connect(dialog.reject)
        buttonsLayout.addWidget(saveButton)
        buttonsLayout.addWidget(cancelButton)

        layout.addRow(buttonsLayout)

        dialog.setLayout(layout)
        dialog.setWindowTitle('Edytuj Dane Klienta')
        dialog.setModal(True)
        dialog.exec()

    def updateClientData(self, client_id, name, phone, description, age, dialog):
        connection = sqlite3.connect('baza_danych.db')
        cursor = connection.cursor()

        cursor.execute('UPDATE klienci SET imie_nazwisko=?, telefon=?, opis_problemu=?, wiek=? WHERE id=?',
                       (name, phone, description, age, client_id))

        connection.commit()
        connection.close()

        dialog.accept()
        self.showClientsView()

    def addPayment(self, client_id):
        # Dodaj funkcję do dodawania płatności
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())
