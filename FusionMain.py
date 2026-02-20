import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk
import threading
import multiprocessing

# WICHTIG: Falls wir als App laufen, müssen wir die Pfade korrigieren
if getattr(sys, 'frozen', False):
    os.environ['PATH'] += os.pathsep + sys._MEIPASS

class FusionPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Pro - iOS Management")
        self.root.geometry("800x550")
        self.root.configure(bg="#ffffff")
        
        self.setup_ui()
        # Startet die Überwachung sanft
        self.root.after(1000, self.start_monitoring)

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="Fusion Pro Manager", font=("Helvetica", 18, "bold"), 
                 bg="#ffffff", fg="#1d1d1f").pack(pady=20)
        
        # Status Anzeige
        self.status_label = tk.Label(self.root, text="Suche Gerät...", font=("Helvetica", 12), 
                                     bg="#f5f5f7", width=50, height=2)
        self.status_label.pack(pady=10)

        # Log Bereich
        self.log_area = tk.Text(self.root, height=15, bg="#1e1e1e", fg="#34c759", 
                                font=("Menlo", 10), padx=10, pady=10)
        self.log_area.pack(padx=20, fill="both", expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Geräte Info", command=lambda: self.run_cmd("diagnostics device-info")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Batterie Status", command=lambda: self.run_cmd("diagnostics ioregistry --entry AppleSmartBattery")).pack(side="left", padx=5)

    def log(self, text):
        self.log_area.insert(tk.END, f"{text}\n")
        self.log_area.see(tk.END)

    def start_monitoring(self):
        def check():
            while True:
                try:
                    # Nutzt den internen Interpreter der App
                    cmd = [sys.executable, "-m", "pymobiledevice3", "usbmux", "list"]
                    res = subprocess.run(cmd, capture_output=True, text=True)
                    if "udid" in res.stdout.lower():
                        self.status_label.config(text="iPhone/iPad verbunden ✅", fg="#34c759")
                    else:
                        self.status_label.config(text="Warte auf USB Verbindung...", fg="#8e8e93")
                except:
                    pass
                import time
                time.sleep(5)
        threading.Thread(target=check, daemon=True).start()

    def run_cmd(self, command_str):
        self.log(f"Starte: {command_str}...")
        def task():
            try:
                # Zerlegt den String in eine Liste für subprocess
                cmd = [sys.executable, "-m", "pymobiledevice3"] + command_str.split()
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
                output = res.stdout if res.stdout else res.stderr
                self.root.after(0, self.log, output)
            except Exception as e:
                self.root.after(0, self.log, f"Fehler: {str(e)}")
        
        threading.Thread(target=task).start()

if __name__ == "__main__":
    # DAS HIER IST KRITISCH FÜR DIE APP-VERSION
    multiprocessing.freeze_support()
    
    # Verhindert rekursives Starten in manchen Umgebungen
    if len(sys.argv) > 1 and sys.argv[1] == "-m":
        # Erlaubt den internen Aufruf von Modulen ohne das GUI zu laden
        pass 
    else:
        root = tk.Tk()
        app = FusionPro(root)
        root.mainloop()
