import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk
import threading
import datetime

class FusionPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Pro - iOS Management")
        self.root.geometry("1100x750")
        self.root.configure(bg="#ffffff")
        
        # --- AUTO-PATH SETUP ---
        # Wir suchen nach Python 3.10+, um den TypeError (|) zu vermeiden
        self.python_exe = self.find_best_python()
        
        self.setup_ui()
        threading.Thread(target=self.auto_check, daemon=True).start()

    def find_best_python(self):
        paths = [
            "/opt/homebrew/bin/python3.12",
            "/usr/local/bin/python3.12",
            "python3.11",
            "python3"
        ]
        for p in paths:
            try:
                # Prüfen ob Version >= 3.10
                res = subprocess.run([p, "-c", "import sys; print(sys.version_info >= (3,10))"], 
                                     capture_output=True, text=True)
                if "True" in res.stdout:
                    return p
            except: continue
        return "python3" # Fallback

    def setup_ui(self):
        # SIDEBAR
        self.sidebar = tk.Frame(self.root, width=250, bg="#f2f2f7", padx=0, pady=10)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Fusion Pro", font=("Helvetica Neue", 24, "bold"), 
                 fg="#1c1c1e", bg="#f2f2f7").pack(pady=(20, 40))

        # NAV BUTTONS
        self.add_nav_header("GERÄT")
        self.add_nav_button("📊 Dashboard", self.device_info)
        self.add_nav_button("🔋 Batterie Pro", self.get_battery_pro)
        
        self.add_nav_header("STEUERUNG")
        self.add_nav_button("🛡️ Supervision", self.run_supervision)
        self.add_nav_button("🌐 MDM Setup", self.run_mdm)
        
        self.add_nav_header("ANALYSE")
        self.add_nav_button("🔍 Security Scan", self.run_security_scan)
        self.add_nav_button("📋 System Log", self.run_syslog_live)

        # MAIN AREA
        self.main_area = tk.Frame(self.root, bg="#ffffff", padx=40, pady=30)
        self.main_area.pack(side="right", expand=True, fill="both")

        # DEVICE CARD
        self.device_card = tk.Frame(self.main_area, bg="#f2f2f7", height=120)
        self.device_card.pack(fill="x", pady=(0, 30))
        self.device_card.pack_propagate(False)
        
        self.status_label = tk.Label(self.device_card, text="Suche Gerät...", 
                                     font=("Helvetica Neue", 16), bg="#f2f2f7", fg="#8e8e93")
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        # LOG
        tk.Label(self.main_area, text="PROZESS-AUSGABE", font=("Helvetica", 10, "bold"), 
                 bg="#ffffff", fg="#c7c7cc").pack(anchor="w")
        self.log_area = tk.Text(self.main_area, height=20, bg="#ffffff", fg="#1c1c1e", 
                                font=("Menlo", 11), relief="flat", highlightthickness=1, 
                                highlightbackground="#e5e5ea")
        self.log_area.pack(fill="both", expand=True, pady=10)

    def add_nav_header(self, text):
        tk.Label(self.sidebar, text=text, font=("Helvetica", 10, "bold"), 
                 bg="#f2f2f7", fg="#8e8e93").pack(anchor="w", padx=20, pady=(15, 5))

    def add_nav_button(self, text, command):
        btn = tk.Button(self.sidebar, text=f"  {text}", command=command, anchor="w", 
                        font=("Helvetica Neue", 12), bg="#f2f2f7", fg="#1c1c1e", 
                        relief="flat", activebackground="#e5e5ea", cursor="hand2", bd=0)
        btn.pack(fill="x", padx=10, pady=1)

    def write_log(self, text):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {text}\n")
        self.log_area.see(tk.END)

    # --- ACTIONS ---

    def auto_check(self):
        while True:
            try:
                cmd = [self.python_exe, "-m", "pymobiledevice3", "usbmux", "list"]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if "udid" in res.stdout.lower
