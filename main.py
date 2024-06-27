Version = 0.1

from main_systems import db

import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 400, 300)

        btn1 = QPushButton("login")
        btn2 = QPushButton("sing up")

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        self.setCentralWidget(widget)

        vbox = widget.findChildren(QVBoxLayout)[0]
        btn = vbox.itemAt(0).widget()
        print(btn.text())


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()