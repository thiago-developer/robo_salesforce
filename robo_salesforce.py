import os
import time
from os import listdir
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

s = Service("C:\\Users\\Thiago\\Documents\\Projeto_Robo_Salesforce\\Robo_SalesForce\\chromedriver.exe")
print("Iniciando...")
driver = webdriver.Chrome(service=s)
driver.get("https://workbench.developerforce.com/login.php")

# configuracao sandbox
driver.find_element(By.XPATH, value='//*[@id="oauth_env"]').send_keys("Sandbox")