import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

def resource_path(relative_path):
    """ Hilfsfunktion für PyInstaller Pfade (EXE/DMG) """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class FusionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion: Dashboard (Nugget & iMazing)")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f5f7")

        self.setup_ui()
        self.write_log("Fusion System gestartet.")
        self.write_log("Suche nach Nugget-Modulen...")

    def setup_ui(self):
        # Sidebar (Dunkel)
        self.sidebar = tk.Frame(self.root, width=220, bg="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")
        
        # Main Area (Hell)
        self.main_content = tk.Frame(self.root, bg="#ffffff")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Titel in Sidebar
        tk.Label(self.sidebar, text="FUSION", font=("Arial", 18, "bold"), fg="white", bg="#1a1a1a").pack(pady=20)

        # LOG KONSOLE
        tk.Label(self.main_content, text="System Log / Output:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
        self.log_area = tk.Text(self.main_content, height=15, bg="#f0f0f0", font=("Courier", 11), relief="flat")
        self.log_area.pack(fill="x", padx=20, pady=10)

        # BUTTONS - NUGGET SEKTION
        tk.Label(self.sidebar, text="JAILBREAK / EXPLOITS", fg="#8e44ad", bg="#1a1a1a", font=("Arial", 9, "bold")).pack(pady=(20, 5))
        
        self.btn_nugget = tk.Button(self.sidebar, text="START NUGGET", command=self.run_nugget, 
                                   bg="#8e44ad", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10)
        self.btn_nugget.pack(fill="x", padx=20, pady=10)

        # BUTTONS - IMAZING SEKTION
        tk.Label(self.sidebar, text="IMAZING FEATURES", fg="#3498db", bg="#1a1a1a", font=("Arial", 9, "bold")).pack(pady=(20, 5))
        
        ttk.Button(self.sidebar, text="Geräte Info (Live)", command=self.get_device_info).pack(fill="x", padx=20, pady=2)
        ttk.Button(self.sidebar, text="Backup Browser", command=lambda: self.write_log("Backup Browser wird geladen...")).pack(fill="x", padx=20, pady=2)
        
        # Footer
        tk.Label(self.sidebar, text="Domain: eu.org (pending)", fg="grey", bg="#1a1a1a", font=("Arial", 8)).pack(side="bottom", pady=10)

    def write_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def find_nugget(self):
        """ Sucht Nugget an verschiedenen Orten """
        home = os.path.expanduser("~")
        search_paths = [
            resource_path("Nugget"),                   # Im App-Bundle (GitHub Version)
            os.path.join(home, "Downloads", "Nugget"), # Separater Download-Ordner
            os.path.join(home, "Documents", "Nugget"), 
            "/Applications/Nugget"                     # Falls als App installiert
        ]
        
        for path in search_paths:
            for script_name in ["main.py", "nugget.py", "main_app.py", "gui.py"]:
                full_path = os.path.join(path, script_name)
                if os.path.exists(full_path):
                    return full_path, path
        return None, None

    def run_nugget(self):
        script_path, folder_path = self.find_nugget()
        
        if not script_path:
            self.write_log("FEHLER: Nugget konnte nicht gefunden werden!")
            messagebox.showerror("Pfad-Fehler", "Nugget-Installation wurde nicht gefunden.\n\nBitte stelle sicher, dass der Ordner 'Nugget' in deinen Downloads liegt.")
            return

        self.write_log(f"Nugget gefunden: {script_path}")
        try:
            # Startet Nugget mit dem System-Python3
            subprocess.Popen(["python3", script_path], cwd=folder_path)
            self.write_log("Nugget erfolgreich gestartet.")
        except Exception as e:
            self.write_log(f"Fehler beim Start: {str(e)}")

    def get_device_info(self):
        self.write_log("Frage USB-Bus nach iOS-Geräten...")
        try:
            # Nutzt pymobiledevice3 (muss installiert sein: pip install pymobiledevice3)
            result = subprocess.run(["pymobiledevice3", "usbmux", "list"], capture_output=True, text=True)
            if result.stdout:
                self.write_log(f"Geräte gefunden:\n{result.stdout}")
            else:
                self.write_log("Kein Gerät erkannt. Kabel prüfen!")
        except Exception as e:
            self.write_log("Fehler: pymobiledevice3 ist nicht installiert.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionApp(root)
    root.mainloop()
