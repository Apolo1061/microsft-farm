import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
import time

options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")

driver = uc.Chrome(options=options)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})

driver.get("https://www.google.com/recaptcha/api2/demo")

iframe = driver.find_element("xpath", '//iframe[contains(@src,"recaptcha")]')
driver.switch_to.frame(iframe)
checkbox = driver.find_element("id", "recaptcha-anchor")

actions = ActionChains(driver)
actions.move_to_element(checkbox)
actions.pause(1)
actions.click()
actions.perform()

driver.switch_to.default_content()
time.sleep(5)

submit_btn = driver.find_element("id", "recaptcha-demo-submit")
actions = ActionChains(driver)
actions.move_to_element(submit_btn)
actions.pause(2)
actions.click()
actions.perform()

time.sleep(2)
driver.save_screenshot("recaptchat.png")
print("Captura tomada")
driver.quit()