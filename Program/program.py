# ----- INFORMATION ABOUT AUTHOR ----- #
# Imie / Name: Piotr Niedziolka
# Nr indeksu / Index number: 249023
# Praca inzynierska / Engineering Thesis

# ----- LIBRARIES ----- #
import threading
import time

from os import system, name

import thinkdsp as T_DSP
import thinkplot as T_PLOT
from tkinter import *

# ----- PARAMETERS ----- #

# Audio start
A_start = 0
# Audio end
A_end = 6

author = 'Piotr Niedziolka'

# ----- DECLARING FUNCTIONS ----- #

class AudioProcessing:
    # Using for clearing screen
    def clear():
        _ = system('clear')

    # Introduction, basic informations
    def introduction():
        print(f' Autor: ' + author) 

    # Loading audio to program
    def processing(name):
        print(' > Przetwarzanie . . . \nAby wykonac nastepna akcje prosze zamknac okno Matplotlib ')

        # Printing wave
        T_PLOT.preplot(rows=3, cols=2)
        T_PLOT.config(xlim=[A_start, A_end], xlabel="time(s)", ylabel="Amplitude", legend=False)
        audio =  T_DSP.read_wave(name)
        audio.scale(10)
        audio.plot()

        T_PLOT.subplot(2)
        T_PLOT.config(xlim=[A_start, A_end], xlabel="time(s)", ylabel="Amplitude", legend=False)
        audio2 =  T_DSP.read_wave("corr.wav")
        audio2.scale(10)
        audio2.plot()

        # Counting 
        suma = 0

        for x in audio.ys:
            suma += abs(x)

        aprox = suma / audio.ys.size

        print(aprox)
        print(audio.ys.size)

        ### Results:
        # Lateas	
        # 0.9551936720431643
        # 423936
        #
        # Mr 
        # 1.276661303947049
        # 425088
        #
        # Corr
        # 0.336043370802107
        # 425088
        ###

        # Printing spectrums
        T_PLOT.subplot(3)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()
        audio_spectrum.low_pass(cutoff=73, factor=0.01)
        audio_spectrum.plot()
        
        T_PLOT.subplot(4)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio2_spectrum=audio2.make_spectrum()
        audio2_spectrum.plot()
        
        T_PLOT.show()

# Function, basic information to analysis
# def example(): 
#    sinus_signal = T_DSP.SinSignal(freq=1)
#    
#    wave = sinus_signal.make_wave(duration=1, framerate=11025)
#    wave.plot()
#
#    T_PLOT.config(xlabel="-", legend=False)
#    T_PLOT.show()

#window = Tk()

# ----- MAIN FUNCTION ----- #
if __name__ == '__main__':
    AudioProcessing.clear()
    name = ""
    AudioProcessing.introduction()

    # MAIN LOOP with program
    while True:

        choose = input("\nCo chciałbyś zrobić?\n 1) Wczytanie pliku\n 2) Analiza pliku\n 3) Wyjscie\n Twój wybór: ")
        
        # Choosing audio to analysis
        if choose=='1':
            # Preventing wrong or no audio to analyse
            while True:
                try:
                    print("\nDostepne pliki:")
                    # Printing all audios in folder
                    _ = system('ls -m *.wav')
                    name = input("Podaj nazwę pliku: ")
                    
                    # Preventing eneter a name with format
                    for x in name:
                        if name.endswith('.wav'):
                            name = name
                        else:
                            name = name + ".wav"

                    file = open(name, 'rb')
                    break
                except OSError:
                    print("Cannot read file |", name ,"| try again")
                
        # Analysis audio
        elif choose=='2':
            if name != "":
                AudioProcessing.processing(name)
            else:
                print("Nie wczytano pliku\n")

        # Exit
        elif choose=='3':
            exit(0)

        else:
            print()    

    #window.title("Program do analizy")
    #window.geometry("1000x800+50+50")
    #window.resizable(False, False)
    #window.mainloop()
    #x.join()

    # example()

    