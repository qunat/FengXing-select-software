import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QBrush, QPixmap, QMovie

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.resize(400, 100)
pix1 = QPixmap("./"+'Pic/' + "FX" + ".png")
print(123)
widget.setWindowTitle("This is a demo for PyQt Widget.")
widget.show()

exit(app.exec_())
