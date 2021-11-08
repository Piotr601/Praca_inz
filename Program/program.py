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
A_end = 5

author = 'Piotr Niedziolka'

# ----- DECLARING FUNCTIONS ----- #

# Using for clearing screen
def clear():
    _ = system('clear')

# Introduction, basic informations
def introduction():
    print(f' Autor: ' + author) 

# Loading audio to program
def processing(name):
    print(' >>>> Loading <<<< ')

    audio =  T_DSP.read_wave(name)
    audio.plot()

    T_PLOT.config(xlim=[A_start, A_end], xlabel="time(s)", legend=False)
    T_PLOT.show()

    audio_spectrum=audio.make_spectrum()
    audio_spectrum.plot()
    T_PLOT.config(xlim=[0, 1000])
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
    clear()
    name = ""
    introduction()

    # MAIN LOOP with program
    while True:

        choose = input("Co chciałbyś zrobić?\n 1) Wczytanie pliku\n 2) Analiza pliku\n 3) Wyjscie\n Twój wybór: ")
        
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
                processing(name)
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

    