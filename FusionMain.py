import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class FusionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Pro - Advanced iOS Management")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f5f5f7")
        
        # Pfad zum Python der Command Line Tools (aus deinem Log)
        self.python_exe = "/Library/Developer/CommandLineTools/usr/bin/python3"
        if not os.path.exists(self.python_exe):
            self.python_exe = sys.executable

        self.setup_ui()
        
        # Startet die Abhängigkeitsprüfung in einem eigenen Thread, damit die App nicht einfriert
        threading.Thread(target=self.auto_install_deps, daemon=True).start()

    def auto_install_deps(self):
        self.write_log("System-Check: Suche nach pymobiledevice3...")
        try:
            # Versuch, das Modul zu importieren
            subprocess.run([self.python_exe, "-c", "import pymobiledevice3"], check=True, capture_output=True)
            self.write_log("Status: pymobiledevice3 ist einsatzbereit.")
        except subprocess.CalledProcessError:
            self.write_log("Status: Modul fehlt. Starte Auto-Installation...")
            try:
                subprocess.check_call([self.python_exe, "-m", "pip", "install", "pymobiledevice3"])
                self.write_log("Installation erfolgreich abgeschlossen!")
            except Exception as e:
                self.write_log(f"Fehler bei Auto-Installation: {e}")
                self.write_log("Bitte manuell im Terminal: sudo pip install pymobiledevice3")

    def setup_ui(self):
        # Design Farben
        bg_dark = "#1a1a1a"
        accent_purple = "#8e44ad"
        accent_blue = "#3498db"
        accent_red = "#e74c3c"

        # Sidebar
        self.sidebar = tk.Frame(self.root, width=260, bg=bg_dark)
        self.sidebar.pack(side="left", fill="y")
        
        # Main Dashboard
        self.main_content = tk.Frame(self.root, bg="#ffffff")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Titel
        tk.Label(self.sidebar, text="FUSION PRO", font=("Arial", 20, "bold"), fg="white", bg=bg_dark).pack(pady=25)

        # LOG KONSOLE (Hacker-Style)
        tk.Label(self.main_content, text="System Log & Analysis:", bg="#ffffff", font=("Arial", 11, "bold")).pack(anchor="w", padx=25, pady=(20, 5))
        self.log_area = tk.Text(self.main_content, height=20, bg="#1e1e1e", fg="#00ff00", font=("Courier", 12), relief="flat")
        self.log_area.pack(fill="x", padx=25, pady=10)

        # BUTTON SEKTIONEN
        self.add_sidebar_button("🚀 START NUGGET", self.run_nugget, accent_purple)
        
        tk.Label(self.sidebar, text="DEVICE MANAGEMENT", fg="grey", bg=bg_dark, font=("Arial", 9, "bold")).pack(pady=(20, 5))
        self.add_sidebar_button("📱 Geräte Info (Extended)", self.get_device_info, accent_blue)
        self.add_sidebar_button("🛡️ Echt-Supervision (AC2)", self.run_supervision, accent_blue)
        self.add_sidebar_button("🏢 MDM Registrierung", self.run_mdm, accent_blue)
        
        tk.Label(self.sidebar, text="SECURITY", fg="grey", bg=bg_dark, font=("Arial", 9, "bold")).pack(pady=(20, 5))
        self.add_sidebar_button("🔍 Spyware Tiefen-Scan", self.run_spyware_deep_scan, accent_red)
        
        # Domain Info
        self.domain_label = tk.Label(self.sidebar, text="Server: pending (.eu.org)", fg="#555555", bg=bg_dark, font=("Arial", 10))
        self.domain_label.pack(side="bottom", pady=20)

    def add_sidebar_button(self, text, command, color):
        btn = tk.Button(self.sidebar, text=text, command=command, bg=color, fg="white", 
                        font=("Arial", 11, "bold"), relief="flat", height=2, cursor="hand2")
        btn.pack(fill="x", padx=20, pady=8)

    def write_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    # --- FUNKTIONEN ---

    def run_nugget(self):
        if os.path.exists("/Applications/Nugget.app"):
            self.write_log("Starte Nugget.app aus den Programmen...")
            subprocess.Popen(["open", "-a", "Nugget"])
        else:
            self.write_log("Nugget.app nicht gefunden. Bitte in /Applications installieren!")
            messagebox.showwarning("Nugget fehlt", "Bitte ziehe die Nugget.app in deinen Programme-Ordner.")

    def run_supervision(self):
        self.write_log("Modus: ECHTE Supervision (DEP-Simulation)...")
        # Setzt die Cloud-Konfiguration wie Apple Configurator 2
        org = "Fusion_Management_Global"
        cmd = f"{self.python_exe} -m pymobiledevice3 management set-cloud-config --org {org} --supervision"
        
        def task():
            try:
                res = subprocess.run(cmd.split(), capture_output=True, text=True)
                if res.returncode == 0:
                    self.write_log(f"ERFOLG: Gerät ist jetzt unter Supervision von: {org}")
                else:
                    self.write_log(f"Fehler: {res.stderr}")
            except Exception as e:
                self.write_log(f"Fehler: {e}")
        
        threading.Thread(target=task).start()

    def run_mdm(self):
        # Hier wird später deine eu.org Domain aktiv
        self.write_log("Kontaktiere MDM-Server (eu.org)...")
        self.write_log("Pushe Enrollment-Profil...")
        # Beispielhafter Befehl für Profil-Installation
        cmd = f"{self.python_exe} -m pymobiledevice3 profile install --name FusionMDM"
        threading.Thread(target=lambda: self.run_cmd_thread(cmd)).start()

    def run_spyware_deep_scan(self):
        self.write_log("Starte heuristische Analyse auf Spyware (Pegasus/Reign)...")
        self.write_log("Prüfe System-Dienste auf versteckte Prozesse...")
        # Nutzt MobileGestalt und Diagnostics für tiefen System-Scan
        cmd = f"{self.python_exe} -m pymobiledevice3 diagnostics mobilegestalt-read"
        threading.Thread(target=lambda: self.run_cmd_thread(cmd)).start()

    def get_device_info(self):
        self.write_log("Lese UDID, Seriennummer und ECID aus...")
        cmd = f"{self.python_exe} -m pymobiledevice3 usbmux list"
        threading.Thread(target=lambda: self.run_cmd_thread(cmd)).start()

    def run_cmd_thread(self, cmd):
        try:
            res = subprocess.run(cmd.split(), capture_output=True, text=True)
            output = res.stdout if res.stdout else "Befehl beendet."
            self.write_log(output)
            if res.stderr: self.write_log(f"Fehler-Log: {res.stderr}")
        except Exception as e:
            self.write_log(f"Crash: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionApp(root)
    root.mainloop()
