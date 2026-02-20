import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class FusionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Dashboard - iMazing x Nugget")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f5f7")

        self.setup_ui()
        self.write_log("System gestartet. Suche in /Applications...")

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, width=220, bg="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")
        
        # Main Area
        self.main_content = tk.Frame(self.root, bg="#ffffff")
        self.main_content.pack(side="right", expand=True, fill="both")

        # LOG KONSOLE (Hacker-Style für bessere Lesbarkeit)
        tk.Label(self.main_content, text="System Log:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
        self.log_area = tk.Text(self.main_content, height=18, bg="#1e1e1e", fg="#00ff00", font=("Courier", 11), relief="flat")
        self.log_area.pack(fill="x", padx=20, pady=10)

        # BUTTONS
        tk.Label(self.sidebar, text="STEUERUNG", fg="#8e44ad", bg="#1a1a1a", font=("Arial", 9, "bold")).pack(pady=(20, 5))
        
        tk.Button(self.sidebar, text="START NUGGET", command=self.run_nugget, 
                  bg="#8e44ad", fg="white", font=("Arial", 10, "bold"), height=2).pack(fill="x", padx=20, pady=10)

        ttk.Button(self.sidebar, text="Geräte Info (Live)", command=self.get_device_info).pack(fill="x", padx=20, pady=5)
        
        tk.Label(self.sidebar, text="Domain: eu.org", fg="grey", bg="#1a1a1a", font=("Arial", 8)).pack(side="bottom", pady=10)

    def write_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def find_nugget(self):
        # Wir suchen gezielt im Programme-Ordner
        base_apps = "/Applications"
        if not os.path.exists(base_apps):
            return None, None
            
        for item in os.listdir(base_apps):
            # Wir suchen nach allem, was "Nugget" im Namen hat
            if "Nugget" in item:
                path = os.path.join(base_apps, item)
                if os.path.isdir(path):
                    # Suche nach dem Python-Skript im Ordner
                    for script in ["main.py", "nugget.py", "gui.py", "main_app.py"]:
                        full_script_path = os.path.join(path, script)
                        if os.path.exists(full_script_path):
                            return full_script_path, path
        return None, None

    def run_nugget(self):
        script, folder = self.find_nugget()
        
        if not script:
            self.write_log("Nugget nicht automatisch in /Applications gefunden.")
            folder = filedialog.askdirectory(title="Wähle den Nugget-Ordner unter 'Programme' aus")
            if folder:
                for s in ["main.py", "nugget.py", "gui.py", "main_app.py"]:
                    if os.path.exists(os.path.join(folder, s)):
                        script = os.path.join(folder, s)
                        break
        
        if script:
            self.write_log(f"Starte: {script}")
            try:
                # Nutzt python3 vom Mac
                subprocess.Popen(["/usr/bin/python3", script], cwd=folder)
                self.write_log("ERFOLG: Nugget-Fenster sollte sich gleich öffnen.")
            except Exception as e:
                self.write_log(f"Fehler: {e}")
        else:
            self.write_log("Abbruch: Kein Nugget-Ordner ausgewählt.")

    def get_device_info(self):
        self.write_log("Prüfe Verbindung zu pymobiledevice3...")
        try:
            # Wir versuchen es über den direkten Python-Aufruf
            cmd = "/usr/bin/python3 -m pymobiledevice3 usbmux list"
            res = subprocess.run(cmd.split(), capture_output=True, text=True)
            if res.stdout:
                self.write_log("Gerät erkannt:\n" + res.stdout)
            elif res.stderr:
                self.write_log("Fehler-Info: " + res.stderr)
            else:
                self.write_log("Kein iPhone/iPad via USB gefunden.")
        except Exception as e:
            self.write_log(f"Systemfehler: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionApp(root)
    root.mainloop()
