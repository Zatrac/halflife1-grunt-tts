# Half life 1 grunt sound concatenatetor - Zatrac 2019
import os

try:
    from pydub import AudioSegment
except ImportError:
    print('You are missing the required modules, attempting to install..')
    os.system('python -m pip install pydub')

from pydub import AudioSegment

sentence = []
DONE = False
COLUMN_WIDTH = 4

def get_files(extensions):
    '''
    Returns an array of the audio files with or without the format extension
    params: True or False
    '''
    files = []
    if extensions == True:
        for filename in os.listdir(os.getcwd() + '/audio'):
            files.append(filename)
        return files
    else:
        for filename in os.listdir(os.getcwd() + '/audio'):
            filename = filename.split('.')
            files.append(filename[0])
        return files


def display_words(files):
    '''
    Displays an array of strings in columns 
    depending on the length of the input array
    '''
    s = ""
    for i in range(len(files)):
        if i == len(files) - 1:
            s += '%20s' % (files[i])
        else:
            s += '%20s %5s' % (files[i], '|')
    print(s)


def validate(attempt):
    ''' 
    Looks for the users choice of sound file to append
    in the audio file directory
    '''
    for word in get_files(False):
        if attempt == word:
            return True
    return False


def query_audio():
    '''
    Sets up multiple strings for display_words()
    '''
    words = []
    for filename in get_files(False):     
        READY = False
        words.append(filename)

        if len(words) > COLUMN_WIDTH:
            READY = True

        if READY:
            display_words(words)
            words = []


def compile_sentence(sentence):
    '''
    Adds together the users choice of words
    and compiles to an output file also 
    allows the user to change the pitch of the output
    '''
    print('0 for default | Negative values for low pitch (recmnd. -.1 to -1) | Positive for high pitch (recmnd. .1 to 1)')
    pitch = float(input('Pitch: '))

    sounds = []
    filename = ''
    compiled = AudioSegment.empty()

    for word in sentence:
        filename += word[0]
        sounds.append(os.getcwd() + '/audio' + '/' + word + '.wav')

    for sound in sounds:
        compiled += AudioSegment.from_wav(sound)

    sample_rate_enchance = int(compiled.frame_rate * (2.0 ** pitch))
    compiled = compiled._spawn(compiled.raw_data, overrides={'frame_rate': sample_rate_enchance})

    filename += '.wav'
    compiled.export(filename, format='wav')
    print('Succesfully compiled as', filename + '!')



while not DONE:
    os.system('cls')
    query_audio()

    print('\n\nType done when finished | Single word at a time | No change means invalid word')

    if len(sentence) > 0:
        s = ''
        print('Current sentence: ', end='')
        for word in sentence:
            s += word + ' '
        print(s)

    choice = input('Word to append: ')

    if(choice.lower() == 'done'):
        DONE = True
    else:
        if validate(choice):
            sentence.append(choice)
        else:
            pass

else:
    compile_sentence(sentence)