def doThing(text):
    print(f'thing done! {text}')

def updateText(text):
    print('1')
    textFormatter = _formatText(text)
    next(textFormatter)
    print('2')

def _formatText(text):
    print('3')
    yield doThing(text)
    print('4')
    return True

updateText('text')
