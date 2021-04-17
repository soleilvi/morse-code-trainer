from pynput.keyboard import Key, Listener
from pygame import mixer
from tkinter import *
import numpy as np
import time


def on_key_press(key):
    '''
    Adds spaces/separates characters according to the time between key presses.

    When a key is pressed, the function calculates the length of time between
    key presses and separates the letters or adds a space depending on how long
    the time was between key presses.
    '''
    global transCode
    global dsplyCode
    global morseChar
    global txt

    if transCode == '':
        pass
    else:
        timeTaken = round(time.time() - btwnPress, 2)

        if timeTaken in range3Units:
            dsplyCode = dsplyCode + ' '
            morseChar = ' '
            transCode = ''  # Reset to avoid translation errors.

        elif timeTaken >= 0.35:
            txt = txt + ' '
            dsplyCode = dsplyCode + ' / '
            morseChar = ' / '
            transCode = ''

    return False  # Stop detecting more key-presses.


def on_key_release(key):
    '''
    Determines the morse code characters based on key press timing.

    When a key is released, the function calculates the length of time the key
    was pressed, determines whether the key was a "special" key (Esc or Delete),
    and decides what character to add to the morse code depending on how long
    the key was pressed.
    '''
    global transCode
    global dsplyCode
    global morseChar
    global txt

    timeTaken = round(time.time() - whenPressed, 2)

    # End program if Esc is pressed.
    if key == Key.esc:
        global x
        x = False

     # Reset all string values if "R" is pressed.
    elif key == Key.backspace:
        dsplyCode = 'MORSE CODE:\n'
        txt = 'TRANSLATION:\n`'
        morseChar = ''
        transCode = ''
        return False

    # Update the morse code strings with a dot if the time pressed = 1 unit
    elif timeTaken in range1Unit:
        transCode = transCode + '.'
        dsplyCode = dsplyCode + '.'
        morseChar = '.'

    elif timeTaken in range3Units:
        transCode = transCode + '-'
        dsplyCode = dsplyCode + '-'
        morseChar = '-'

    else:
        mixer.music.load('amogus.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(loops=0)
        morseChar = ':('
        return False  # End so that it doesn't translate the same letter again

    change_txt()

    return False  # stop detecting more key-releases


def change_txt():
    '''Updates the translation text in real-time as the user presses a key.'''
    global txt

    if transCode == '':
        pass
    else:
        # Skip if there has already been a break between letters or if the \
        # letter has already been determined
        if ' ' in dsplyCode[-2:]:
            if transCode in morseKey.keys():
                txt += morseKey[transCode]
            else:
                pass

        # Update the letters as the user types (until there is a space)
        elif transCode in morseKey.keys():
            if txt[-1:] != ' ':  # Has to have a colon because otherwise, the \
            # program crashes if the txt string isn't that long yet
                txt = txt[:-1] + morseKey[transCode]
            else:
                if txt[-2:] == '  ':
                    txt = txt[:-1] + morseKey[transCode]
                else:
                    txt += morseKey[transCode]

        # Prevents the program from passing an unknown morse value.
        else:
            end_program()


def end_program():
    global x
    endDialogue = 'Haha wow, you\'ve really fucked up! I\'ll just end the ' \
                  'program here so that neither of us have to suffer more.\n' \
                  '\nERROR PHRASE: ' + transCode
    print(endDialogue)
    x = False


# WINDOW AND SOUND INITIATION #
root = Tk()
root.geometry('1105x695')
root.title('Morse Code Trainer')
mixer.init()

# VARIABLE DEFINITION #
transCode = ''
morseChar = ''
dsplyCode = 'MORSE CODE:\n'
txt = 'TRANSLATION:\n`'  # "`" necessary to combat logic in change_txt()
instr = 'INSTRUCTIONS:\n\n' \
'Press "Esc" to exit the program\n\n' \
'Press "ENTER" to return a line\n\n' \
'Press "DELETE" to clear the message in your current line\n\n' \
'If you hear a sound, it\'s because you messed up your press timing.'

range1Unit = np.round(np.arange(0.04, 0.10, 0.01), 2)  # Increment by .01 and \
range3Units = np.round(np.arange(0.12, 0.28, 0.01), 2)  # round to 2 decimals

morseKey = {'.-': 'A',
            '-...': 'B',
            '-.-.': 'C',
            '-..': 'D',
            '.': 'E',
            '..-.': 'F',
            '--.': 'G',
            '....': 'H',
            '..': 'I',
            '.---': 'J',
            '-.-': 'K',
            '.-..': 'L',
            '--': 'M',
            '-.': 'N',
            '---': 'O',
            '.--.': 'P',
            '--.-': 'Q',
            '.-.': 'R',
            '...': 'S',
            '-': 'T',
            '..-': 'U',
            '...-': 'V',
            '.--': 'W',
            '-..-': 'X',
            '-.--': 'Y',
            '--..': 'Z',
            '.----': '1',
            '..---': '2',
            '...--': '3',
            '....-': '4',
            '.....': '5',
            '-....': '6',
            '--...': '7',
            '---..': '8',
            '----.': '9',
            '-----': '0',
            '.-.-.-': '.',
            '--..--': ',',
            '..--..': '?',
            ' / ': ' '}

# FORMATTING #
title = Label(root,
              font=('Arial', 25),
              text='Morse Code Trainer')
charBoxText = Label(root,
                    font=('Arial', 14),
                    text='CHARACTER PREVIEW')
morseBox = Label(root,
                 width=115, height=20,
                 relief=GROOVE, anchor='nw', bg='white')
transBox = Label(root,
                 width=115, height=20,
                 relief=GROOVE, anchor='nw', bg='white')
instrBox = Label(root,
                 width=35, height=20,
                 relief=GROOVE, bg='white')
charBox = Label(root,
                width=6, height=2,
                font=('Arial', 50), relief=GROOVE, bg='white')

# Yes, message boxes on top of the labels. Shut up.
morseCode = Message(root,
                    width=805,
                    bg='white',
                    text=dsplyCode)
translation = Message(root,
                      width=805,
                      bg='white',
                      text=txt)
instructions = Message(root,
                       width=230,
                       bg='white',
                       text=instr)

title.grid(row=0, column=1,
           padx=10, pady=2,
           sticky='W')
morseBox.grid(row=1, column=1,
              padx=15, pady=5)
transBox.grid(row=3, column=1,
              rowspan=3,
              padx=15, pady=12)
instrBox.grid(row=1, column=3,
              pady=5)
charBoxText.grid(row=4, column=3,
                 sticky='S')
charBox.grid(row=5, column=3,
             rowspan=2,
             pady=12,
             sticky='S')
morseCode.grid(row=1, column=1,
               padx=17, pady=10,
               sticky='NW')
translation.grid(row=3, column=1,
                 rowspan=3,
                 padx=17, pady=17,
                 sticky='NW')
instructions.grid(row=1, column=3,
                  padx=2, pady=10,
                  sticky='NW')

# MAIN CODE #
x = True
while x is True:
    btwnPress = time.time()

    # setting code for listening key-press
    with Listener(on_press=on_key_press) as press_listener:
        press_listener.join()

    whenPressed = time.time()

    # setting code for listening key-release
    with Listener(on_release=on_key_release) as release_listener:
        release_listener.join()

    # Update labels as you press a button
    morseCode.config(text=dsplyCode)
    translation.config(text=txt)
    charBox.config(font=('Arial', 50), text=morseChar)

    # Paired with root.update(), root.update_idletasks() mimics \
    # root.mainloop(), but allows the program to continue running commands.
    root.update_idletasks()
    root.update()
