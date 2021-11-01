# Imie / Name: Piotr Niedziolka
# Nr indeksu / Index number: 249023
# Praca inzynierska / Engineering Thesis

# Libraries:
import thinkdsp as T_DSP
import thinkplot as T_PLOT
from tkinter import *

#window = Tk()
# Audio start
A_start = 0
# Audio end
A_end = 5

author = 'Piotr'

# Introduction, basic informations
def introduction():
    print(f'> Hi, ' + author) 

# Loading audio to program
def processing():
    print(' >>>> Loading <<<< ')

    name = input("Podaj nazwę pliku: ")
    print(name)

    audio =  T_DSP.read_wave(name + ".wav")
    audio.plot()

    T_PLOT.config(xlim=[A_start, A_end], xlabel="time(s)", legend=False)
    T_PLOT.show()

    audio_spectrum=audio.make_spectrum()
    audio_spectrum.plot()
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


# Main function
if __name__ == '__main__':

    #window.title("Program do analizy")
    #window.geometry("1000x800+50+50")
    #window.resizable(False, False)
    #window.mainloop()

    introduction()
    processing()
 #   example()

    