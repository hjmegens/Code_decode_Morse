#####################################################################
# python Morse_message_to_wav.py -s 20 -m 'WHAT HATH GOD WROUGHT' -o What_hath_God_wrought_test.wav
#
#   .-- .... .- - / .... .- - .... / --. --- -.. / .-- .-. --- ..- --. .... - 
#     W    H  A T /    H  A T    H /   G   O   D /   W   R   O   U   G    H T 
#
# WHAT HATH GOD WROUGHT
#
#####################################################################
# import libs
import argparse
from scipy.io import wavfile
import scipy.io
import numpy as np

morse_code = {'A': '.-',
              'B': '-...',
              'C': '-.-.',
              'D': '-..',
              'E': '.',
              'F':'..-.',
              'G': '--.',
              'H':'....',
              'I':'..',
              'J':'.---',
              'K':'-.-',
              'L':'.-..',
              'M':'--',
              'N':'-.',
              'O':'---',
              'P':'.--.',
              'Q':'--.-',
              'R':'.-.',
              'S':'...',
              'T':'-',
              'U':'..-',
              'V':'...-',
              'W':'.--',
              'X':'-..-',
              'Y':'-.--',
              'Z':'--..',
              '1':'.----',
              '2':'..---',
              '3':'...--',
              '4':'....-',
              '5':'.....',
              '6':'-....',
              '7':'--...',
              '8':'---..',
              '9':'----.',
              '0':'-----',
              '?':'..--..',
              '/':'-..-.',
              '=':'-...-',
              '-':'-....-',
              '_':'..--.-',
              '.':'.-.-.-',
              ',':'--..--',
              '(':'-.--.',
              ')':'-.--.-',
              ':':'---...',
              '"':'.-..-.',
              "'":'.----.',
              '@':'.--.-.',
              '$':'...-..-',
              'error':'........',
              'end of work':'...-.-',
              'starting signal':'-.-.-',
              'new page signal':'.-.-.',
              'understood':'...-.',
              'wait':'',

             }

####################
# block arguments and parsing
parser = argparse.ArgumentParser( description='Convert text message to Morse audio file')
parser.add_argument("-b", "--bitdepth", help="currently only 16 bits supported",type=int, default=16)
parser.add_argument("-s", "--speed_wpm", help="speed in Words Per Minute",type=int, default=12)
parser.add_argument("-m", "--message", help="start addres", type=str, default='NA')
parser.add_argument("-o", "--output", help="output WAV", type = str, default='out.wav')

args = parser.parse_args()

bitdepth = args.bitdepth
wpm = args.speed_wpm
message = args.message
output_WAV = args.output
# end block args and parsing
####################

# sinusoidal waves
fs = 44100
f = 700 # frequency
tdit = 60/(50 * wpm) # duration of dit (in seconds): "))
tdah = 3 * tdit

dit_samples = np.arange(tdit * fs) / fs
dah_samples = np.arange(tdah * fs) / fs
onedit = np.sin(2 * np.pi * f * dit_samples)
onedah = np.sin(2 * np.pi * f * dah_samples)
onedit *= (2**(bitdepth-1))-1 # 32767
onedah *= (2**(bitdepth-1))-1
onedit = list(onedit)
onedah = list(onedah)

oneintrachar = int(44100 * tdit) * [0]
oneinterchar = 2*oneintrachar # actually 3 but we add this to a standard intrachar
wordspace = 4*oneintrachar # actually 7 but we add this to an interchar

print('\n   ', end = '')
formatted_message = '   '
message_list = list()
for character in message:
    if character in morse_code.keys():
        mc = morse_code[character]
        for signal in mc:
            print(signal, end = '')
            if signal == '.':
                message_list += onedit
            else:
                message_list += onedah
            message_list += oneintrachar
        message_list += oneinterchar
        print(' ', end = '')
        formatted_message += ' '*(len(mc)-1) + character + ' '
    else:
        message_list += wordspace
        print('/ ', end = '')
        formatted_message += '/ '

print('\n' + formatted_message + '\n')
print('\n   ' + message + '\n')
leaderzero = 44100 * 2 * [0]
endzero = 44100 * 2 * [0]
total_vector = np.array(leaderzero + message_list + endzero, dtype='int'+str(bitdepth))

# report total time of the WAV
print("WAV total time: {:.2f} seconds.".format(len(total_vector)/44100))

# write vector to WAV
wavfile.write(output_WAV, 44100, total_vector)


