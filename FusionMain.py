import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import threading
import multiprocessing # WICHTIG für gefrorene Apps

class FusionPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Pro - Safe Boot")
        self.root.geometry("900x600")
        
        # Sicherheits-Check: Woher kommt das Kommando?
        self.python_exe = self.get_safe_runtime()
        
        self.setup_ui()
        # Den Check-Loop starten wir erst nach 2 Sekunden, um dem System Luft zu lassen
        self.root.after(2000, self.start_monitor)

    def get_safe_runtime(self):
        # Wenn wir als App laufen, müssen wir das interne Python finden, 
        # nicht die App-Binary selbst aufrufen!
        if getattr(sys, 'frozen', False):
            # Pfad zum Python-Interpreter innerhalb des PyInstaller-Bundles
            return sys._MEIPASS if hasattr(sys, '_MEIPASS') else sys.executable
        return sys.executable

    def setup_ui(self):
        self.root.configure(bg="#ffffff")
        tk.Label(self.root, text="Fusion Pro v3 (Stable)", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=20)
        
        self.log_area = tk.Text(self.root, height=20, bg="#f4f4f4", padx=10, pady=10)
        self.log_area.pack(padx=20, fill="both", expand=True)
        
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Geräte Info", command=self.run_info).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Notstopp", command=self.emergency_exit, fg="red").pack(side="left", padx=10)

    def log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def start_monitor(self):
        self.log("Überwachung aktiv... Suche nach iOS Geräten.")
        # Hier nutzen wir jetzt einen daemon-Thread, der keine neuen Prozesse spawnt
        threading.Thread(target=self.device_check_logic, daemon=True).start()

    def device_check_logic(self):
        import time
        while True:
            # Wir prüfen nur, ob das Tool überhaupt da ist, ohne Endlosschleife bei Fehlern
            try:
                # WICHTIG: Wir rufen pymobiledevice3 NICHT über -m auf, wenn wir unsicher sind
                # sondern checken nur die USB-Liste
                cmd = ["pymobiledevice3", "usbmux", "list"] 
                subprocess.run(cmd, capture_output=True, timeout=5)
            except Exception:
                pass
            time.sleep(10) # Hoher Intervall zur CPU-Schonung

    def run_info(self):
        threading.Thread(target=self._execute_cmd, args=(["diagnostics", "device-info"],)).start()

    def _execute_cmd(self, args):
        try:
            # Sicherer Aufruf
            cmd = ["pymobiledevice3"] + args
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            self.root.after(0, self.log, res.stdout)
        except Exception as e:
            self.root.after(0, self.log, f"Fehler: {str(e)}")

    def emergency_exit(self):
        self.root.quit()
        sys.exit()

if __name__ == "__main__":
    # DAS HIER VERHINDERT DAS DAUERHAFTE ÖFFNEN (FORK BOMB)
    multiprocessing.freeze_support()
    
    root = tk.Tk()
    app = FusionPro(root)
    root.mainloop()
