import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import keyboard
import threading
import subprocess

from modules.config.config_handler import setting_load

# Dark mode settings
def set_dark_mode(root):
    root.tk_setPalette(background='#2e2e2e', foreground='white', activeBackground='#4d4d4d', activeForeground='white')
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure("TButton", background="#333", foreground="white", borderwidth=1)
    style.map("TButton", background=[("active", "#666")])
    style.configure("TLabel", background="#2e2e2e", foreground="white")
    style.configure("TEntry", fieldbackground="#666", foreground="white")
    style.configure("TText", background="#666", foreground="white")
    style.configure("TListbox", background="#2e2e2e", foreground="white", selectbackground="#4d4d4d", selectforeground="white")

def load_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
            sorted_data = {k: {sub_k: data[k][sub_k] for sub_k in sorted(data[k].keys(), key=lambda x: datetime.datetime.strptime(x, "%d.%m.%Y"))} 
                           for k in sorted(data.keys(), key=lambda x: datetime.datetime.strptime(x.split(' - ')[0], "%d.%m.%Y"))}
            return sorted_data
    return {}

def save_data(filepath, data):
    sorted_data = {k: {sub_k: data[k][sub_k] for sub_k in sorted(data[k].keys(), key=lambda x: datetime.datetime.strptime(x, "%d.%m.%Y"))} 
                   for k in sorted(data.keys(), key=lambda x: datetime.datetime.strptime(x.split(' - ')[0], "%d.%m.%Y"))}
    with open(filepath, 'w') as file:
        json.dump(sorted_data, file, indent=4)

def save_to_txt(data):
    with open("Tasks.txt", "w", encoding='utf-8') as txt_file:
        for week_key in sorted(data.keys(), key=lambda x: datetime.datetime.strptime(x.split(' - ')[0], "%d.%m.%Y")):
            week_data = data[week_key]
            for date_key in sorted(week_data.keys(), key=lambda x: datetime.datetime.strptime(x, "%d.%m.%Y")):
                entries = week_data[date_key]
                txt_file.write(f"- {date_key}:\n")
                for entry in entries:
                    txt_file.write(f"\t{entry}\n")
                txt_file.write("\n")

class ReportApp:
    def __init__(self, root, data_filepath):
        self.root = root
        self.data_filepath = data_filepath
        self.data = load_data(data_filepath)
        self.current_date = datetime.date.today()
        self.current_day = None
        self.init_gui()
        self.start_hotkey_listener()

    def init_gui(self):
        set_dark_mode(self.root)
        self.root.geometry("800x500")
        self.root.title("Weekly Reports")

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.week_label = ttk.Label(top_frame, text="")
        self.week_label.pack()

        self.prev_week_button = ttk.Button(top_frame, text="Previous week", command=self.show_previous_week)
        self.prev_week_button.pack(side=tk.LEFT, padx=5)

        self.next_week_button = ttk.Button(top_frame, text="Next week", command=self.show_next_week)
        self.next_week_button.pack(side=tk.LEFT, padx=5)

        self.current_week_button = ttk.Button(top_frame, text="Current week", command=self.show_current_week)
        self.current_week_button.pack(side=tk.LEFT, padx=5)

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.days_listbox = tk.Listbox(main_frame, height=10, bg='#2e2e2e', fg='white', selectbackground='#4d4d4d', selectforeground='white')
        self.days_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        self.days_listbox.bind("<<ListboxSelect>>", self.on_day_select)

        self.entry_text = tk.Text(main_frame, height=10, width=50, bg='#666', fg='white', insertbackground='white')
        self.entry_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        self.submit_button = ttk.Button(bottom_frame, text="Save entry", command=self.submit_entry)
        self.submit_button.pack()
        
        self.weekly_button = ttk.Button(bottom_frame, text="Create Weekly Report", command=self.build_weekly_report)
        self.weekly_button.pack(pady=5)
        
        self.display_week_list()

    def build_weekly_report(self):
        os.system("python setup.py --build")
        os.system('"' + os.path.abspath(os.getcwd()) + "/" + setting_load("path_export", "export") + r"\output\report.pdf" + '"')

    def submit_entry(self):
        entry = self.entry_text.get("1.0", tk.END).strip()
        today = self.current_day if self.current_day else datetime.date.today()
        start, end = self.get_week_range(today)
        week_key = f"{self.get_date_string(start)} - {self.get_date_string(end)}"
        date_key = self.get_date_string(today)

        self.ensure_week_structure(today)

        if entry:
            processed_entries = self.process_entry(entry)
            self.data[week_key][date_key] = processed_entries
        else:
            if week_key in self.data and date_key in self.data[week_key]:
                del self.data[week_key][date_key]
                if not self.data[week_key]:
                    del self.data[week_key]

        save_data(self.data_filepath, self.data)
        save_to_txt(self.data)
        messagebox.showinfo("Success", "The entry was saved successfully!")
        self.display_week_list()

    def show_previous_week(self):
        self.current_date -= datetime.timedelta(days=7)
        self.display_week_list()

    def show_next_week(self):
        self.current_date += datetime.timedelta(days=7)
        self.display_week_list()

    def show_current_week(self):
        self.current_date = datetime.date.today()
        self.display_week_list()

    def display_week_list(self):
        self.days_listbox.delete(0, tk.END)

        start, end = self.get_week_range(self.current_date)
        week_key = f"{self.get_date_string(start)} - {self.get_date_string(end)}"
        self.week_label.config(text=week_key)

        if (week_key := f"{self.get_date_string(start)} - {self.get_date_string(end)}") in self.data:
            week_data = self.data[week_key]
        else:
            week_data = {}

        current_week_dates = [start + datetime.timedelta(days=i) for i in range(5)]
        current_week_dates_strings = [self.get_date_string(date) for date in current_week_dates]

        current_week_dates_strings = list(dict.fromkeys(current_week_dates_strings))

        for date in current_week_dates_strings:
            self.days_listbox.insert(tk.END, date)

    def on_day_select(self, event):
        selection = self.days_listbox.curselection()
        if selection:
            date_key = self.days_listbox.get(selection[0])
            week_key = self.week_label.cget("text")

            self.entry_text.delete("1.0", tk.END)
            if week_key in self.data and date_key in self.data[week_key]:
                entries = self.data[week_key][date_key]
                for entry in entries:
                    self.entry_text.insert(tk.END, f"{entry}\n")
            self.current_day = datetime.datetime.strptime(date_key, "%d.%m.%Y").date()

    def get_week_range(self, date):
        start = date - datetime.timedelta(days=date.weekday())
        end = start + datetime.timedelta(days=4)
        return start, end

    def get_date_string(self, date):
        return date.strftime("%d.%m.%Y")

    def process_entry(self, entry):
        processed_entries = []
        for line in entry.split('\n'):
            if line.strip().startswith("§i"):
                processed_entries.append(line.strip().replace("§i", "Illness: "))
            elif line.strip().startswith("§v"):
                processed_entries.append(line.strip().replace("§v", "Vacation: "))
            else:
                processed_entries.append(line.strip())
        return processed_entries

    def ensure_week_structure(self, date):
        start, end = self.get_week_range(date)
        week_key = f"{self.get_date_string(start)} - {self.get_date_string(end)}"
        if week_key not in self.data:
            self.data[week_key] = {}

    def start_hotkey_listener(self):
        def on_ctrl_s():
            self.submit_entry()

        keyboard.add_hotkey("ctrl+s", on_ctrl_s)
        threading.Thread(target=keyboard.wait, args=("ctrl+s",), daemon=True).start()

def run_gui():
    root = tk.Tk()
    app = ReportApp(root, 'reports.json')
    root.mainloop()

if __name__ == "__main__":
    run_gui()
