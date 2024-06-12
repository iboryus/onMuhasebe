import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTabWidget, QLabel # type: ignore

class MyWindow(QMainWindow):
    def __init__(self, titles):
        super().__init__()

        self.titles = titles

        self.setWindowTitle("Sekme İle Metin Girişi")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.textbox = QLineEdit()
        self.layout.addWidget(self.textbox)

        self.start_button = QPushButton("Başlat")
        self.start_button.clicked.connect(self.update_tabs)
        self.layout.addWidget(self.start_button)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.tabs = []

    def update_tabs(self):
        text = self.textbox.text()
        for idx, title in enumerate(self.titles):
            if idx >= self.tab_widget.count():
                tab = QWidget()
                layout = QVBoxLayout()
                tab.setLayout(layout)
                self.tab_widget.addTab(tab, f"Sekme {idx+1}")

                label = QLabel(f"{text} - {title}")
                layout.addWidget(label)
            else:
                tab = self.tab_widget.widget(idx)
                layout = tab.layout()
                label = layout.itemAt(0).widget()
                label.setText(f"{text} - {title}")

if __name__ == "__main__":
    titles = [
        "de 1",
        "de 2",
        "de 3",
        "de 4",
        "de 5",
        "de 6",
        "de 7",
        "de 8",
        "de 9",
        "de 10",
        "de 11",
        "de 12",
        "de 13",
        "de 14",
        "de 15",
        "de 16",
        "de 17",
        "de 18",
        "de 19",
        "de 20",
        "de 21",
        "de 22",
        "de 23",
        "de 24",
        "de 25",
        "de 26",
        "de 27",
        "de 28",
    ]

    app = QApplication(sys.argv)
    window = MyWindow(titles)
    window.show()
    sys.exit(app.exec_())
