# import libs
import sys
import argparse
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

morse_code_rev = {
                  '.-':    'A',
                  '-...':  'B',
                  '-.-.':  'C',
                  '-..':   'D',
                  '.':     'E',
                  '..-.':  'F',
                  '--.':   'G',
                  '....':  'H',
                  '..':    'I',
                  '.---':  'J',
                  '-.-':   'K',
                  '.-..':  'L',
                  '--':    'M',
                  '-.':    'N',
                  '---':   'O',
                  '.--.':  'P',
                  '--.-':  'Q',
                  '.-.':   'R',
                  '...':   'S',
                  '-':     'T',
                  '..-':   'U',
                  '...-':  'V',
                  '.--':   'W',
                  '-..-':  'X',
                  '-.--':  'Y',
                  '--..':  'Z',
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
                  '..--..':'?',
                  '-..-.': '/',
                  '-...-': '=',
                  '-....-':'-',
                  '..--.-':'_',
                  '.-.-.-':'.',
                  '--..--':',',
                  '-.--.': '(',
                  '-.--.-':')',
                  '---...':':',
                  '.-..-.':'"',
                  '.----.':"'",
                  '.--.-.':'@',
                  '...-..-':'$',
                  '........':'error',
                  '...-.-':'end of work',
                  '-.-.-':'starting signal',
                  '.-.-.':'new page signal',
                  '...-.':'understood'
                 }

# plot specgram, if --make_plots
def plot_specgram(signal_data, sampling_frequency,outfilestub):

    # Plot the signal read from wav file
    plt.figure(figsize=(16, 8), dpi=300)

    plt.title('Spectrogram of a wav file for Morse code')
    spectrum,freqs,t,d = plt.specgram(signal_data[1:],Fs=sampling_frequency,scale='dB',cmap='Spectral')
    plt.xlabel('Time')
    plt.ylim(0,5000)
    plt.ylabel('Frequency')
    plt.savefig(outfilestub + '_specgram.png')
    return(spectrum,freqs,t)

# plot the FFT, if --make_plots
def plot_fft(sound, sampling_freq, outfilestub):
    fft_spectrum = np.fft.rfft(sound)
    freq = np.fft.rfftfreq(sound.size, d=1./sampling_freq)
    fft_spectrum_abs = np.abs(fft_spectrum)
    plt.figure(figsize=(16, 5), dpi=300)
    plt.plot(freq[freq<1500], fft_spectrum_abs[freq<1500])
    print('peak frequency is at: {:.2f} Hz.'.format(freq[np.where(fft_spectrum_abs == np.amax(fft_spectrum_abs))[0]][0]))
 
    plt.title('FFT of Morse code, peak at {:.2f} Hz'.format(freq[np.where(fft_spectrum_abs == np.amax(fft_spectrum_abs))[0]][0]))
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.ylim(0,1.1*fft_spectrum_abs[freq>0].max())
    plt.xlim(0,1500)
    plt.savefig(outfilestub + '_fft.png')

# output some diagnostic plot of the waveform
#def plot_start(starttime,time,sound,outfilestub,title):
def plot_waves(time,sound,title):
    plt.figure(figsize=(16, 5), dpi=300)
    plt.plot(time, sound)
    plt.title(title)
    #plt.savefig(outfilestub + '_start_waves_short.png')

# output some diagnostic plot of the waveform
def plot_start(starttime,time,sound,title):
    newvec = (time>starttime) & (time<(starttime+0.02))
    plt.figure(figsize=(16, 5), dpi=300)
    plt.plot(time[newvec], sound[newvec])
    plt.title(title)

def plot_signal_time_histogram(signals, directions, outfilestub, wpm):
    plt.figure(figsize=(10, 5), dpi=300)
    n, bins,a = plt.hist(signals[directions == 'up'],bins=100)
    maxima = bins[np.where(n > 0.5* n.max())]
    plt.title('Distribution of signal time durations\nspeed: {:.2f} wpm'.format(wpm))
    xlabel = "Signal duration, in sec.\nmaxima at : "+'{:.3f} '*len(maxima)
    plt.xlabel(xlabel.format(*tuple(maxima)))
    plt.ylabel("counts")
    plt.savefig(outfilestub + '_signal_duration_histogram.png')

# return data vector and sample rate from wav
def return_data_from_wav(input_file):

    wav = wavfile.read(input_file)
    samplerate = wav[0]
    data = wav[1]
    sound = ''
    # assuming mono, if stereo deciding which channel
    # note: there is a potential weakness; if mute channel
    # has still lots of noise it could be inadvertently selected
    # this needs some work to make full-proof. 
    if len(data.shape) == 2:
           maxsignal1 = data[:,0].max()
           maxsignal2 = data[:,1].max()
           if maxsignal1 >= maxsignal2:
               sound = data[:,0]
           else:
               sound = data[:,1]
    elif len(data.shape) == 1:
        sound = data
    maxsignal = sound.max()
    minsignal = sound.min()
    
    if minsignal >= 0:
        sound2 = list()
        for value in sound:
            sound2.append(value - int(0.5*maxsignal)+1)
        sound = np.array(sound2)
        minsignal = sound.min()
        maxsignal = sound.max()
    length = sound.shape[0] / samplerate # aantal seconden
    time = np.linspace(0., length, sound.shape[0])
    return sound,maxsignal,minsignal,time,samplerate


####################
# block arguments and parsing
parser = argparse.ArgumentParser( description='Convert  Morse audio file to message')
parser.add_argument("-w", "--wav_file", help="start addres", type=str, default='NA')
parser.add_argument("-o", "--output", help="output stub", type = str, default='out.wav')

args = parser.parse_args()

wav_file = args.wav_file
outfilestub = args.output
# end block args and parsing
####################

sound,maxsignal,minsignal,time,samplerate = return_data_from_wav(wav_file)

spectrum,freqs,t = plot_specgram(sound,samplerate, outfilestub)

plot_fft(sound, samplerate, outfilestub)

testval = 0.5 * spectrum[4,].max()
switchup = False
switchdown = False
firstsignal = False
signals = list()
directions = list()
for i,value in enumerate(spectrum[4,]):
    if value > testval and not switchup:
        #print(t[i], 'up')
        switchup = True
        switchdown = False
        startup = t[i]
        if firstsignal == True:
            enddown = t[i]
            signals.append(enddown - startdown)
            directions.append('down')
        if firstsignal == False:
            firstsignal = True
            t_first = t[i]

    if value < testval and not switchdown and firstsignal:
        #print(t[i],'down')
        switchup = False
        switchdown = True
        endup = t[i]
        startdown = t[i]
        signals.append(endup - startup)
        directions.append('up')

print('\nfirst signal: {:.3f}'.format(t_first))

directions = np.array(directions)
signals = np.array(signals)
shortsignal = ( signals[directions == 'up'].min() + signals[directions == 'down'].min() ) / 2

print('\nestimated duration of dit: {:.3f} seconds\n'.format(shortsignal))
wpm = (60/shortsignal)/50
print('estimated wpm: {:.2f}\n'.format(wpm))

plot_signal_time_histogram(signals, directions, outfilestub, wpm)

morsecode = ''
for j,signal in enumerate(signals):
    #print(signal, directions[j])
    if signal < 1.2 * shortsignal and signal > 0.8 * shortsignal and directions[j] == 'up':
        morsecode += '.'
    elif signal < 1.2 * shortsignal and signal > 0.8 * shortsignal and directions[j] == 'down':
        morsecode += ''
    elif signal < 1.2 * shortsignal * 3 and signal > 0.8 * shortsignal * 3 and directions[j] == 'up':
        morsecode += '-'
    elif signal < 1.2 * shortsignal * 3 and signal > 0.8 * shortsignal * 3 and directions[j] == 'down':
        morsecode += ' '
    elif signal < 1.2 * shortsignal * 7 and signal > 0.8 * shortsignal * 7 and directions[j] == 'down':
        morsecode += ' / '

print(' ' + morsecode)

words = morsecode.split(' / ')
morse_message = ''
formatted_message = ''
for word in words:
    letters = word.split(' ')
    for letter in letters:
        #print(letter, morse_code_rev[letter])
        formatted_message += ' '*len(letter) + morse_code_rev[letter]
        morse_message += morse_code_rev[letter]
    morse_message += ' '
    formatted_message += ' /'

print(formatted_message)
print('\n' + morse_message)

