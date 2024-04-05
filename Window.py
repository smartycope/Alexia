from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QMainWindow, QLabel, QApplication)
import json
import re
from PyQt6.QtGui import QMovie, QFont, QScreen
from PyQt6.QtCore import QSize, Qt, QTimer, QThread
from PyQt6 import uic
from Cope import debug, todo, untested, distinctColor
from Singleton import Singleton as S
from Loading import GPTRequest
import clipboard
import openai
import sys
from time import sleep

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = S.settings['advanced/API_Key']

exampleText = """
    <html>
        <head/>
            <body>
                <p>
                <span style=" font-style:italic;">Press</span>
                <span style=" text-decoration: underline;">Ctrl+v</span>
                <span style=" color:#ff0004;"> to</span>
                <span style=" font-weight:700;">paste</span>
                <span style=" font-size:18pt;">text</span>
                <span style=" background-color: #000000">...</span>
                </p>
            </body>
    </html>
"""

class Window(QMainWindow):
    black = '#ffffff'
    white = '#000000'
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(S.ui / "form.ui", self)
        S.mainWindow = self
        self.bindSignals()

        self._bodyText = ''
        self._rawBodyText = ''
        self.summarized = False # We don't want to summarize a summary
        self.importanced = False
        self.namesColored = False
        self.requestThread = QThread(self)

        self.text.setFont(QFont(str(S.settings['font'])))

        self.updateText('Sup homies')

    def bindSignals(self):
        self.actionPaste.triggered.connect(self.getTextFromClipboard)
        self.actionInvertColors.triggered.connect(self.reloadText)
        self.actionImportance.triggered.connect(self.reloadText)
        self.actionSummarize.triggered.connect(self.reloadText)
        self.actionColorNames.triggered.connect(self.reloadText)
        self.actionDebug.triggered.connect(self.debug)
        self.actionSettings.triggered.connect(lambda: S.settings.generateMenu(self))

    def debug(self):
        debug('Debugging Action Triggered!')
        self.startLoading()
        sleep(3)
        self.stopLoading()
        debug()

    def getTextFromClipboard(self):
        self.summarized = False
        self.importanced = False
        self.namesColored = False
        self.updateText(clipboard.paste())

    def reloadText(self):
        self.updateText(self._rawBodyText)

    def updateText(self, text):
        self._rawBodyText = text
        custom = False
        if self.actionSummarize.isChecked() and not self.summarized:
            debug('Summarizing')
            custom = True
            self.summarized = True
            self.request(S.summaryPrefix.format(self._rawBodyText), temp=S.settings['advanced/summarize_temperature'])

        if self.actionColorNames.isChecked() and not self.namesColored:
            debug('Coloring Names')
            custom = True
            self.namesColored = True
            self.request(S.colorNamesPrefix.format(self._bodyText), temp=S.settings['advanced/color_names_temperature'], outputHandler=self._colorText)

        if self.actionImportance.isChecked() and not self.importanced:
            debug('Marking word importance')
            custom = True
            self.importanced = True
            self.request(S.importancePrefix.format(self._bodyText), temp=S.settings['advanced/importance_temperature'])

        if not custom:
            debug('manually setting text')
            self._setText(self._rawBodyText)

    def _colorText(self, text):
        t = self._bodyText
        # I think this should work, it's untested
        for name, color in json.loads(text):
            t = re.sub(name, f'<span style=" color:{distinctColor(color)};">name</span>', t)
        self._setText()

    def _setText(self, text):
        self._bodyText = text
        text = f"""<html>
                        <head/>
                            <body>
                                <p>
                                    <span style=" background-color: {self.black if self.actionInvertColors.isChecked() else self.white}">
                                    <span style=" color: {self.white if self.actionInvertColors.isChecked() else self.black}">
                                        {text}
                                    </span>
                                    </span>
                                </p>
                            </body>
                    </html>
                """
        self.text.setText(text)

    def request(self, prompt, temp, outputHandler=None):
        if outputHandler is None:
            outputHandler = self._setText
        def requestDone(s):
            self.stopLoading()
            self.requestThread.exit(0)
            outputHandler(s)

        # Initialize the request thread
        self.loader = GPTRequest(prompt, temp)
        self.loader.moveToThread(self.requestThread)
        self.loader.resultsReady.connect(requestDone)
        # self.loadingThread.finished.connect(lambda: debug('thread finished called'))
        self.requestThread.started.connect(self.loader.run)

        # Start loading & start the thread
        self.startLoading()
        self.requestThread.start()

    def startLoading(self):
        self._label = QLabel(self)
        self._label.setScaledContents(True)
        self._label.setMinimumSize(QSize(150, 100))
        self._label.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.WindowDoesNotAcceptFocus | Qt.WindowType.WindowTransparentForInput)
        self._label.move(self._label.screen().geometry().center() - self._label.rect().center())
        self._movie = QMovie(S.loadingGIF)
        self._label.setMovie(self._movie)
        self._label.show()
        self._movie.start()

    def stopLoading(self):
        self._movie.stop()
        self._label.close()

    def close(self):
        if self.requestThread.isRunning():
            self.requestThread.exit(5)
        super().close()
