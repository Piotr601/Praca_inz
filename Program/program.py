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
# * HIGHLIGHTED                          #
# ! Alert ...                            #
# ? Should ....                          #
# TODO sth                               #
# // that                                #
# -------------------------------------- # 

# Nagrywanie
import pyaudio
import wave

# Filtrowanie
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import butter, lfilter

# Analizowanie
import thinkdsp as T_DSP
import thinkplot as T_PLOT

# Podstawowe
from array import *
from os import system

# -------------------------------------- #
# -------------- PARAMETRY ------------- #
# ------------ (PARAMETERS) ------------ #
# -------------------------------------- #

# Przedzial czasowy wyswietlany na wykresach
# Start audio na wykresie 
A_start = 0
# Koniec audio na wykresie
A_end = 6

# Liczba probek brana pod uwage w liczeniusrednich wykresow
# - szare wykresy w analizie - 
l_probek = 500
# Przelicznik sluzacy jako mnoznik wybierany przy wczytywaniu pliku.
przelicznik = 0

# -------------------------------------- #
# -------------- FUNKCJE --------------- #
# ------- (DECLARING FUNCTIONS) -------- #
# -------------------------------------- #

#--------------------------------------------------------------------#
#                                                                    #
# Klasa AudioProcessing sluzaca do obslugi przetwarzania audio       #
#                                                                    #
# Metody:                                                            #
#  - clear                                                           #
#       odpowiada za czyszczenie ekranu terminala po wywolaniu       #
#  - record                                                          #
#       sluzy do nagrywania pliku, a nastepnie jest on zapisywany    #
#       do folderu z plikiem z nazwa wpisana przez uzytkownika       #
#  - introduction                                                    #
#       wyswietla podstawowe informacje takie jak autora, temat      #
#       pracy oraz kierunek i uczelnie autora                        #
#  - preview                                                         #
#       funkcja sluzaca do podgladu zalodowanego pliku, zostala      #
#       stworzona po to by szybko podejrzec co jest w pliku, to      #
#       znaczy jak wygladaja wykresy: amplitudowo-czasowy oraz       #
#       amplitudowo-czestotliwosciowy                                #
#  - filtration                                                      #
#       funkcja sluzaca do filtrowania nagranych audio poprzez       #
#       metode record, zastosowane sa 3 filtry, kolejno:             #
#       band, low, band aby zniwelowac szumy i uwydatnic             #
#       dzwiek bicia serca                                           #
#  - processing                                                      #
#       glowna funkcja sluzaca analizie danych, to w niej odbywa     #
#       sie badanie i wyswietlanie pozniejszego wyniku, jest to      #
#       jedna z najdluzszych i najwazniejszych funkcji programu      #
#                                                                    #
# Argumenty:                                                         #
#   - name                                                           #
#       przekazuje do metod nazwe pliku (zalodowanego)               #
#   - przelicznik                                                    #
#       przekazuje informacje o zalodowanym pliku, czy               #
#       zostal on nagrany, czy nie. Dzieki temu mozna dobrac         #
#       odpowiednie parametry do analizy, nie jest jednak to         #
#       konieczne. Calosc powinna dzialac dla parametru 'n' - 0.7    #
#                                                                    #
#--------------------------------------------------------------------#

class AudioProcessing:
    #* Funkcja uzywana w celu czyszczenia ekranu
    def clear():
        _ = system('clear')

    #* Funkcja uzywana do nagrywania pliku
    def record():
        # Zmienne do nagrywania
        chunk = 1024                     # ilosc chunkow
        sample_format = pyaudio.paInt16  # ilosc bitow w probce
        channels = 2                     # 2 kanal
        fs = 44100                       # nagrywanie w liczbie probek na sekunde
        seconds = 7                      # czas nagrywania

        # Nazwa pliku nagrywanego
        recording = input('\nPodaj nazwe pliku: ') + '.wav'

        # Tworzenie interfejsu PyAudio
        PyAud = pyaudio.PyAudio()

        # Czyszczenie ekranu
        AudioProcessing.clear()

        print('Nagrywanie ...')

        # Zdefiniowanie strumienia
        stream = PyAud.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

        # Inicjalizacja tabeli do przechowywania ramek
        frames = []

        # Przechowywanie danych w chunkach
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Zatrzymanie i zamkniecie strumienia 
        stream.stop_stream()
        stream.close()
        
        # Zakonczenie interfejsu PyAud
        PyAud.terminate()

        print(' Pomyslnie zakonczono nagrywanie pliku: ' + recording)

        # Zapis zapisanego pliku do formatu WAV
        wav_file = wave.open(recording, 'wb')
        
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(PyAud.get_sample_size(sample_format))
        wav_file.setframerate(fs)
        wav_file.writeframes(b''.join(frames))
        wav_file.close()

        song = AudioSegment.from_wav(recording)
        last_6_sec = song[-6000:]
        last_6_sec.export(recording, format="wav")
        
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

    #* Usuwanie szumow, wstepna filtracja
    # Napisano filtracje bazujaca na 3 filtrach
    # Band -> Lower -> Band
    # Dzieki temu usuwamy niechciane szumy
    def filtration(name):
        # Zdefiniowanie okna do wyswietlania
        T_PLOT.preplot(rows=2, cols=2)

        # Podglad sciezki audio
        T_PLOT.config(xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio =  T_DSP.read_wave(name)
        audio.scale(10)
        audio.plot(color='blue')

        # Wykres czestotliwosci audio
        T_PLOT.subplot(2)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()
        audio_spectrum.plot(color='darkblue')

        #====================================#
        #              FILTR BAND            #
        #====================================#

        # Zmienne stale
        PLIK_WAVE = name
        NOWY_PLIK_WAVE = 'f_' + name
        FRAME_RATE = 44100
        ORDER = 2

        # Zmienne pomocnicze
        lowcut = 29.0
        highcut = 40.0
        
        # Zdefiniowanie filtra
        def butter_bandpass(lowcut, highcut, fs, order=ORDER):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            b, a = butter(order, [low, high], btype='band')
            return b, a

        def butter_bandpass_filter(data, lowcut, highcut, fs, order=ORDER):
            b, a = butter_bandpass(lowcut, highcut, fs, order=order)
            y = lfilter(b, a, data)
            return y

        def bandpass_filter0(buffer):
            return butter_bandpass_filter(buffer, lowcut, highcut, FRAME_RATE, order=ORDER)

        # Wczytanie pliku
        samplerate, data = wavfile.read(PLIK_WAVE)
        samplerate = FRAME_RATE

        # Filtrowanie oraz zapis do pliku
        filtered = np.apply_along_axis(bandpass_filter0, 0, data).astype('int16')
        wavfile.write(NOWY_PLIK_WAVE, samplerate, filtered)

        #====================================#
        #              FILTR LOW             #
        #====================================#

        # Zmienna pomocnicza
        cutoff = 10.0

        # Zdefiniowanie filtra 
        def butter_lowpass(cutoff, fs, order = ORDER):
            nyqs = 0.5 * fs
            normal_cutoff = cutoff/nyqs
            b,a = butter(order, normal_cutoff, btype='low', analog= False)
            return b,a

        def butter_lowpass_filter(data, cutoff, fs, order=ORDER):
            b, a = butter_lowpass(cutoff, fs, order=order)
            y = lfilter(b, a, data)
            return y

        def lowpass_filter(buffer):
            return butter_lowpass_filter(buffer, cutoff, FRAME_RATE, order=ORDER)
            
        # Wczytanie pliku
        samplerate, data = wavfile.read(NOWY_PLIK_WAVE)
        samplerate = FRAME_RATE

        # Filtracja, zapis do pliku
        filtered = np.apply_along_axis(lowpass_filter, 0, data).astype('int16')
        wavfile.write(NOWY_PLIK_WAVE, samplerate, filtered)

        #====================================#
        #              FILTR BAND            #
        #====================================#

        # Zmienne pomocnicze
        lowcut = 22.0
        highcut = 40.0

        # Wczytanie pliku
        samplerate, data = wavfile.read(NOWY_PLIK_WAVE)
        samplerate = FRAME_RATE

        # Filtracja, zapis do pliku
        filtered = np.apply_along_axis(bandpass_filter0, 0, data).astype('int16')
        wavfile.write(NOWY_PLIK_WAVE, samplerate, filtered)

        # Odczytanie pliku
        file = open(NOWY_PLIK_WAVE, 'rb')
                 
        # Podglad sciezki audio, wykres amplitudowy
        T_PLOT.subplot(3)
        T_PLOT.config(xlim=[0, 6], xlabel="Time [s]", ylabel="Amplitude", legend=False)
        audio =  T_DSP.read_wave(file)
        audio.scale(10)
        audio.plot(color='blue')

        # Podglad sciezki audio, wykres czestotliwosciowy
        T_PLOT.subplot(4)
        T_PLOT.config(xlim=[0, 100], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()
        audio_spectrum.plot(color='darkblue')

        T_PLOT.show()

        print(' Pomyslnie przefiltrowano plik: ' + name)
        print(' Nowy plik ma nazwe: ' + NOWY_PLIK_WAVE)
        print('- - - - - - - - - - - - - - - - - - - - - - -')
        
    #* Analizowanie audio
    def processing(name, przelicznik):

        # Punkty do zliczania szansy na szumy
        POINTS = 0
        POINTS_ALL = 0

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
        PROG = 1.65
        PROG_DET = PROG*0.3

        przec, x_pop, przec_sum, przec_kontr = 0, 0, 0, 0
        suma, aud_sum, i, k = 0, 0, 0, 0
        x_pop_pop = 0
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
        # Srednia powiekszona o prog
        aprox = PROG * aprox

        # Rysowanie sygnalu
        T_PLOT.Plot(tabb, taba, color='black') 

        # Wypisanie sredniej i wielkosci audio (ilosc probek - calosc)
        print("\nAprox: " + str(aprox))
        print(" Size: " + str(audio.ys.size) + '\n')

        # Rysowanie sredniej na wykresie - zielony kolor
        for y in tabb:
            T_PLOT.Plot(y, aprox, color='green', marker='_')
            T_PLOT.Plot(y, PROG_DET*aprox*przelicznik, color='darkred', marker='_')

        # Przechodzenie przez wszystkie wartosci
        # Pozniej nastepuje zliczanie punktow ktore przechodza przez srednia - aprox
        # Zwracana jest ilosc przechodzenia w jednym cyklu
        # =  2  poprawna wartosc
        # >= 2  niepoprawne wartosci - wystepuje szum zaklocajacy
        for x in taba:
            # Gdy wykres przecina sie rosnac
            if ((x_pop <= aprox and x_pop_pop <= aprox) and (x > aprox)):
                przec += 1
                przec_sum+=1
            # Gdy wykres przecina sie malejac
            elif((x_pop >= aprox and x_pop_pop >= aprox) and (x < aprox)):
                przec += 1
                przec_sum+=1
            x_pop = x
            x_pop_pop = x_pop

            # Gdy spelnione sa dwa warunki, to jest ilosc przeciec jest wieksza, badz
            # rowna 2 i jest mniejsza od parametru (aby oddzielic kolejne cykle)
            if (przec >= 2 and x <= PROG_DET*aprox*przelicznik):
                print(' 01 Przeciecia w jednym uderzeniu: ' + str(przec))
                # Zmienna pomocnicza - kontrolna
                przec_kontr += przec 

                # Gdy wystepuje wiecej niz 2 przeciecia (inaczej niz norma)
                if (przec > 2):
                    print(" > Uwaga tutaj wystepuja nieprawidlowosci.")
                    POINTS += 2
                    if (przec > 6):
                        print(" > Uwaga wystepuja szumy! ")
                        POINTS += 9
                    if (przec > 4):
                        print(" > Uwaga prawdopodobnie wystepuja szumy")
                        POINTS += 3
                POINTS_ALL += 14
                przec = 0
        
        # Wypisywanie ilosc przeciec i liczby kontrolnej
        # Gdy obydwie liczby sie zgadzaja, program zlicza wszystkie uderzenia
        # i dziala prawidlowo        
        print(PROG_DET*aprox*przelicznik)
        print('Przeciecia 1: ' + str(przec_sum) + '\n  Kontrolnie: ' + str(przec_kontr) + '\n')      

        #* =====================================================================================
        # *08 Wykres
        ## Drugi czarny wykres
        # Pomocnicze zmienne do analizy
        # Wyzerowanie wartosci
        przec, x_pop, przec_sum, przec_kontr = 0, 0, 0, 0
        x_pop_pop = 0
        suma, aud_sum, i, k = 0, 0, 0, 0
        taba = []
        tabb = []

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
        aprox = PROG * aprox
        T_PLOT.Plot(tabb, taba, color='black')  

        # Rysowanie sredniej na wykresie - zielony kolor
        for y in tabb:
            T_PLOT.Plot(y, aprox, color='green', marker='_') 
            T_PLOT.Plot(y, PROG_DET*aprox, color='darkred', marker='_')

        # Przechodzenie przez wszystkie wartosci
        for x in taba:
            if ((x_pop <= aprox and x_pop_pop <= aprox) and (x > aprox)):
                przec += 1
                przec_sum +=1
            elif((x_pop >= aprox and x_pop_pop >= aprox) and (x < aprox)):
                przec += 1
                przec_sum += 1
            x_pop = x
            x_pop_pop = x_pop

            if (przec >= 2 and x <= PROG_DET*aprox):
                print(' 02 Przeciecia w jednym uderzeniu: ' + str(przec))
                przec_kontr += przec 

                if (przec > 2):
                    print(" > Uwaga tutaj wystepuja nieprawidlowosci.")
                    if (przec > 6):
                        print(" > Uwaga wystepuja szumy! ")
                    elif (przec > 4):
                        print(" > Uwaga prawdopodobnie wystepuja szumy")
                
                przec = 0
            
        print(aprox)
        print('Przeciecia 2: ' + str(przec_sum) + '\n  Kontrolnie: ' + str(przec_kontr) + '\n')    

        #* =====================================================================================
        # *03 Wykres
        # Rysowanie spektrum wczytanego audio

        NORMA_MAX = 100000
        NORMA_AVG = 4000

        T_PLOT.subplot(3)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum=audio.make_spectrum()
        audio_spectrum.plot(color='darkblue')

        # Policzenie sredniej czestotliwosci
        k,i = 0, 0
        plot_sum = 0
        tabc = []

        for x in audio_spectrum.fs:
            if (x<=200):
                if abs(audio_spectrum.hs[k]) >= 500:
                    plot_sum = plot_sum + abs(audio_spectrum.hs[k])
                    i += 1
                tabc.append(k)
                k += 1

        # Wyswietlenie sredniej czestotliwosci
        freq_avg = plot_sum/k
        freq_max = abs(max(audio_spectrum.hs))
        print('\n 01 Srednia czestotliwosc: ' + str(freq_avg))
        print(' 01 Maksymalna czestotliwosc: ' + str(freq_max))

        # Norma czestotliwosc SREDNIA
        if(freq_avg > NORMA_AVG):
            print(" [-] Czestotliwosc srednia POZA NORMA ")
            POINTS += 10
            if(freq_avg > NORMA_AVG + 500):
                POINTS += 20
            if(freq_avg > NORMA_AVG + 1000):
                POINTS += 40
        elif(freq_avg <= NORMA_AVG):
            print(" [+] Czestotliwosc srednia w normie ")

        # Norma czestotliwosc MAX
        if(freq_max > NORMA_MAX):
            print(" [-] Czestotliwosc maksymalna POZA NORMA ")
            POINTS += 10
            if(freq_max > NORMA_MAX + 1000):
                POINTS += 20
            if(freq_max > NORMA_MAX + 2000):
                POINTS += 40
        elif(freq_max <= NORMA_MAX):
            print(" [+] Czestotliwosc maksymalna w normie ")

        POINTS_ALL += 140

        # *05 Wykres
        # Rysowanie spektrum z filtrem dolnoprzepustowym
        T_PLOT.subplot(5)
        T_PLOT.config(xlim=[0, 200], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio_spectrum.low_pass(cutoff=200, factor=0.01)
        audio_spectrum.plot(color='darkblue')
        
        # Rysowanie sredniej na wykresie - czerwony kolor
        for y in tabc:
            T_PLOT.Plot(y, freq_avg, color='red', marker='_')
            T_PLOT.Plot(y, freq_max, color='darkgreen', marker ='_')

        #* =====================================================================================
        # *04 Wykres
        # Rysowanie spektrum poprawnego bicia serca
        T_PLOT.subplot(4)
        T_PLOT.config(xlim=[0, 1000], ylabel="Amplitude", xlabel="Frequency [Hz]")
        audio2_spectrum=audio2.make_spectrum()
        audio2_spectrum.plot(color='darkred')

        # Policzenie sredniej czestotliwosci
        k, i = 0, 0
        plot_sum1 = 0
        tabd = []

        for x in audio2_spectrum.fs:
            if (x<=200):
                if abs(audio2_spectrum.hs[k]) >= 500:
                    plot_sum1 = plot_sum1 + abs(audio2_spectrum.hs[k])
                    i += 1
                tabd.append(k)
                k += 1

        # Wyswietlenie sredniej czestotliwosci
        freq_avg1 = plot_sum1/k
        freq_max1 = abs(max(audio2_spectrum.hs))
        print('\n 02 Srednia czestotliwosc: ' + str(freq_avg1))
        print(' 02 Maksymalna czestotliwosc: ' + str(freq_max1))

        # Norma czestotliwosc SREDNIA
        if(freq_avg1 > NORMA_AVG):
            print(" [-] Czestotliwosc srednia POZA NORMA ")
        elif(freq_avg1 <= NORMA_AVG):
            print(" [+] Czestotliwosc srednia w normie ")

        # Norma czestotliwosc MAX
        if(freq_max1 > NORMA_MAX):
            print(" [-] Czestotliwosc maksymalna POZA NORMA ")
        elif(freq_max1 <= NORMA_MAX):
            print(" [+] Czestotliwosc maksymalna w normie ")

        # *06 Wykres
        # Rysowanie spektrum z filtrem dolnoprzepustowym
        T_PLOT.subplot(6)
        T_PLOT.config(xlim=[0, 200], ylabel="Amplitude", xlabel="Frequency [Hz]") #ylim=[0,60000]
        audio2_spectrum.low_pass(cutoff=200, factor=0.01)
        audio2_spectrum.plot(color='darkred')
        
        # Rysowanie sredniej na wykresie - czerwony kolor
        for y in tabd:
            T_PLOT.Plot(y, freq_avg1, color='red', marker='_')
            T_PLOT.Plot(y, freq_max1, color='darkgreen', marker ='_')

        # Oblicza punkty i ich stosunek wzgledem siebie
        result = round(POINTS/POINTS_ALL*100, 4)
        print("\n Uzyskany wynik: " + str(POINTS) + "/" + str(POINTS_ALL) + " pkt")
        print(" Stosunek punktowy: " + str(result))

        # Prawdopodobienstwo wystepowania szumow biorac pod uwage
        # ich stosunek pomnozony o 100
        if(result <= 100.0):
            # 100 - zaszumiony sygnal
            if(result == 100.0):
                print("\n Zaszumiony sygnal. Ta probka nie nadaje sie do analizy.")
            # 100 <-> 30 
            if(result >= 30.0 and result < 100.0):
                print("\n Wystepuja szumy ")
            # 30 <-> 20
            if(result >= 20.0 and result < 30.0):
                print("\n Wystepuje duze prawdopodobienstwo szumow ")
            # 20 <-> 15
            if(result >= 15.0 and result < 20.0):
                print("\n Wystepuje średnie prawdopodobienstwo szumow ")
            # 15 <-> 12
            if(result >= 12.0 and result < 15.0):
                print("\n Wystepuje male prawdopodobienstwo szumow. Mozliwe drobne zaklocenia.")
            # 12 <-> 5
            if(result >= 5.0 and result < 12.0):
                print("\n Wystepuje znikome prawdopodobienstwo szumow. Mozliwe drobne zaklocenia.")
            # 5 <-> 0
            if(result > 0.0 and result < 5.0):
                print("\n Nie wystepuja szumy")
            # 0 - brak szumow
            if(result == 0.0):
                print("\n Brak szumow, idealny sygnal.")

        #* Wyswietla wszystkie wykresy
        T_PLOT.show()

# -------------------------------------- #
# ----- FUNKCJA MAIN - GŁÓWNA PĘTLA ---- #
# ----------- (MAIN FUNCTION) ---------- #
# -------------------------------------- #

# FUnkcja do wyswietlania menu
def menu():
    print("\n#==================================#")
    print("|           M  E  N  U             |")
    print("#==================================#")
    print("| 1) Wczytanie pliku               |")
    print("| 2) Szybki podglad                |")
    print("| 3) Analiza pliku                 |")
    print("| 4) Filtracja                     |")
    print("| 5) Nagrywanie dzwieku            |")
    print("| 6) Wyjscie                       |")
    print("#==================================#")

# Glowna funkcja
def main():
    name = ""
    AudioProcessing.clear()
    AudioProcessing.introduction()

    # Glowna petla z programem
    while True:
        if name:
            print("\n[@] Aktualnie wczytany plik: " + name)
            if przelicznik == 1.7:
                print("[@] Plik nagrany w programie")
            if przelicznik == 0.7:
                print("[ ] Plik nie zostal nagrany w programie")
        else:
            print("\n[ ] Aktualnie wczytany plik: " + name)
        
        menu()
        choose = input("\n > Twoj wybor: ")
        
        # Wybranie i wczytywanie sciezki audio do analizy
        if choose =='1':
            # Zapobieganie wpisaniu zlej nazwy oraz braku wybrania audio do analizy
            while True:
                try:
                    print("\n o Dostepne pliki:")
                    # Wyswietlenie wszystkich dostepnych audio w programie
                    _ = system('ls -m *.wav')
                    print("\n o Dostepne pliki po filtracji:")
                    _ = system('ls -m f_*.wav')
                    name = input("\n > Podaj nazwę pliku: ")
                    
                    # Zapobieganie wpisaniu nazwy audio bez formatu
                    for x in name:
                        if name.endswith('.wav'):
                            name = name
                        else:
                            name = name + ".wav"

                    file = open(name, 'rb')

                    correct = 0

                    while correct == 0:
                        f_rec = input('\n >> Czy plik zostal nagrany? (Y/n): ')
                        if f_rec == 'Y' or f_rec == 'y':
                            przelicznik = 1.7
                            correct = 1
                        elif f_rec == 'n' or f_rec == 'N':
                            przelicznik = 0.7
                            correct = 1
                        else:
                            print(" Podaj poprawna opcje !")
                            correct = 0
                        
                    correct = 0

                    AudioProcessing.clear()
                    break
                except OSError:
                    print("Nie mozna wczytac pliku |", name ,"| sprobuj ponownie")

        # Szybki podglad pliku
        elif choose =='2':
            if name != "":
                AudioProcessing.preview(name)
                AudioProcessing.clear()
            else:
                print("Nie wczytano pliku\n")

        # Uruchomienie funkcji z analiza audio
        elif choose =='3':
            if name != "":
                AudioProcessing.clear()
                AudioProcessing.processing(name, przelicznik)
            else:
                print("Nie wczytano pliku\n")

        # Filtracja szumów
        elif choose =='4':
            if name != "":
                AudioProcessing.clear()
                AudioProcessing.filtration(name)
            else:
                print("Nie wczytano pliku\n")
            
        # Wyjscie z programu
        elif choose =='5':
            AudioProcessing.record()
            AudioProcessing.clear()

        elif choose =='6':
            exit(0)

        else:
            AudioProcessing.clear()
            print(" Bledny wybor, wybierz ponownie! ")    

# Wywolanie funkcji
if __name__ == '__main__':
    main()

# -------------------------------------- #
# --------------- KONIEC --------------- #
# --------------- (END) ---------------- #
# -------------------------------------- #
