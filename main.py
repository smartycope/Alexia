import sys
from PyQt6.QtWidgets import QApplication
from Window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
