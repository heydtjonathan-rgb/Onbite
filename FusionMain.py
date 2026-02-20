import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class FusionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Dashboard")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f5f7")
        
        # Python Pfad für pymobiledevice3
        self.python_exe = "/Library/Developer/CommandLineTools/usr/bin/python3"

        self.setup_ui()
        self.write_log("Fusion System bereit.")

    def setup_ui(self):
        self.sidebar = tk.Frame(self.root, width=220, bg="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")
        self.main_content = tk.Frame(self.root, bg="#ffffff")
        self.main_content.pack(side="right", expand=True, fill="both")

        # LOG KONSOLE
        tk.Label(self.main_content, text="System Log:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
        self.log_area = tk.Text(self.main_content, height=18, bg="#1e1e1e", fg="#00ff00", font=("Courier", 11), relief="flat")
        self.log_area.pack(fill="x", padx=20, pady=10)

        # BUTTONS
        tk.Label(self.sidebar, text="STEUERUNG", fg="#8e44ad", bg="#1a1a1a", font=("Arial", 9, "bold")).pack(pady=(20, 5))
        
        # Der Button startet jetzt die App oder öffnet die DMG
        tk.Button(self.sidebar, text="START NUGGET", command=self.run_nugget, 
                  bg="#8e44ad", fg="white", font=("Arial", 10, "bold"), height=2).pack(fill="x", padx=20, pady=10)

        ttk.Button(self.sidebar, text="Geräte Info (Live)", command=self.get_device_info).pack(fill="x", padx=20, pady=5)
        
        tk.Label(self.sidebar, text="Domain: eu.org", fg="grey", bg="#1a1a1a", font=("Arial", 8)).pack(side="bottom", pady=10)

    def write_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def run_nugget(self):
        self.write_log("Suche Nugget App oder DMG...")
        
        # 1. Check ob Nugget bereits in Programme installiert ist
        if os.path.exists("/Applications/Nugget.app"):
            self.write_log("Nugget App in /Applications gefunden. Starte...")
            subprocess.Popen(["open", "-a", "Nugget"])
            return

        # 2. Check ob die DMG in Downloads oder Programme liegt
        home = os.path.expanduser("~")
        search_files = [
            "/Applications/Nugget.dmg",
            os.path.join(home, "Downloads", "Nugget.dmg"),
            os.path.join(home, "Desktop", "Nugget.dmg")
        ]
        
        found_file = None
        for f in search_files:
            if os.path.exists(f):
                found_file = f
                break
        
        # 3. Manueller Fallback
        if not found_file:
            self.write_log("Nugget nicht gefunden. Bitte .app oder .dmg wählen.")
            found_file = filedialog.askopenfilename(title="Wähle Nugget (.app oder .dmg)")

        if found_file:
            self.write_log(f"Öffne: {found_file}")
            subprocess.Popen(["open", found_file])
        else:
            self.write_log("Abbruch: Keine Datei ausgewählt.")

    def get_device_info(self):
        self.write_log("Rufe Geräte-Informationen ab...")
        try:
            cmd = f"{self.python_exe} -m pymobiledevice3 usbmux list"
            res = subprocess.run(cmd.split(), capture_output=True, text=True)
            if res.stdout:
                self.write_log(res.stdout)
            else:
                self.write_log("Kein Gerät erkannt. Kabel prüfen!")
                if res.stderr: self.write_log(f"Fehler: {res.stderr}")
        except Exception as e:
            self.write_log(f"Systemfehler: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionApp(root)
    root.mainloop()
