# ----- INFORMATION ABOUT AUTHOR ----- #
# Imie / Name: Piotr Niedziolka
# Nr indeksu / Index number: 249023
# Praca inzynierska / Engineering Thesis

# ----- LIBRARIES ----- #
import threading
import time

from matplotlib import pyplot as plt
from array import *
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
        T_PLOT.preplot(rows=4, cols=2)
        T_PLOT.config(xlim=[A_start, A_end], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio =  T_DSP.read_wave(name)
        audio.scale(10)
        audio.plot(color='blue')

        T_PLOT.subplot(2)
        T_PLOT.config(xlim=[A_start, A_end], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio2 =  T_DSP.read_wave("corr.wav")
        audio2.scale(10)
        audio2.plot(color='red')


        ### Counting 
        
        ## Drawing first chart

        suma, aud_sum, i, k = 0, 0, 0, 0
        taba = []
        tabb = []

        T_PLOT.subplot(7)
        for x in audio.ys:
            suma += abs(x)
            aud_sum += abs(x)
            
            if(k % 500 == 0):
                aud_apr = aud_sum/500
                
                taba.append(aud_apr)
                tabb.append(i)
                    
                i += 1
                aud_sum = 0

            k += 1
        aprox = suma / audio.ys.size 
            
        T_PLOT.Plot(tabb, taba, color='black') 

        print("\nAprox: " + str(aprox))
        print(" Size: " + str(audio.ys.size))

        # Drawing aprox line
        for y in tabb:
            T_PLOT.Plot(y, aprox, color='green', marker='_') 
        
        ## Drawing second chart

        suma, aud_sum, i, k = 0, 0, 0, 0
        taba = []
        tabb = []

        T_PLOT.subplot(8)
        for x in audio2.ys:
            suma += abs(x)
            aud_sum += abs(x)
            
            if(k % 500 == 0):
                aud_apr = aud_sum/500

                taba.append(aud_apr)
                tabb.append(i)
                    
                i += 1
                aud_sum = 0

            k += 1
        aprox = suma / audio2.ys.size 
        T_PLOT.Plot(tabb, taba, color='black')  

        # Drawing a aprox line
        for y in tabb:
            T_PLOT.Plot(y, aprox, color='green', marker='_') 

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
        audio_spectrum.plot(color='blue')

        T_PLOT.subplot(5)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum.low_pass(cutoff=73, factor=0.01)
        audio_spectrum.plot(color='blue')
        
        T_PLOT.subplot(4)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio2_spectrum=audio2.make_spectrum()
        audio2_spectrum.plot(color='red')

        T_PLOT.subplot(6)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]") #ylim=[0,60000]
        audio2_spectrum.low_pass(cutoff=73, factor=0.01)
        audio2_spectrum.plot(color='red')

        T_PLOT.show()

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