from pathlib import Path
from Settings import Settings

class _Singleton():
    dir = Path(__file__).resolve().parent

    debugging = __debug__ and True
    testing   = debugging and False

    assets = dir / 'assets/'
    ui = dir

    mainWindow = None
    settings = Settings('Alexia')

    loadingGIF = "/home/leonard/Documents/loading.gif"

    importancePrefix = """Change the size of each word in the following text using HTML, according to how important it is:

Input: The quick brown fox jumps over the lazy dog.
Output: <span style="font-size:10px;">The</span>
        <span style="font-size:16px;">quick</span>
        <span style="font-size:16px;">brown</span>
        <span style="font-size:20px;">fox</span>
        <span style="font-size:16px;">jumps</span>
        <span style="font-size:12px;">over</span>
        <span style="font-size:10px;">the</span>
        <span style="font-size:14px;">lazy</span>
        <span style="font-size:18px;">dog</span>

Input: {}
Output:"""
    summaryPrefix = """Summarize this: {}"""
    colorNamesPrefix = """Assign every proper noun in the text a unique integer in the form of a Python dict: {}"""

Singleton = _Singleton()
