import requests, random, time, sys, threading, signal, webbrowser, os
import customtkinter as ctk
from customtkinter import CTkImage
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO

try:
    import winreg
except ImportError:
    print("[ X ] Solo funciona en Windows")
    sys.exit(1)

REG_PATH = r"Software\\MSEdgeDriverConfig"

def save_reg(val: str):
    k = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    winreg.SetValueEx(k, "DriverPath", 0, winreg.REG_SZ, val)
    winreg.CloseKey(k)

def load_reg():
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(k, "DriverPath")
        winreg.CloseKey(k)
        if os.path.exists(val):
            return val
    except FileNotFoundError:
        return None
    return None

def splash(root, next_f):
    sp = ctk.CTkToplevel(root)
    sp.title("When Community")
    sp.geometry("500x300+600+300")
    sp.configure(fg_color="#0d1117")
    sp.overrideredirect(False)
    f = ctk.CTkFrame(sp, fg_color="#0d1117", corner_radius=30)
    f.pack(expand=True, fill="both", padx=10, pady=10)

    url = "https://media.discordapp.net/attachments/1346725481046872148/1409703421619212378/images-removebg-preview_1.png?ex=68ae581e&is=68ad069e&hm=798116d15d2786146f4352ee654fbe4ce233821d54b2e950b8c32d26b9c383a1&=&format=webp&quality=lossless"
    r = requests.get(url)
    img = Image.open(BytesIO(r.content))
    w = 90
    h = int((w / img.width) * img.height)
    pil_img = img.resize((w,h), Image.Resampling.LANCZOS)
    logo = CTkImage(pil_img, size=(w,h))

    ctk.CTkLabel(f, image=logo, text="").pack(pady=15)
    ctk.CTkLabel(f, text="MICROSOFT REWIND", font=("Segoe UI", 20, "bold"), text_color="#00aaff").pack(pady=10)
    ctk.CTkLabel(f, text="Iniciando ...", font=("Segoe UI", 12), text_color="white").pack(pady=5)
    pb = ctk.CTkProgressBar(f, width=350)
    pb.pack(pady=20)

    def run_pb():
        for i in range(101):
            pb.set(i/100)
            sp.update_idletasks()
            time.sleep(0.03)
        sp.destroy()
        next_f()
    threading.Thread(target=run_pb, daemon=True).start()

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x700")
        self.root.title("When Community")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(fg_color="#001f3f")

        frame = ctk.CTkFrame(root, fg_color="#001a3f", corner_radius=20)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        url_logo = "https://media.discordapp.net/attachments/1346725481046872148/1409698385887367270/Screenshot_2025-08-12-19-37-59-220_com.android.chrome.png?ex=68ae536e&is=68ad01ee&hm=c15e6de29017be95af395c3bca0cc2e10c2c9caf7d395dfa1cdeafbaf2294b6e&=&format=webp&quality=lossless"
        r = requests.get(url_logo)
        img = Image.open(BytesIO(r.content))
        w = 55
        h = int((w / img.width) * img.height)
        pil_logo = img.resize((w,h), Image.Resampling.LANCZOS)
        self.logo = CTkImage(pil_logo, size=(w,h))

        top = ctk.CTkFrame(frame, fg_color="#001a3f", corner_radius=0)
        top.pack(fill="x", pady=(10,20))
        ctk.CTkLabel(top, image=self.logo, text="", width=w, height=h).pack(side="left", padx=10)
        ctk.CTkLabel(top, text="When Community", font=("Segoe UI", 18, "bold"), text_color="#00aaff").pack(side="left", padx=10)

        self.driver = None
        self.driver_path = load_reg()
        self.running = False
        self.num_b = 40

        entry_f = ctk.CTkFrame(frame, fg_color="#0d1117", corner_radius=15)
        entry_f.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(entry_f, text="Busquedas:", text_color="white").pack(side="left", padx=5)
        self.entry = ctk.CTkEntry(entry_f, width=60, placeholder_text="40", corner_radius=10)
        self.entry.pack(side="left", padx=5)

        self.start_btn = ctk.CTkButton(frame, text="▶ START", fg_color="#00cc66", hover_color="#00ff88", corner_radius=20,
                                       command=self.start_bot)
        self.start_btn.pack(pady=15)
        self.stop_btn = ctk.CTkButton(frame, text="■ STOP", fg_color="#cc0033", hover_color="#ff3355", corner_radius=20,
                                      command=self.stop_bot)
        self.stop_btn.pack(pady=5)

        self.log = ctk.CTkTextbox(frame, height=200, width=650, corner_radius=15, fg_color="#1e1e2f", text_color="#00ffcc")
        self.log.pack(pady=20, fill="x", expand=True)
        self.log.configure(state="disabled")

        self.pb = ctk.CTkProgressBar(frame, width=600)
        self.pb.pack(pady=10)
        self.pb.configure(mode="determinate")
        self.pb.set(0)

        self.label_p = ctk.CTkLabel(frame, text="40 búsquedas = 90 puntos", text_color="#00aaff")
        self.label_p.pack(pady=15)

        footer = ctk.CTkFrame(frame, fg_color="#001a3f", corner_radius=0)
        footer.pack(side="bottom", fill="x", pady=10)
        url_credit = "https://media.discordapp.net/attachments/1346725481046872148/1409699367333396590/images-removebg-preview.png?ex=68ae5458&is=68ad02d8&hm=377761240cf7e51cc2e6dcc0ab2b86b1575a9dedaca433804ca0f9e729c44344&=&format=webp&quality=lossless"
        r = requests.get(url_credit)
        pil_credit = Image.open(BytesIO(r.content)).resize((40,40), Image.Resampling.LANCZOS)
        self.credit = CTkImage(pil_credit)
        ctk.CTkLabel(footer, image=self.credit, text="").pack(side="left", padx=5)

        def open_dc(event=None): webbrowser.open("https://discord.gg/q8WyCQhgMt")
        label_dc = ctk.CTkLabel(footer, text="When Community DC", text_color="#00aaff", cursor="hand2")
        label_dc.pack(side="left", padx=5)
        label_dc.bind("<Button-1>", open_dc)

    def log_msg(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def ask_driver(self):
        from tkinter import filedialog, messagebox
        path = filedialog.askopenfilename(title="Selecciona msedgedriver.exe", filetypes=[("Driver","*.exe")])
        if path:
            save_reg(path)
            self.driver_path = path
        else:
            messagebox.showerror("Error", "Necesitas seleccionar el driver")
            self.root.quit()

    def config_driver(self):
        opts = Options()
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--start-maximized")
        opts.add_argument("--headless")
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81"
        opts.add_argument(f"user-agent={ua}")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        srv = Service(self.driver_path)
        drv = webdriver.Edge(service=srv, options=opts)
        drv.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                            {"source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"})
        return drv

    def palabra(self):
        try:
            r = requests.get("https://random-word-api.herokuapp.com/word?number=1")
            if r.status_code == 200: return r.json()[0]
            else: raise Exception("API NO RESPONDE")
        except Exception:
            self.log_msg("ERROR: La API necesita actualizarse")
            if self.driver: self.driver.quit()
            sys.exit(1)

    def run_bot(self):
        if not self.driver_path: self.ask_driver()
        try: self.num_b = int(self.entry.get())
        except: self.num_b = 40
        self.label_p.configure(text=f"{self.num_b} búsquedas = {int(self.num_b*2.25)} puntos")

        self.driver = self.config_driver()
        self.running = True
        self.pb.set(0)

        try:
            for i in range(self.num_b):
                if not self.running: break
                w = self.palabra()
                self.driver.get("https://www.bing.com")
                time.sleep(random.uniform(2,4))
                caja = self.driver.find_element(By.NAME, "q")
                caja.clear()
                caja.send_keys(w)
                caja.submit()
                self.log_msg(f"🔍 Buscando: {w}")
                self.pb.set((i+1)/self.num_b)
                self.root.update_idletasks()
                time.sleep(random.uniform(3,6))
        finally:
            if self.driver: self.driver.quit()
            self.running = False
            self.log_msg("✅ Finalizado.")

    def start_bot(self):
        if not self.running: threading.Thread(target=self.run_bot, daemon=True).start()

    def stop_bot(self):
        if self.running: 
            self.running = False
            self.log_msg("⛔ Deteniendo ...")

def main():
    root = ctk.CTk()
    root.withdraw()
    root.title("When Community")

    def launch(): root.deiconify(); App(root)
    splash(root, launch)
    root.mainloop()

signal.signal(signal.SIGINT, lambda s,f: sys.exit(0))
main()
