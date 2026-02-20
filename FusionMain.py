import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class FusionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion: Dashboard (Nugget & iMazing)")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f5f7")

        self.setup_ui()
        self.write_log("Fusion System gestartet.")
        self.write_log("Prüfe Programme-Ordner auf Nugget...")

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, width=220, bg="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")
        
        # Main Area
        self.main_content = tk.Frame(self.root, bg="#ffffff")
        self.main_content.pack(side="right", expand=True, fill="both")

        # LOG KONSOLE
        tk.Label(self.main_content, text="System Log:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
        self.log_area = tk.Text(self.main_content, height=15, bg="#f0f0f0", font=("Courier", 11), relief="flat")
        self.log_area.pack(fill="x", padx=20, pady=10)

        # BUTTONS
        tk.Label(self.sidebar, text="MODUL CONTROL", fg="#8e44ad", bg="#1a1a1a", font=("Arial", 9, "bold")).pack(pady=(20, 5))
        
        tk.Button(self.sidebar, text="START NUGGET", command=self.run_nugget, 
                  bg="#8e44ad", fg="white", font=("Arial", 10, "bold")).pack(fill="x", padx=20, pady=10)

        ttk.Button(self.sidebar, text="Geräte Info (Live)", command=self.get_device_info).pack(fill="x", padx=20, pady=2)
        
        tk.Label(self.sidebar, text="Domain: eu.org (pending)", fg="grey", bg="#1a1a1a", font=("Arial", 8)).pack(side="bottom", pady=10)

    def write_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def find_nugget(self):
        # Wir suchen nach dem Ordner in Applications
        base_apps = "/Applications"
        # Wir suchen nach "Nugget", "Nugget-main", etc.
        for folder in os.listdir(base_apps):
            if "Nugget" in folder:
                full_folder_path = os.path.join(base_apps, folder)
                if os.path.isdir(full_folder_path):
                    # Suche nach dem Skript im Ordner
                    for script in ["main.py", "nugget.py", "gui.py", "main_app.py"]:
                        script_path = os.path.join(full_folder_path, script)
                        if os.path.exists(script_path):
                            return script_path, full_folder_path
        return None, None

    def run_nugget(self):
        script_path, folder_path = self.find_nugget()
        
        # Falls die Automatik im Programme-Ordner scheitert
        if not script_path:
            self.write_log("Nugget nicht in /Applications gefunden. Bitte manuell wählen.")
            selected = filedialog.askdirectory(title="Wähle den Nugget-Ordner aus")
            if selected:
                for script in ["main.py", "nugget.py", "gui.py"]:
                    if os.path.exists(os.path.join(selected, script)):
                        script_path = os.path.join(selected, script)
                        folder_path = selected
                        break
        
        if script_path:
            self.write_log(f"Starte: {script_path}")
            try:
                # Nutzt 'python3' direkt aus dem System-Pfad
                subprocess.Popen(["python3", script_path], cwd=folder_path)
                self.write_log("Nugget erfolgreich gestartet.")
            except Exception as e:
                self.write_log(f"Fehler: {e}")
        else:
            self.write_log("Abbruch: Kein Nugget-Skript gefunden.")

    def get_device_info(self):
        self.write_log("Suche Geräte...")
        try:
            # Versucht pymobiledevice3 über die Shell aufzurufen
            res = subprocess.run("python3 -m pymobiledevice3 usbmux list", shell=True, capture_output=True, text=True)
            if res.stdout:
                self.write_log(res.stdout)
            else:
                self.write_log("Kein Gerät gefunden oder Fehler.")
                if res.stderr: self.write_log(f"Error: {res.stderr}")
        except Exception as e:
            self.write_log(f"Systemfehler: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionApp(root)
    root.mainloop()
