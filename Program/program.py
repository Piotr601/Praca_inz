# -------------------------------------- #
# -------- INFORMACJE O AUTORZE -------- #
# ----- (INFORMATION ABOUT AUTHOR) ----- #
# -------------------------------------- #
# *    Imie / Name: Piotr Niedziolka   * #
# *  Nr indeksu / Index number: 249023 * #
# Praca inzynierska / Engineering Thesis #
# -------------------------------------- #

# -------------------------------------- #
# ------------- BIBLIOTEKI ------------- #
# ------------ (LIBRARIES) ------------- #
# -------------------------------------- #

# -------------------------------------- #
#            BETTER COMMENTS             #
# * HIGHLIGHTED
# ! Alert ...
# ? Should ....
# TODO sth
# // that
# -------------------------------------- # 

import threading
import time
import math

from scipy.io import wavfile
from matplotlib import pyplot as plt
from array import *
from os import system, name
from numpy.lib.function_base import average

import noisereduce as nr
import thinkdsp as T_DSP
import thinkplot as T_PLOT

import scipy.signal as sig
from tkinter import *

# -------------------------------------- #
# -------------- PARAMETRY ------------- #
# ------------ (PARAMETERS) ------------ #
# -------------------------------------- #

# Start audio na pierwszym wykresie 
A_start = 0
# Koniec audio na pierwszym wykresie
A_end = 6
# Liczba probek brana pod uwage w liczeniu
# srednich wykresow - szare wykresy w analizie
l_probek = 500

# -------------------------------------- #
# -------------- FUNKCJE --------------- #
# ------- (DECLARING FUNCTIONS) -------- #
# -------------------------------------- #

#
# Klasa AudioProcessing sluzaca do obslugi przetwarzania audio
#
# Metody:
#  - clear
#  - introduction
#  - preview
#  - filtration 
#  - processing
#
# W argumentach kilku funkcji przekazywana jest nazwa pliku
# audio wczytana w menu wyboru
#

class AudioProcessing:
    #* Funkcja uzywana w celu czyszczenia ekranu
    def clear():
        _ = system('clear')

    #// TODO wiecej informacji o autorze, o stworzeniu programu itp...
    #* Wstep, podstawowe informacje
    def introduction():
        print('#======================================================================#')
        print('|     Opracowanie i implementacja systemu do analizy szumów serca      |') 
        print('|  Development and Implementation of a Heart Sound Analysis Framework  |')
        print('|                                                                      |')
        print('|                          Automatyka i Robotyka                       |')
        print('|                         Politechnika Wroclawska                      |')
        print('|                              Przemysl 4.0                            |')
        print('|                             Piotr Niedziolka                         |')
        print('#======================================================================#')        
    
    #* Szybki podglad pliku
    def preview(name):
        # Zdefiniowanie okna do wyswietlania
        T_PLOT.preplot(rows=2, cols=1)
        
        # Podglad sciezki audio, wykres amplitudowy
        T_PLOT.config(xlim=[A_start, A_end], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio =  T_DSP.read_wave(name)
        audio.scale(10)
        audio.plot(color='blue')

        # Podglad sciezki audio, wykres czestotliwosciowy
        T_PLOT.subplot(2)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()
        audio_spectrum.plot(color='darkblue')

        T_PLOT.show()

    #* Usuwanie szumow (wstepna filtracja sygnalu)
    #! Nalezy filtrowac tylko i wylacznie gdy wystepuja znaczne szumy 
    #! Blad przy wczytywaniu za duzych plikow  
    def filtration(name):
        # Zdefiniowanie okna do wyswietlania
        T_PLOT.preplot(rows=2, cols=2)

        # Wykres ścieżki audio
        T_PLOT.config(xlim=[A_start, A_end], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio =  T_DSP.read_wave(name)
        rate, data = wavfile.read(name)
        audio.scale(10)
        audio.plot(color='darkblue')

        # CWykres częstotliwościowy audio
        T_PLOT.subplot(3)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()
        audio_spectrum.plot(color='darkblue')

        # Odszumianie niechcianych szumów
        # ! Uwaga, przy braku szumów nie należy !
        # ! korzystać z opcji filtrowania       !
        reduced_noises = nr.reduce_noise(y = data, sr = rate)
        
        # Tworzenie nowej nazwy i zapis do innego pliku
        # przefiltrowanego sygnalu
        new_name = 'rn' + name
        wavfile.write(new_name, rate, reduced_noises)
        
        # Wyswietlenie nowego przefiltrowanego audio
        # Wykres amplitudowy
        T_PLOT.subplot(2)
        T_PLOT.config(xlim=[A_start, A_end], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio_rn = T_DSP.read_wave(new_name)
        audio_rn.scale(10)
        audio_rn.plot(color='blue')

        # Wykres czestotliwosciowy
        T_PLOT.subplot(4)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_rn_spectrum=audio_rn.make_spectrum()
        audio_rn_spectrum.plot(color='blue')

        T_PLOT.show()
   
    # TODO Wykonac analizowanie w zaleznosci od czestotliwosci
    # TODO Srednia z przedzialu 0 - 200 Hz, rysowanie i znalezienie
    # TODO pewnej zaleznosci, by to wykorzystac pozniej
    # TODO Wiecej w pliku .txt
    # TODO Sprawdzenie czy maksymalna wartosc przypada na mniej wiecej 100Hz
    #* Analizowanie audio
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


        ###* Rysowanie czarnych wykresow do analizy
        ## Pierwszy czarny wykres
        # Pomocnicze zmienne do analizy
        przec, x_pop, przec_sum, przec_kontr = 0, 0, 0, 0
        suma, aud_sum, i, k = 0, 0, 0, 0
        taba = []
        tabb = []

        #* =====================================================================================
        # *07 Wykres
        # Polega na wyliczeniu sredniej z wartosci bezwzglednej,
        # a nastepnie co (l_probek) brana jest srednia, dzieki
        # ktorej pozniej calosc jest nanoszona na wykres.
        T_PLOT.subplot(7)
        for x in audio.ys:
            suma += abs(x)
            aud_sum += abs(x)
            
            if(k % l_probek == 0):
                aud_apr = aud_sum/l_probek
                
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

        #* =====================================================================================
        # *08 Wykres
        T_PLOT.subplot(8)
        for x in audio2.ys:
            suma += abs(x)
            aud_sum += abs(x)
            
            if(k % l_probek == 0):
                aud_apr = aud_sum/l_probek

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

        #* =====================================================================================
        # *03 Wykres
        # Rysowanie spektrum wczytanego audio
        T_PLOT.subplot(3)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()
        audio_spectrum.plot(color='darkblue')

        # Maksymalna wartość Amplitudy w Hz
        # print(' Avarage: ' + str(abs(average(audio_spectrum.hs))))
        # print(' Max: ' + str(abs(max(audio_spectrum.hs))))

        # Policzenie sredniej czestotliwosci
        k = 0
        plot_sum = 0
        tabc = []

        for x in audio_spectrum.fs:
            if (x<=200):
                plot_sum = plot_sum + abs(audio_spectrum.hs[k])
                tabc.append(k)
                k += 1

        # Wyswietlenie sredniej czestotliwosci
        freq_avg = plot_sum/k
        
        # *05 Wykres
        # Rysowanie spektrum z filtrem dolnoprzepustowym
        T_PLOT.subplot(5)
        T_PLOT.config(xlim=[0, 200], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum.low_pass(cutoff=200, factor=0.01)
        audio_spectrum.plot(color='darkblue')
        
        # Rysowanie sredniej na wykresie - czerwony kolor
        for y in tabc:
            T_PLOT.Plot(y, freq_avg, color='red', marker='_')

        #* =====================================================================================
        # *04 Wykres
        # Rysowanie spektrum poprawnego bicia serca
        T_PLOT.subplot(4)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio2_spectrum=audio2.make_spectrum()
        audio2_spectrum.plot(color='darkred')

        # Maksymalna wartość Amplitudy w H
        # print(' --------------------------')
        # print(' Avarage: ' + str(abs(average(audio2_spectrum.hs))))
        # print(' Max: ' + str(abs(max(audio2_spectrum.hs))))

        # Policzenie sredniej czestotliwosci
        k = 0
        plot_sum1 = 0
        tabd = []

        for x in audio2_spectrum.fs:
            if (x<=200):
                plot_sum1 = plot_sum1 + abs(audio2_spectrum.hs[k])
                tabd.append(k)
                k += 1

        # Wyswietlenie sredniej czestotliwosci
        freq_avg1 = plot_sum1/k

        #// Jeśli amplituda jest wieksza niz 125% bazowego to mozliwe szumy
        #//if (abs(max(audio_spectrum.hs)) / abs(max(audio2_spectrum.hs))) > 1.25:
        #//    print("MOŻLIWE SZUMY!!")

        # *06 Wykres
        # Rysowanie spektrum z filtrem dolnoprzepustowym
        T_PLOT.subplot(6)
        T_PLOT.config(xlim=[0, 200], ylabel="Amplitude", xlabel="Frequency [Hz]") #ylim=[0,60000]
        audio2_spectrum.low_pass(cutoff=200, factor=0.01)
        audio2_spectrum.plot(color='darkred')
        
        # Rysowanie sredniej na wykresie - czerwony kolor
        for y in tabd:
            T_PLOT.Plot(y, freq_avg1, color='red', marker='_')

        #* Wyswietla wszystkie wykresy
        T_PLOT.show()


#// window = Tk()
# -------------------------------------- #
# ----- FUNKCJA MAIN - GŁÓWNA PĘTLA ---- #
# ----------- (MAIN FUNCTION) ---------- #
# -------------------------------------- #

# Glowna funkcja
def main():
    name = ""
    AudioProcessing.clear()
    AudioProcessing.introduction()

    # Glowna petla z programem
    while True:
        if name:
            print("\n[@] Aktualnie wczytany plik: " + name)
        else:
            print("\n[] Aktualnie wczytany plik: " + name)
        choose = input("\nCo chcialbys zrobic?\n 1) Wczytanie pliku\n 2) Szybki podglad\n 3) Analiza pliku\n 4) Filtracja\n 5) Wyjscie\n Twoj wybor: ")
        
        # Wybranie i wczytywanie sciezki audio do analizy
        if choose =='1':
            # Zapobieganie wpisaniu zlej nazwy oraz braku wybrania audio do analizy
            while True:
                try:
                    print("\nDostepne pliki:")
                    # Wyswietlenie wszystkich dostepnych audio w programie
                    _ = system('ls -m *.wav')
                    print("\nDostepne pliki po filtracji:")
                    _ = system('ls -m rn*.wav')
                    name = input("\nPodaj nazwę pliku: ")
                    
                    # Zapobieganie wpisaniu nazwy audio bez formatu
                    for x in name:
                        if name.endswith('.wav'):
                            name = name
                        else:
                            name = name + ".wav"

                    file = open(name, 'rb')
                    AudioProcessing.clear()
                    break
                except OSError:
                    print("Nie mozna wczytac pliku |", name ,"| sprobuj ponownie")

        # Szybki podglad pliku
        elif choose =='2':
            if name != "":
                AudioProcessing.preview(name)
            else:
                print("Nie wczytano pliku\n")

        # Uruchomienie funkcji z analiza audio
        elif choose =='3':
            if name != "":
                AudioProcessing.clear()
                AudioProcessing.processing(name)
            else:
                print("Nie wczytano pliku\n")

        # Filtracja szumów
        elif choose =='4':
            if name != "":
                AudioProcessing.filtration(name)
            else:
                print("Nie wczytano pliku\n")
            
        # Wyjscie z programu
        elif choose =='5':
            exit(0)
        
        else:
            AudioProcessing.clear()
            print(" Bledny wybor, wybierz ponownie! ")    

    #//window.title("Program do analizy")
    #//window.geometry("1000x800+50+50")
    #//window.resizable(False, False)
    #//window.mainloop()
    #//x.join()

# Wywolanie funkcji
if __name__ == '__main__':
    main()

# -------------------------------------- #
# --------------- KONIEC --------------- #
# --------------- (END) ---------------- #
# -------------------------------------- #
