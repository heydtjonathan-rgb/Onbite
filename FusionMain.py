import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Findet Dateien innerhalb des Pakets (Wichtig für .exe/.dmg)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class FusionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion: Nugget x iMazing")
        self.root.geometry("850x600")
        
        # Nugget-Pfad Logik
        self.base_dir = resource_path("Nugget")
        # Wir suchen nach der Startdatei (da main_app.py fehlte)
        self.nugget_script = self.find_nugget_start()
        
        self.setup_ui()

    def find_nugget_start(self):
        # Wir prüfen alle gängigen Namen für das Nugget-Skript
        for name in ["main_app.py", "main.py", "nugget.py", "gui.py"]:
            full_path = os.path.join(self.base_dir, name)
            if os.path.exists(full_path):
                return full_path
        return None

    def setup_ui(self):
        # Sidebar Design
        self.sidebar = tk.Frame(self.root, width=220, bg="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")
        
        self.main_content = tk.Frame(self.root, bg="#ffffff")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Status Check
        status_color = "#2ecc71" if self.nugget_script else "#e74c3c"
        tk.Label(self.sidebar, text="SYSTEM STATUS", fg="white", bg="#1a1a1a", font=("Arial", 10, "bold")).pack(pady=20)
        tk.Label(self.sidebar, text="Nugget: Aktiv" if self.nugget_script else "Nugget: Fehlend", 
                 fg=status_color, bg="#1a1a1a").pack(pady=5)

        # Buttons: Nugget
        tk.Label(self.sidebar, text="Jailbreak Mode", fg="#f1c40f", bg="#1a1a1a").pack(pady=15)
        tk.Button(self.sidebar, text="START NUGGET", command=self.run_nugget, bg="#f1c40f").pack(fill="x", padx=20)

        # Buttons: iMazing
        tk.Label(self.sidebar, text="iMazing Mode", fg="#3498db", bg="#1a1a1a").pack(pady=15)
        ttk.Button(self.sidebar, text="Geräte Info", command=self.get_info).pack(fill="x", padx=20, pady=2)
        ttk.Button(self.sidebar, text="Backup Browser", command=lambda: messagebox.showinfo("iMazing", "Suche Backups...")).pack(fill="x", padx=20, pady=2)

    def run_nugget(self):
        if not self.nugget_script:
            messagebox.showerror("Fehler", "Nugget Startdatei nicht gefunden!")
            return
        subprocess.Popen([sys.executable, self.nugget_script], cwd=self.base_dir)

    def get_info(self):
        try:
            res = subprocess.check_output(["pymobiledevice3", "usbmux", "list"], text=True)
            messagebox.showinfo("iMazing Device Info", res)
        except:
            messagebox.showerror("Fehler", "Verbindung fehlgeschlagen. Ist pymobiledevice3 installiert?")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionApp(root)
    root.mainloop()
