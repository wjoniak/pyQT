import sys
from datetime import date
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QCalendarWidget, QPushButton, QDialog, QLabel, QVBoxLayout,QDialogButtonBox,QFormLayout,QSizePolicy,QComboBox
from PyQt6.QtCore import QLocale

import sqlite3


class TableViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicjalizacja interfejsu użytkownika
        self.initUI()

        # Łączenie z bazą danych SQLite
        self.conn = sqlite3.connect('baza_danych.db')
        self.cur = self.conn.cursor()

        # Pobranie danych z bazy
        self.cur.execute("SELECT godzina,imie_nazwisko FROM terminarz")
        data = self.cur.fetchall()

        # Wyświetlenie danych w tabeli
        self.displayData(data,date.today())


    def initUI(self):
        self.setWindowTitle('PTTP')
        self.setGeometry(100, 100, 800, 600)

        # Utworzenie QTabWidget
        tabWidget = QTabWidget()

        # Dodanie karty z tabelą
        tableWidget = QTableWidget()
        tableWidget.setShowGrid(False)

        tableWidget.verticalHeader().setVisible(False)  # Ukrywa numery wierszy
        tableWidget.horizontalHeader().setVisible(False)  # Ukrywa numery kolumn

        formWidget = QWidget()
        calendarWidget = QCalendarWidget()
        calendarWidget.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        calendarWidget.setLocale(QLocale(QLocale.Language.Polish))
        tabWidget.addTab(calendarWidget, 'Kalendarz')
        tabWidget.addTab(tableWidget, 'plan dnia')
        self.layout_table = QVBoxLayout(tableWidget)


        tabWidget.addTab(formWidget, 'trening')
        self.layout_trening = QVBoxLayout(formWidget)

        layout = QVBoxLayout()

        layout.addWidget(tabWidget)


        # Ustawienie kolumn w tabeli
        tableWidget.setColumnCount(7)  # Dodaliśmy dwie kolumny na przyciski
        #tableWidget.setHorizontalHeaderLabels(['Kolumna 1', 'Kolumna 2', 'Kolumna 3', 'Akcja 1', 'Akcja 2'])

        # Ustawienie rozmiaru kolumn
        tableWidget.setColumnWidth(0, 60)
        tableWidget.setColumnWidth(1, 150)
        tableWidget.setColumnWidth(2, 50)
        tableWidget.setColumnWidth(3, 120)
        tableWidget.setColumnWidth(4, 120)  # Ustawiamy szerokość kolumny z przyciskiem 1
        tableWidget.setColumnWidth(5, 100)  # Ustawiamy szerokość kolumny z przyciskiem 2
        tableWidget.setColumnWidth(6, 150)
        # Ustawienie rosnącego rozmiaru wierszy
        tableWidget.verticalHeader().setDefaultSectionSize(50)

        # Utworzenie karty z kalendarzem


        # Podłączenie sygnału clicked z QCalendarWidget do funkcji displayDataByDate
        calendarWidget.clicked.connect(self.displayDataByDate)

        # Ustawienie głównego widgetu
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def displayData(self, data,day):
        # Wstawienie danych do tabeli
        tableWidget = self.centralWidget().findChild(QTableWidget)

        tableWidget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                if  cell_data is not None:
                    tableWidget.setItem(row_idx, col_idx, item)
                else:
                    button0 = QPushButton('zaplanuj')
                    button0.clicked.connect(lambda _, row=row_idx: self.onButtonClick0(row))
                    button0.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    tableWidget.setCellWidget(row_idx, 4, button0)

                if col_idx == 1 and cell_data is not None:
                    button1 = QPushButton('dodaj płatność')
                    button1.clicked.connect(lambda _, row=row_idx: self.onButtonClick1(row))
                    button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    tableWidget.setCellWidget(row_idx, 4, button1)
                if col_idx == 1 and cell_data is not None:
                    button2 = QPushButton('edytuj dane')
                    button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    button2.clicked.connect(lambda _, row=row_idx: self.onButtonClick2(row))
                    tableWidget.setCellWidget(row_idx, 5, button2)
                if col_idx == 1 and cell_data is not None:
                    button3 = QPushButton('przejdź do treningu')
                    button3.clicked.connect(lambda _, row=row_idx: self.onButtonClick3(row))
                    button3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    tableWidget.setCellWidget(row_idx, 6, button3)

    def onButtonClick0(self, row):
        dialog = self.Dialog
        self.showDialog(row, 'zaplanuj')

    def onButtonClick1(self, row):
        self.showDialog(row, 'dodaj płatność')

    def onButtonClick2(self, row):

        self.centralWidget().findChild(QTabWidget).setCurrentIndex(2)  # Przełączamy na nową kartę

    def onButtonClick3(self, row):
        tabWidget = self.centralWidget().findChild(QTabWidget)
        tabWidget.setCurrentIndex(2)

    def treningOption(self,row):
        pass

    def displayDataByDate(self):
        # Pobieramy datę z QCalendarWidget
        calendarWidget = self.centralWidget().findChild(QCalendarWidget)
        selected_date = calendarWidget.selectedDate()


        # Formatujemy datę na format zgodny z bazą danych (np. 'RRRR-MM-DD')
        formatted_date = selected_date.toString('yyyy-MM-dd')

        # Łączymy się z bazą danych
        self.conn = sqlite3.connect('baza_danych.db')
        self.cur = self.conn.cursor()

        # Pobieramy dane z bazy na podstawie wybranej daty
        self.cur.execute("SELECT godzina,imie_nazwisko FROM terminarz"
                         " WHERE data=?", (formatted_date,))
        data = self.cur.fetchall()

        # Wyświetlamy dane w tabeli
        self.displayData(data,formatted_date)

        # Przełączamy na kartę z tabelą
        tabWidget = self.centralWidget().findChild(QTabWidget)
        tabWidget.setCurrentIndex(1)

        # Zamykamy połączenie z bazą danych
        self.conn.close()

    def closeEvent(self, event):
        # Zamykanie połączenia z bazą danych przy zamykaniu okna
        self.conn.close()


class Dialog(QDialog):
    def __init__(self, selected_date, record, parent=None):
        super().__init__(parent)

        self.selected_date = selected_date
        self.record = record

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        #label_date = QLabel(f'Selected date: {self.selected_date}')
        #layout.addWidget(label_date)

        #label_record = QLabel(f'Record: {self.record}')
        #layout.addWidget(label_record)

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.addPayment)
        buttonBox.rejected.connect(self.reject)

        self.setLayout(layout)

    def addPayment(self):

        conn = sqlite3.connect('baza_danych.db')
        c = conn.cursor()
        print(f'INSERT INTO platnosci (klient_id,data,kwota) VALUES {self.record[3],self.record[1],100}')
        c.execute(f'INSERT INTO platnosci (klient_id, data, kwota) VALUES (?, ?, ?)',(self.record[3], self.record[1], 100))

        conn.commit()
        conn.close()


        # Zamykamy okno dialogowe
        self.accept()

    def selektor_klienta():
        conn = sqlite3.connect('baza_danych.db')
        c = conn.cursor()
        c.execute('SELECT imie_nazwisko FROM klienci')
        nazwiska = c.fetchall()
        conn.close()
        combo_box = QComboBox()
        combo_box.addItem('wybierz ...')
        for nazwisko in nazwiska:
            combo_box.addItem(nazwisko[0])

        return combo_box


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TableViewer()

    # open qss file
    with open("Ubuntu.qss", "r") as file:
        app.setStyleSheet(file.read())

    viewer.show()
    sys.exit(app.exec())
