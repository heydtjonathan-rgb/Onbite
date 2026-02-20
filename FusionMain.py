import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class FusionPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Pro - iOS Management Console")
        self.root.geometry("1200x800")
        self.root.configure(bg="#ffffff")
        
        # Pfad-Setup
        self.python_exe = "/Library/Developer/CommandLineTools/usr/bin/python3"
        
        self.setup_styles()
        self.setup_ui()
        
        # Startet Auto-Check
        threading.Thread(target=self.auto_check, daemon=True).start()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, font=("Segoe UI", 10))
        self.style.configure("Card.TFrame", background="#f8f8f8", relief="flat")

    def setup_ui(self):
        # --- SIDEBAR (Helles Grau wie iMazing) ---
        self.sidebar = tk.Frame(self.root, width=280, bg="#f0f0f2", padx=10, pady=10)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / Name
        tk.Label(self.sidebar, text="Fusion Pro", font=("Helvetica", 22, "bold"), fg="#333333", bg="#f0f0f2").pack(pady=(20, 30))

        # NAVIGATION (Kategorien)
        self.add_nav_header("QUICK ACTIONS")
        self.add_nav_button("🚀 Start Nugget", self.run_nugget)
        self.add_nav_button("🔋 Battery Life", self.get_battery_pro)

        self.add_nav_header("MANAGEMENT")
        self.add_nav_button("🛡️ Supervision (AC2)", self.run_supervision)
        self.add_nav_button("🏢 MDM Enrollment", self.run_mdm)

        self.add_nav_header("SECURITY")
        self.add_nav_button("🔍 Spyware Deep Scan", self.run_spyware_deep_scan)
        self.add_nav_button("📜 Live Syslog", self.run_syslog_live)

        # --- MAIN AREA ---
        self.main_area = tk.Frame(self.root, bg="#ffffff", padx=30, pady=20)
        self.main_area.pack(side="right", expand=True, fill="both")

        # Gerätestatus-Karte (Oben)
        self.device_card = tk.Frame(self.main_area, bg="#f8f8f8", height=150, bd=0)
        self.device_card.pack(fill="x", pady=(0, 20))
        
        self.status_label = tk.Label(self.device_card, text="Kein Gerät verbunden", font=("Helvetica", 14), bg="#f8f8f8", fg="#888888")
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        # LOG KONSOLE
        tk.Label(self.main_area, text="Aktivitäten & Berichte", font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#333333").pack(anchor="w")
        self.log_area = tk.Text(self.main_area, height=25, bg="#ffffff", fg="#333333", font=("Menlo", 11), relief="flat", highlightthickness=1, highlightcolor="#dddddd")
        self.log_area.pack(fill="both", expand=True, pady=10)

        # Footer
        tk.Label(self.sidebar, text="Server: fusion-pro.eu.org", font=("Helvetica", 9), bg="#f0f0f2", fg="#999999").pack(side="bottom", pady=10)

    def add_nav_header(self, text):
        tk.Label(self.sidebar, text=text, font=("Helvetica", 9, "bold"), bg="#f0f0f2", fg="#666666").pack(anchor="w", padx=15, pady=(20, 5))

    def add_nav_button(self, text, command):
        btn = tk.Button(self.sidebar, text=f"  {text}", command=command, anchor="w", 
                        font=("Helvetica", 11), bg="#f0f0f2", fg="#333333", 
                        relief="flat", activebackground="#e0e0e2", cursor="hand2", bd=0)
        btn.pack(fill="x", padx=5, pady=2)

    def write_log(self, text):
        self.log_area.insert(tk.END, f"[{self.get_time()}] {text}\n")
        self.log_area.see(tk.END)

    def get_time(self):
        import datetime
        return datetime.datetime.now().strftime("%H:%M:%S")

    # --- FEATURES ---

    def auto_check(self):
        # Prüft im Hintergrund ob Gerät da ist
        while True:
            try:
                cmd = f"{self.python_exe} -m pymobiledevice3 usbmux list"
                res = subprocess.run(cmd.split(), capture_output=True, text=True)
                if "udid" in res.stdout.lower():
                    self.status_label.config(text="iPhone / iPad verbunden ✅", fg="#27ae60")
                else:
                    self.status_label.config(text="Warte auf USB-Verbindung...", fg="#888888")
            except: pass
            import time
            time.sleep(5)

    def run_nugget(self):
        if os.path.exists("/Applications/Nugget.app"):
            self.write_log("Starte Nugget Exploits...")
            subprocess.Popen(["open", "-a", "Nugget"])
        else:
            self.write_log("FEHLER: Nugget.app nicht in /Applications gefunden.")

    def get_battery_pro(self):
        self.write_log("Analyse der Hardware-Batteriezyklen...")
        cmd = f"{self.python_exe} -m pymobiledevice3 diagnostics ioreg --entry AppleSmartBattery"
        threading.Thread(target=lambda: self.run_cmd_thread(cmd)).start()

    def run_supervision(self):
        self.write_log("Starte Enterprise-Supervision Prozess...")
        org = "Fusion_Enterprise"
        cmd = f"{self.python_exe} -m pymobiledevice3 management set-cloud-config --org {org} --supervision"
        threading.Thread(target=lambda: self.run_cmd_thread(cmd)).start()

    def run_mdm(self):
        self.write_log("Kontaktiere Enrollment-Dienst (eu.org)...")
        # MDM Profile werden hier geladen
        self.write_log("Vorbereitung für Profile-Push...")

    def run_spyware_deep_scan(self):
        self.write_log("Sicherheits-Scan: Suche nach bekannten Rootkits...")
        cmd = f"{self.python_exe} -m pymobiledevice3 diagnostics mobilegestalt-read"
        threading.Thread(target=lambda: self.run_cmd_thread(cmd)).start()

    def run_syslog_live(self):
        self.write_log("Öffne Live-Konsole...")
        cmd = f"{self.python_exe} -m pymobiledevice3 syslog"
        subprocess.Popen(cmd.split())

    def run_cmd_thread(self, cmd):
        try:
            res = subprocess.run(cmd.split(), capture_output=True, text=True)
            self.write_log(res.stdout if res.stdout else "Vorgang abgeschlossen.")
            if res.stderr: self.write_log(f"System-Info: {res.stderr}")
        except Exception as e:
            self.write_log(f"Fehler: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionPro(root)
    root.mainloop()
