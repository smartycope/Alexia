from PyQSettings import PyQSettings, Option, OptionWidgets
from PyQt6.QtGui import QColor, QKeySequence, QBrush, QPen
from PyQt6.QtCore import QStandardPaths, Qt
from pathlib import Path

class Settings(PyQSettings):
    documentsPath = Path(QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DocumentsLocation)[0]).resolve() / 'GeoDoodle'
    defaults = {
        # Parameters
        'advanced/importance_temperature': 0.,
        'advanced/summarize_temperature': 0.5,
        'advanced/color_names_temperature': 0,
        # In tokens (like short words)
        'advanced/max_len': 2048,
        'advanced/model': "text-davinci-003",
        'advanced/frequency_penalty': 0,
        'advanced/presence_penalty': 0,
        'advanced/API_Key': "", # Add API key here
        'font': Path('/home/leonard/Documents/open-dyslexic-font.zip')
    }
