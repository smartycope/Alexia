import sys
from Singleton import Singleton as S
from PyQt6.QtCore import QObject, QThread, QRunnable, Qt, QSize, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QApplication, QLabel
from Cope import debug
import time
import openai

dontMakeCall = S.debugging and False

class GPTRequest(QObject):
    resultsReady = pyqtSignal(str)

    def __init__(self, prompt, temp,
            model=S.settings['advanced/model'],
            max_len=S.settings['advanced/max_len'],
            freq_penalty=S.settings['advanced/frequency_penalty'],
            presence_penalty=S.settings['advanced/presence_penalty']):
        super().__init__()
        self.prompt = prompt
        self.response = None
        self.finishReason = None
        self.model = model
        self.temp = temp
        self.max_len = max_len
        self.freq_penalty = freq_penalty
        self.presence_penalty = presence_penalty

    def run(self):
        response = openai.Completion.create(
            model=self.model,
            prompt=self.prompt,
            temperature=self.temp,
            max_tokens=self.max_len,
            frequency_penalty=self.freq_penalty,
            presence_penalty=self.presence_penalty,
        )

        response = response['choices'][0]
        self.response = response['text']
        self.finishReason = response['finish_reason']
        self.resultsReady.emit(self.response)

        return self.response
