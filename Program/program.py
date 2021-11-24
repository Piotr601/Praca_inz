# -------------------------------------- #
# -------- INFORMACJE O AUTORZE -------- #
# ----- (INFORMATION ABOUT AUTHOR) ----- #
# -------------------------------------- #
#     Imie / Name: Piotr Niedziolka      #
#   Nr indeksu / Index number: 249023    #
# Praca inzynierska / Engineering Thesis #
# -------------------------------------- #

# -------------------------------------- #
# ------------- BIBLIOTEKI ------------- #
# ------------ (LIBRARIES) ------------- #
# -------------------------------------- #

import threading
import time

from matplotlib import pyplot as plt
from array import *
from os import system, name

import thinkdsp as T_DSP
import thinkplot as T_PLOT
from tkinter import *

# -------------------------------------- #
# -------------- PARAMETRY ------------- #
# ------------ (PARAMETERS) ------------ #
# -------------------------------------- #

# Start audio na pierwszym wykresie 
A_start = 0
# Koniec audio na pierwszym wykresie
A_end = 6

author = 'Piotr Niedziolka'

# -------------------------------------- #
# -------------- FUNKCJE --------------- #
# ------- (DECLARING FUNCTIONS) -------- #
# -------------------------------------- #

class AudioProcessing:
    # Funkcja uzywana w celu czyszczenia ekranu
    def clear():
        _ = system('clear')

    # Wstep, podstawowe informacje
    def introduction():
        print(f' Autor: ' + author) 

    # Analizowanie audio
    def processing(name):
        AudioProcessing.clear()
        print(' > Przetwarzanie . . . \nAby wykonac nastepna akcje prosze zamknac okno Matplotlib ')

        # Zadeklarowanie wielkosci okna do wyswietlania
        T_PLOT.preplot(rows=4, cols=2)
        
        # Wyswietlanie wczytanych plikow
        # 01 Wykres
        T_PLOT.config(xlim=[A_start, A_end], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio =  T_DSP.read_wave(name)
        audio.scale(10)
        audio.plot(color='blue')

        # 02 Wykres
        T_PLOT.subplot(2)
        T_PLOT.config(xlim=[A_start, A_end], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio2 =  T_DSP.read_wave("corr.wav")
        audio2.scale(10)
        audio2.plot(color='red')


        ### Rysowanie czarnych wykresow do analizy
        ## Pierwszy czarny wykres
        # Pomocnicze zmienne do analizy
        przec, x_pop, przec_sum, przec_kontr = 0, 0, 0, 0
        suma, aud_sum, i, k = 0, 0, 0, 0
        taba = []
        tabb = []

        # 07 Wykres
        # Polega na wyliczeniu sredniej z wartosci bezwzglednej,
        # a nastepnie co 500 probek brana jest srednia, dzieki
        # ktorej pozniej calosc jest nanoszona na wykres.
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
        # Srednia sygnalu
        aprox = suma / audio.ys.size 
        # Rysowanie sygnalu
        T_PLOT.Plot(tabb, taba, color='black') 

        # Wypisanie sredniej i wielkosci audio (ilosc probek - calosc)
        print("\nAprox: " + str(aprox))
        print(" Size: " + str(audio.ys.size) + '\n')

        # Rysowanie sredniej na wykresie - zielony kolor
        for y in tabb:
            T_PLOT.Plot(y, aprox, color='green', marker='_')


        # Przechodzenie przez wszystkie wartosci
        # Pozniej nastepuje zliczanie punktow ktore przechodza przez srednia - aprox
        # Zwracana jest ilosc przechodzenia w jednym cyklu
        # =  4  poprawna wartosc
        # >= 6  niepoprawne wartosci - wystepuje szum zaklocajacy
        for x in taba:
            # Gdy wykres przecina sie rosnac
            if ((x_pop < aprox) and (x > aprox)):
                przec += 1
                przec_sum+=1
            # Gdy wykres przecina sie malejac
            elif((x_pop > aprox) and (x < aprox)):
                przec += 1
                przec_sum+=1
            x_pop = x

            # Gdy spelnione sa dwa warunki, to jest ilosc przeciec jest wieksza, badz
            # rowna niz 4 i jest mniejsza od parametru (aby oddzielic kolejne cykle)
            if (przec >= 4 and x <= 0.1*aprox):
                print(' 01 Przeciecia w jednym uderzeniu: ' + str(przec))
                # Zmienna pomocnicza - kontrolna
                przec_kontr += przec 

                # Gdy wystepuje wiecej niz 4 przeciecia (inaczej niz norma)
                if (przec > 4):
                    print(" > Uwaga tutaj prawdopodobnie wystepuja szumy")

                przec = 0

        # Wypisywanie ilosc przeciec i liczby kontrolnej
        # Gdy obydwie liczby sie zgadzaja, program zlicza wszystkie uderzenia
        # i dziala prawidlowo        
        print('Przeciecia 1: ' + str(przec_sum) + '\n  Kontrolnie: ' + str(przec_kontr) + '\n')      

        ## Drugi czarny wykres
        # Pomocnicze zmienne do analizy
        # Wyzerowanie wartosci
        przec, x_pop, przec_sum, przec_kontr = 0, 0, 0, 0
        suma, aud_sum, i, k = 0, 0, 0, 0
        taba = []
        tabb = []

        # 08 Wykres
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

        # Rysowanie sredniej na wykresie - zielony kolor
        for y in tabb:
            T_PLOT.Plot(y, aprox, color='green', marker='_') 

        # Przechodzenie przez wszystkie wartosci
        for x in taba:
            if ((x_pop <= aprox) and (x > aprox)):
                przec += 1
                przec_sum +=1
            elif((x_pop >= aprox) and (x < aprox)):
                przec += 1
                przec_sum += 1
            x_pop = x

            if (przec >= 4 and x <= 0.1*aprox):
                print(' 02 Przeciecia w jednym uderzeniu: ' + str(przec))
                przec_kontr += przec 

                if (przec > 4):
                    print(" > Uwaga tutaj prawdopodobnie wystepuja szumy")
                
                przec = 0
            
        print('Przeciecia 2: ' + str(przec_sum) + '\n  Kontrolnie: ' + str(przec_kontr) + '\n')    

        # 03 Wykres
        # Rysowanie spektrum wczytanego audio
        T_PLOT.subplot(3)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()

        # Maksymalna wartość Amplitudy w Hz
        # print(abs(max(audio_spectrum.hs)))

        audio_spectrum.plot(color='blue')

        # 05 Wykres
        # Rysowanie spektrum z filtrem dolnoprzepustowym
        T_PLOT.subplot(5)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum.low_pass(cutoff=73, factor=0.01)
        audio_spectrum.plot(color='blue')
        
        # 04 Wykres
        # Rysowanie spektrum poprawnego bicia serca
        T_PLOT.subplot(4)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio2_spectrum=audio2.make_spectrum()
        audio2_spectrum.plot(color='red')

        # 06 Wykres
        # Rysowanie spektrum z filtrem dolnoprzepustowym
        T_PLOT.subplot(6)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]") #ylim=[0,60000]
        audio2_spectrum.low_pass(cutoff=73, factor=0.01)
        audio2_spectrum.plot(color='red')

        # Wysietla wszystkie wykresy
        T_PLOT.show()


# window = Tk()
# -------------------------------------- #
# ----- FUNKCJA MAIN - GŁÓWNA PĘTLA ---- #
# ----------- (MAIN FUNCTION) ---------- #
# -------------------------------------- #

if __name__ == '__main__':

    name = ""
    AudioProcessing.clear()
    AudioProcessing.introduction()

    # Glowna petla z programem
    while True:

        choose = input("\nCo chciałbyś zrobić?\n 1) Wczytanie pliku\n 2) Analiza pliku\n 3) Wyjscie\n Twój wybór: ")
        
        # Wybranie i wczytywanie sciezki audio do analizy
        if choose=='1':
            # Zapobieganie wpisaniu zlej nazwy oraz braku wybrania audio do analizy
            while True:
                try:
                    print("\nDostepne pliki:")
                    # Wyswietlenie wszystkich dostepnych audio w programie
                    _ = system('ls -m *.wav')
                    name = input("Podaj nazwę pliku: ")
                    
                    # Zapobieganie wpisaniu nazwy audio bez formatu
                    for x in name:
                        if name.endswith('.wav'):
                            name = name
                        else:
                            name = name + ".wav"

                    file = open(name, 'rb')
                    break
                except OSError:
                    print("Cannot read file |", name ,"| try again")
                
        # Uruchomienie funkcji z analiza audio
        elif choose=='2':
            if name != "":
                AudioProcessing.processing(name)
            else:
                print("Nie wczytano pliku\n")

        # Wyjscie z programu
        elif choose=='3':
            exit(0)

        else:
            AudioProcessing.clear()
            print(" Bledny wybor, wybierz ponownie! ")    

    #window.title("Program do analizy")
    #window.geometry("1000x800+50+50")
    #window.resizable(False, False)
    #window.mainloop()
    #x.join()

# -------------------------------------- #
# --------------- KONIEC --------------- #
# --------------- (END) ---------------- #
# -------------------------------------- #
