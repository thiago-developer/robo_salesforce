import os
import pathlib
import time
from os import listdir
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TesteTag:

    def __init__(self, id_objeto, caminho_arquivos, caminho_driver):
        self.id_objeto = id_objeto
        self.caminho_arquivos = caminho_arquivos
        self._caminho_driver = caminho_driver


    def envia_arquivos_org_institucional(self):

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        s = Service(self._caminho_driver)
        print("Iniciando robo...")
        driver = webdriver.Chrome(options=options, service=s)
        driver.get(f"https://login.salesforce.com/{self.id_objeto}")
        driver.find_element(By.XPATH, value='//*[@id="username"]').send_keys("usuario")
        driver.find_element(By.XPATH, value='//*[@id="password"]').send_keys("senha")
        driver.find_element(By.XPATH, value='//*[@id="Login"]').click()
        time.sleep(10)



        arquivos_diretorio = os.listdir(self.caminho_arquivos)
        codigo_input_file = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'input-file')]"))).get_property("id")
        print(f"Código input file encontrato. {codigo_input_file}")
        elemento = driver.find_element(By.XPATH, value=f'//*[@id="{codigo_input_file}"]')

        # Necessário para correção de bug salesforce
        nome_arquivo_fake = 'ignorar_wv_arquivoFN3.txt'
        caminho_completo = os.path.join(self.caminho_arquivos, nome_arquivo_fake)
        arquivo_fake = open(caminho_completo, "w")
        arquivo_fake.write("Este arquivo será excluido")
        arquivo_fake.close()

        file = pathlib.Path(self.caminho_arquivos + "ignorar_wv_arquivoFN3.txt")

        for i in range(len(arquivos_diretorio)):

            if file.exists():
                elemento.send_keys(self.caminho_arquivos + 'ignorar_wv_arquivoFN3.txt')
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div/div[3]/div/span[2]/div/button'))).click()
                os.remove(self.caminho_arquivos + 'ignorar_wv_arquivoFN3.txt')

            if (len(arquivos_diretorio)) >= 1:
                arquivo = arquivos_diretorio[i]
            print(f"Arquivos {arquivo}")
            # elemento.send_keys(self.caminho_arquivos,'ignorar.txt')
            elemento.send_keys(self.caminho_arquivos + arquivo)
            time.sleep(10)
            # nome_arquivo = driver.find_element(By.CSS_SELECTOR, 'div.slds-show_inline-block.slds-float_left.slds-p-left--x-small.slds-truncate.slds-m-right_x-small').text
            # print("NOME ARQUIVO:::{}".format(nome_arquivo))
            os.remove(self.caminho_arquivos + arquivo)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div/div[3]/div/span[2]/div/button'))).click()



test_tag = TesteTag('a0l3j00000KNPYPAA5','C:\\Users\\Thiago\\Downloads\\', 'C:\\Users\\Thiago\\Documents\\Projeto_Robo_Salesforce\\Robo_SalesForce\\chromedriver.exe')
test_tag.envia_arquivos_org_institucional()
