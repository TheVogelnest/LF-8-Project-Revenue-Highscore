import VMMain as vm
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import VHellGui
import threading

#simon binär = 0101001101101001011011010110111101101110

main = tk.Tk()
login_window = tk.Toplevel(main)
console_thread = threading.Thread(target=vm.write_to_console, daemon=True)

#tkinter hat einen Bug das die Hintergrundfarbe einer Treeview vom Style im Nachhinein immer überschrieben wird
#deswegen Funktioniert ohne diese Bug Fix Methode das Farbliche Makieren des höhsten eintrages nicht
#Quelle = https://core.tcl-lang.org/tk/tktview?name=509cafafae
style = ttk.Style()
def fixed_map(option):
        # Returns the style map for 'option' with any styles starting with
        # ("!disabled", "!selected", ...) filtered out
        # style.map() returns an empty list for missing options, so this should
        # be future-safe
        return [elm for elm in style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

def show_revenues():
    columns = ("Filiale", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag")
    revenue_overview = ttk.Treeview(main, columns=columns, show='headings')

    #Tag definieren für die Filliale mit dem Höhsten Umsatz
    revenue_overview.tag_configure("highlight", background="lightgreen")

    #Aufrufen der Bug Fix Methode
    style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))
    for c in columns:
        revenue_overview.heading(c, text=c)
        revenue_overview.column(c, width=100, anchor=tk.CENTER)

    for store in vm.stores:
        item_id = revenue_overview.insert("", tk.END, values=(store.name, *store.revenues))
        if store == vm.highest_store:
            revenue_overview.item(item_id, tags="highlight")

    revenue_overview.pack(fill=tk.BOTH, expand=False)

def create_main_window_widgets():
    button = tk.Button(main, text="Beenden", command=close)
    button.place(x=720,y=250)

def close():
    main.destroy()
    #vermeidet fehler und das Konsolen Programm kann trotz schließen des Hauptprogrammes ausgeführt werden
    console_thread.join()

def config_main_window():
    main.withdraw() #blendet das main window aus
    main.geometry('800x300')

    create_main_window_widgets()
    show_revenues()

def open_login_window():
    def check_name_input():
        name = name_entry.get().strip()
        if vm.is_binary_string(name):
            if len(name) <= 24:
                messagebox.showerror('Error', 'Das ist zu kurz für einen Namen')
            elif vm.tempName != None and vm.convert_binary_to_letter(name) != vm.tempName:
                messagebox.showerror('Error', 'Das ist nicht der Name den du zuerst eingegeben hast du Schlingel')
            else:
                messagebox.showinfo("Willkommen", f"Hallo, {vm.convert_binary_to_letter(name)}")
                login_window.destroy()
                main.deiconify()
        else:
            vm.tempName = name
            messagebox.showerror('Error', 'Nur die binäre schreibweise ist erlaubt')

    #Login Window designen
    login_window.lower()
    login_window.title("Login")
    login_window.geometry("300x150")
    tk.Label(login_window, text="Geben Sie Ihren Namen ein:").pack(pady=10)
    name_entry = tk.Entry(login_window, width=25)
    name_entry.pack(pady=5)
    login_button = tk.Button(login_window, text="Anmelden", command=check_name_input)
    login_button.pack(pady=10)

def start_gui():
    config_main_window()
    open_login_window()
    VHellGui.create_heart()
    VHellGui.play_song()

    #Startet das Konsolen Programm auf einem anderen Thread damit es sich nicht gegenseitig behindert
    #console_thread = threading.Thread(target=vm.write_to_console, daemon=True)
    console_thread.start()

    main.mainloop()

start_gui()
