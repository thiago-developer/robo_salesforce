import os
import time
from os import listdir
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


class RoboSalesforce:

    # metodo contrutor que recebe por parâmetro o objeto a ser realizado envio dos anexos.
    def __init__(self, objeto, ambiente, usuario, senha):
        self._objeto = objeto
        self._ambiente = ambiente
        self._usuario = usuario
        self._senha = senha

    def abre_navegador(self):
        pass

    def _ambiente_de_acesso_workbench(self, ambiente):
        dev_homol = ambiente.upper() == "desenvolvimento".upper() or ambiente.upper() == "homologacao".upper()
        if dev_homol:
            return "Sandbox"
        if not dev_homol:
            return "Production"

    def _filtra_id_objeto(self, href):
        posicao_encontrada = href.find('=')
        id_objeto = href[posicao_encontrada + 1:]
        return id_objeto

    # metodo que realiza a query para pegar os id's a ser enviado
    def lista_ids_objeto(self):

        # options, faz com que o browser fique aberto após execução.
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        s = Service("C:\\Users\\Thiago\\Documents\\Projeto_Robo_Salesforce\\Robo_SalesForce\\chromedriver.exe")
        print("Iniciando robo...")
        driver = webdriver.Chrome(options=options, service=s)
        driver.get("https://workbench.developerforce.com/login.php")
        # configuracao sandbox
        driver.find_element(By.XPATH, value='//*[@id="oauth_env"]').send_keys(self._ambiente_de_acesso_workbench(self._ambiente))
        driver.find_element(By.XPATH, value='//*[@id="termsAccepted"]').click()
        driver.find_element(By.XPATH, value='//*[@id="loginBtn"]').click()
        driver.find_element(By.XPATH, value='//*[@id="username"]').send_keys(self._usuario)
        driver.find_element(By.XPATH, value='//*[@id="password"]').send_keys(self._senha)
        driver.find_element(By.XPATH, value='//*[@id="Login"]').click()
        driver.find_element(By.XPATH, value='//*[@id="actionJump"]').send_keys("SOQL Query")
        driver.find_element(By.XPATH, value='//*[@id="mainBlock"]/form/input[2]').click()
        driver.find_element(By.XPATH, value='//*[@id="soql_query_textarea"]').send_keys(
                                                                                        f"SELECT Id, Id_legado__c "
                                                                                        f"FROM {self._objeto} "
                                                                                        f"WHERE Id_legado__c !=null "
                                                                                        f"AND AnexoLegado__c = null "
                                                                                        f"Order By Id DESC")
        driver.find_element(By.XPATH, value='//*[@id="query_form"]/table/tbody/tr[3]/td[1]/input').click()
        time.sleep(5)
        id_institucional = self._filtra_id_objeto(driver.find_element(By.XPATH, '//*[@id="query_results"]/tbody/tr[2]/td[2]/a').get_property("href"))
        id_legado = self._filtra_id_objeto(driver.find_element(By.XPATH, '//*[@id="query_results"]/tbody/tr[2]/td[3]/a').get_property("href"))
        print(f"Id institucional: {id_institucional}, \nId IU Conecta: {id_legado}")



robo = RoboSalesforce("objeto", "ambiente", "usuario", "senha")
robo.lista_ids_objeto()
