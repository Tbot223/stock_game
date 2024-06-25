import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 420, 120)

        btn = QPushButton(text="로그인", parent=self)
        btn.move(220, 10)
        btn.resize(200, 100)
        btn = QPushButton(text="가입", parent=self)
        btn.move(0, 10)
        btn.resize(200, 100)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()