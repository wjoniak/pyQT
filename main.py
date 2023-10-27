import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QCalendarWidget, QPushButton, QDialog, QLabel, QVBoxLayout

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
        self.cur.execute("SELECT * FROM tabela")
        data = self.cur.fetchall()

        # Wyświetlenie danych w tabeli
        self.displayData(data)
        # Wczytaj plik QSS
        with open('Adaptic.qss', 'r') as qss_file:
            stylesheet = qss_file.read()

        # Ustaw arkusz stylów dla całego okna
        self.setStyleSheet(stylesheet)

    def initUI(self):
        self.setWindowTitle('Table Viewer')
        self.setGeometry(100, 100, 800, 600)

        # Utworzenie QTabWidget
        tabWidget = QTabWidget()

        # Dodanie karty z tabelą
        tableWidget = QTableWidget()
        tabWidget.addTab(tableWidget, 'plan dnia')

        layout = QVBoxLayout()
        layout.addWidget(tabWidget)

        # Ustawienie kolumn w tabeli
        tableWidget.setColumnCount(5)  # Dodaliśmy dwie kolumny na przyciski
        tableWidget.setHorizontalHeaderLabels(['Kolumna 1', 'Kolumna 2', 'Kolumna 3', 'Akcja 1', 'Akcja 2'])

        # Ustawienie rozmiaru kolumn
        tableWidget.setColumnWidth(0, 150)
        tableWidget.setColumnWidth(1, 150)
        tableWidget.setColumnWidth(2, 150)
        tableWidget.setColumnWidth(3, 100)  # Ustawiamy szerokość kolumny z przyciskiem 1
        tableWidget.setColumnWidth(4, 100)  # Ustawiamy szerokość kolumny z przyciskiem 2

        # Ustawienie rosnącego rozmiaru wierszy
        tableWidget.verticalHeader().setDefaultSectionSize(50)

        # Utworzenie karty z kalendarzem
        calendarWidget = QCalendarWidget()
        tabWidget.addTab(calendarWidget, 'Kalendarz')

        # Podłączenie sygnału clicked z QCalendarWidget do funkcji displayDataByDate
        calendarWidget.clicked.connect(self.displayDataByDate)

        # Ustawienie głównego widgetu
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def displayData(self, data):
        # Wstawienie danych do tabeli
        tableWidget = self.centralWidget().findChild(QTableWidget)
        tableWidget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                tableWidget.setItem(row_idx, col_idx, item)
                button1 = QPushButton('Akcja 1')
                button1.clicked.connect(lambda _, row=row_idx: self.onButtonClick1(row))
                tableWidget.setCellWidget(row_idx, 3, button1)
                button2 = QPushButton('Akcja 2')
                button2.clicked.connect(lambda _, row=row_idx: self.onButtonClick2(row))
                tableWidget.setCellWidget(row_idx, 4, button2)

    def onButtonClick1(self, row):
        self.showDialog(row, 'Akcja 1')

    def onButtonClick2(self, row):
        self.showDialog(row, 'Akcja 2')

    def showDialog(self, row, action):
        # Pobieramy datę z QCalendarWidget
        calendarWidget = self.centralWidget().findChild(QCalendarWidget)
        selected_date = calendarWidget.selectedDate()

        # Formatujemy datę na format zgodny z bazą danych (np. 'RRRR-MM-DD')
        formatted_date = selected_date.toString('yyyy-MM-dd')

        # Łączymy się z bazą danych
        self.conn = sqlite3.connect('baza_danych.db')
        self.cur = self.conn.cursor()

        # Pobieramy dane z bazy dla wybranej daty i wybranego wiersza
        self.cur.execute("SELECT * FROM tabela WHERE data=?", (formatted_date,))
        data = self.cur.fetchall()

        # Tworzymy i wyświetlamy okno dialogowe
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Okno dialogowe - {action}')
        layout = QVBoxLayout()

        label_date = QLabel(f'Selected date: {formatted_date}')
        layout.addWidget(label_date)

        label_record = QLabel(f'Record: {data[row]}')
        layout.addWidget(label_record)

        dialog.setLayout(layout)
        dialog.exec()

        # Zamykamy połączenie z bazą danych
        self.conn.close()

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
        self.cur.execute("SELECT * FROM tabela WHERE data=?", (formatted_date,))
        data = self.cur.fetchall()

        # Wyświetlamy dane w tabeli
        self.displayData(data)

        # Przełączamy na kartę z tabelą
        tabWidget = self.centralWidget().findChild(QTabWidget)
        tabWidget.setCurrentIndex(0)

        # Zamykamy połączenie z bazą danych
        self.conn.close()

    def closeEvent(self, event):
        # Zamykanie połączenia z bazą danych przy zamykaniu okna
        self.conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TableViewer()
    viewer.show()
    sys.exit(app.exec())
