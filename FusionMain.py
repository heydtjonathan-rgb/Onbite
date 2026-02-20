import sys
import os
import subprocess
import tkinter as tk
import threading
import multiprocessing

class FusionPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusion Pro v3.2")
        self.root.geometry("800x600")
        
        # Bestimmt den Pfad zum internen Python der App
        self.executor = [sys.executable, "-m", "pymobiledevice3"]
        
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#ffffff")
        tk.Label(self.root, text="Fusion Pro - GitHub Build", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.log_area = tk.Text(self.root, height=15, bg="#1e1e1e", fg="#34c759", font=("Menlo", 10))
        self.log_area.pack(padx=20, fill="both", expand=True)
        
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Device Scan", command=self.scan_device).pack(side="left", padx=10)

    def log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def scan_device(self):
        def run():
            try:
                # Nutzt sys.executable, um die interne Engine der App aufzurufen
                cmd = self.executor + ["usbmux", "list"]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                output = res.stdout if res.stdout else "Kein Gerät erkannt (Prüfe USB)."
                self.root.after(0, self.log, output)
            except Exception as e:
                self.root.after(0, self.log, f"Fehler: {str(e)}")
        
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    # CRITICAL: Verhindert, dass GitHub/macOS hängen bleibt
    multiprocessing.freeze_support()
    
    # Prüft, ob wir nur einen Unterbefehl ausführen (interne Engine)
    if len(sys.argv) > 1 and sys.argv[1] == "-m":
        # Hier lassen wir pymobiledevice3 die Arbeit machen, ohne die GUI zu laden
        from pymobiledevice3.__main__ import main
        main()
    else:
        # Normaler App-Start
        root = tk.Tk()
        app = FusionPro(root)
        root.mainloop()
