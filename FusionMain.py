import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk
import threading
import datetime
import shutil

# Kompatibilitäts-Import für ältere Python-Versionen (Fix für Exit Code 1)
from typing import Optional, Union

class FusionPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Pro - iOS Enterprise Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ffffff")
        
        # Erkennt automatisch, ob wir in einer PyInstaller-App laufen oder im Skript
        self.python_exe = self.get_python_runtime()
        
        self.setup_ui()
        self.check_loop()

    def get_python_runtime(self):
        """Findet die richtige Python-Umgebung für den Prozess."""
        if getattr(sys, 'frozen', False):
            # Wenn als .app/.exe gebaut, nutze das interne Python
            return sys.executable
        return sys.executable  # Nutzt das aktuelle Interpreter-Environment

    def setup_ui(self):
        # UI Styling wie iMazing / Apple Design
        style = ttk.Style()
        style.theme_use('clam')
        
        # Sidebar
        self.sidebar = tk.Frame(self.root, width=220, bg="#f5f5f7", bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Fusion Pro", font=("Helvetica", 20, "bold"), 
                 bg="#f5f5f7", fg="#1d1d1f").pack(pady=30)

        # Navigation
        self.btn_frame = tk.Frame(self.sidebar, bg="#f5f5f7")
        self.btn_frame.pack(fill="both", expand=True, padx=10)

        self.add_menu_btn("Dashboard", self.cmd_info)
        self.add_menu_btn("Batterie-Check", self.cmd_battery)
        self.add_menu_btn("Supervision On", self.cmd_supervision)
        self.add_menu_btn("System Log", self.cmd_syslog)

        # Main Content
        self.main = tk.Frame(self.root, bg="#ffffff")
        self.main.pack(side="right", expand=True, fill="both", padx=30, pady=30)

        self.status_card = tk.Label(self.main, text="Warte auf Gerät...", font=("Helvetica", 14), 
                                   bg="#f2f2f7", fg="#86868b", height=3, width=50)
        self.status_card.pack(pady=(0, 20))

        self.log_display = tk.Text(self.main, bg="#fafafa", fg="#1d1d1f", font=("Menlo", 11),
                                  relief="flat", highlightthickness=1, highlightbackground="#d2d2d7")
        self.log_display.pack(expand=True, fill="both")

    def add_menu_btn(self, text, command):
        btn = tk.Button(self.btn_frame, text=text, command=command, font=("Helvetica", 12),
                        bg="#f5f5f7", fg="#1d1d1f", relief="flat", anchor="w", 
                        activebackground="#e8e8ed", cursor="hand2", bd=0)
        btn.pack(fill="x", pady=2, ipady=5)

    def log(self, message):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_display.insert(tk.END, f"[{now}] {message}\n")
        self.log_display.see(tk.END)

    # --- Befehle ---

    def check_loop(self):
        """Prüft im Hintergrund, ob ein iPhone verbunden ist."""
        def run():
            while True:
                try:
                    # 'usbmux list' ist der schnellste Weg für den Heartbeat
                    res = subprocess.run([self.python_exe, "-m", "pymobiledevice3", "usbmux", "list"], 
                                         capture_output=True, text=True)
                    if "udid" in res.stdout.lower():
                        self.status_card.config(text="Gerät verbunden ✅", fg="#34c759", bg="#e5f9e7")
                    else:
                        self.status_card.config(text="Kein Gerät erkannt", fg="#86868b", bg="#f2f2f7")
                except: pass
                import time
                time.sleep(5)
        threading.Thread(target=run, daemon=True).start()

    def cmd_info(self):
        self.log("Lese Geräte-Details aus...")
        self.run_pmd3(["diagnostics", "device-info"])

    def cmd_battery(self):
        self.log("Analysiere Batterie-Zyklen (ioregistry)...")
        self.run_pmd3(["diagnostics", "ioregistry", "--entry", "AppleSmartBattery"])

    def cmd_supervision(self):
        self.log("Starte Enterprise-Supervision Prozess...")
        # Nutzt eu.org für das Profil (aus deinen Vorgaben)
        self.run_pmd3(["management", "set-cloud-config", "--org", "Fusion.eu.org", "--supervision"])

    def cmd_syslog(self):
        self.log("Öffne Live-Syslog...")
        # Öffnet ein neues Terminal-Fenster für den Log-Stream
        if sys.platform == "darwin":
            subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "{self.python_exe} -m pymobiledevice3 syslog"'])

    def run_pmd3(self, args):
        """Führt pymobiledevice3 Befehle sicher in einem Thread aus."""
        def thread_task():
            full_cmd = [self.python_exe, "-m", "pymobiledevice3"] + args
            try:
                process = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
                if process.stdout:
                    self.log(process.stdout)
                if process.stderr and "warning" not in process.stderr.lower():
                    self.log(f"Fehler: {process.stderr}")
            except Exception as e:
                self.log(f"Prozess-Fehler: {str(e)}")
        
        threading.Thread(target=thread_task).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionPro(root)
    root.mainloop()
