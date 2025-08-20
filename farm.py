import requests
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import sys
import signal
import json
import os

DATO3 = "datos.json"

def rutadriver():
    if os.path.exists(DATO3):
        with open(DATO3, "r", encoding="utf-8") as f:
            datos = json.load(f)
            ruta = datos.get("msedgedriver_path")
            if ruta and os.path.exists(ruta):
                return ruta

    ruta = input("[ ? ] Introduce la ruta > ").strip()
    while not os.path.exists(ruta):
        print("[ X ] Ruta invalida, intenta de nuevo.")
        ruta = input("[ ? ] Introduce la ruta > ").strip()

    with open(DATO3, "w", encoding="utf-8") as f:
        json.dump({"msedgedriver_path": ruta}, f)

    return ruta

driver_path = rutadriver()

# Config edge
opts = Options()
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_argument("--start-maximized")
opts.add_argument("--headless")
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81"
opts.add_argument(f"user-agent={ua}")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)

srv = Service(driver_path)
drv = webdriver.Edge(service=srv, options=opts)
drv.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    }
)

def stop(sig, frame):
    print("\nFinalizando procesos...")
    drv.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, stop)

def palabra():
    try:
        res = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        if res.status_code == 200:
            return res.json()[0]
        else:
            raise Exception("API NO RESPONDE")
    except Exception:
        print("ERROR: La API necesita actualizarse")
        drv.quit()
        sys.exit(1)

n_busq = 45

try:
    for _ in range(n_busq):
        t = palabra()
        drv.get("https://www.bing.com")
        time.sleep(random.uniform(2, 4))

        caja = drv.find_element(By.NAME, "q")
        caja.clear()
        caja.send_keys(t)
        caja.submit()

        print(f"Buscando: {t}")
        time.sleep(random.uniform(3, 6))
        #drv.save_screenshot(f"resultado_{t[:10]}.png")  #<-- screenshot

finally:
    drv.quit()
    print("Script finalizado.")
