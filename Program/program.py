# Imie / Name: Piotr Niedziolka
# Nr indeksu / Index number: 249023
# Praca inzynierska / Engineering Thesis

# Libraries:
import thinkdsp as T_DSP
import thinkplot as T_PLOT

name = 'Piotr'


def introduction():
    # Introduction
    print(f'Hi, ' + name)


def processing():
    # Here all function/information about ThinkDSP
    sinus_signal = T_DSP.SinSignal(freq=1)
    T_PLOT.config(xlabel="time(s)", legend=False)
    wave = sinus_signal.make_wave(duration=1, framerate=11025)
    wave.plot()
    T_PLOT.show()


if __name__ == '__main__':
    # Main function
    introduction()
    processing()