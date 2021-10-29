# Imie / Name: Piotr Niedziolka
# Nr indeksu / Index number: 249023
# Praca inzynierska / Engineering Thesis

# Libraries:
import thinkdsp as T_DSP
import thinkplot as T_PLOT

name = 'Piotr'

# Introduction, basic informations
def introduction():
    print(f'Hi, ' + name)


# Loading audio to program
def audio_loading():
    print('Loading')


# Function, basic information to analysis
def processing(): 
    sinus_signal = T_DSP.SinSignal(freq=1)
    T_PLOT.config(xlabel="time(s)", legend=False)
    wave = sinus_signal.make_wave(duration=1, framerate=11025)
    wave.plot()
    T_PLOT.show()

# Main function
if __name__ == '__main__':
    introduction()
    audio_loading()
    processing()