import sys

import MStore as st
import re
from tkinter import messagebox

datas = st.StoreDatas()
datas.dictionary_path = 'Umsätze/*.csv'
datas.store_path = st.get_store_path(datas.dictionary_path)

plane_stores = []
plane_stores = st.get_store_datas(datas.store_path)

#für GUI out of Hell
tempName = None

#Hell Gui überprüfungen
def is_binary_string(s):
    return bool(re.fullmatch("[01]*", s)) #überprüft ob nur 0 und 1 im string enthalten sind
def convert_binary_to_letter(string_binary):
    n = 8 #8er binäre Blöcke für ASCII
    array_byte = []
    ascii_name = ''
    for i in range(0, len(string_binary), n):
        array_byte.append(string_binary[i:i+n])
    for byte in array_byte:
        ascii_name += chr(int(byte, 2)) # 2 repräsentiert hier Binär // Hier wird der 8er Block Binärer Zahlen
        # in einen char nach ASCII konvertiert
    return ascii_name

#Daten aufarbeitung
def init_stores(plane_data, pathes):
    temp_list = []
    for i in range(len(plane_data)):
        cur_store = st.Store()
        cur_store.days = plane_data[i][0]
        cur_plane_revenues = plane_data[i][1]
        cur_store.revenues = st.config_list_revenue(cur_plane_revenues)
        cur_store.name = pathes[i][8:-4]
        temp_list.append(cur_store)
    return temp_list

if len(datas.store_path) > 0:
    stores = init_stores(plane_stores, datas.store_path)
else:
    messagebox.showerror('Error', 'Keine Dateien im Umsatzordner gefunden') #überprüfen ob der Ordner leer ist
    sys.exit()

def get_highest_revenue():
    highest_revenue = 0
    for store in stores:
        total_revenue = sum(store.revenues)
        if total_revenue > highest_revenue:
            highest_revenue = total_revenue
            highest_store = store
    return highest_store

highest_store = get_highest_revenue()

#Daten verarbeitung
def write_to_console():
    highest_revenue_day = {}

    for i, day in enumerate(stores[0].days): #enumerate gibt den wert (day) und den index des elementes zurück (i)
        max_sale = 0
        best_store = None

        for store in stores:
            if store.revenues[i] > max_sale:
                max_sale = store.revenues[i]
                best_store = store.name

        highest_revenue_day[day] = {'name': best_store, 'revenues': max_sale}

    print('Wähle eine der optionen \n Option A: Umsatz stärkste filliale für jeden Wochentag \n Option B: Highscore an wie vielen Tagen jede Filliale die Umsatz stärkste wahr')
    option = input("Option (a/b): ")

    def print_option_a():
        for day, info in highest_revenue_day.items():
            print(f"Am {day} hatte {info['name']} den höchsten Umsatz mit {info['revenues']} Euro.")
    def print_option_b():
        for day, info in highest_revenue_day.items():
            tem_stores = []
            for i, store in enumerate(stores):
                if info['name'] == store.name:
                    stores[i].highscore += 1
                tem_stores.append(store)
        for store in stores:
            print(f"{store.name}: {store.highscore} Tage der Umsatz stärkste")

    if option.lower() == 'a':
        print_option_a()
    elif option.lower() == 'b':
        print_option_b()
    else:
        print("Unzulässige Eingabe!")


