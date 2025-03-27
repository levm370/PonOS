from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

app = QApplication()
window = QMainWindow()
window.setWindowTitle('PonosWeb')
browser = QWebEngineView()
browser.load("https://google.com")
window.setCentralWidget(browser)
window.show()
app.exec()
