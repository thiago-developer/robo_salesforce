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
    def __init__(self, objeto, ambiente, usuario, senha, caminho_driver):
        self._objeto = objeto
        self._ambiente = ambiente
        self._usuario = usuario
        self._senha = senha
        self._caminho_driver = caminho_driver

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
        s = Service(self._caminho_driver)
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
        try:
            driver.find_element(By.XPATH, value='//*[@id="actionJump"]').send_keys("SOQL Query")
        except:
            driver.close()
            self.lista_ids_objeto()

        driver.find_element(By.XPATH, value='//*[@id="mainBlock"]/form/input[2]').click()
        driver.find_element(By.XPATH, value='//*[@id="soql_query_textarea"]').send_keys(
                                                                                        f"SELECT Id, Id_legado__c "
                                                                                        f"FROM {self._objeto} "
                                                                                        f"WHERE Id_legado__c !=null "
                                                                                        f"AND AnexoLegado__c = null "
                                                                                        f"Order By Id DESC")
        driver.find_element(By.XPATH, value='//*[@id="query_form"]/table/tbody/tr[3]/td[1]/input').click()
        time.sleep(7)
        id_institucional = self._filtra_id_objeto(driver.find_element(By.XPATH, '//*[@id="query_results"]/tbody/tr[2]/td[2]/a').get_property("href"))
        id_legado = self._filtra_id_objeto(driver.find_element(By.XPATH, '//*[@id="query_results"]/tbody/tr[2]/td[3]/a').get_property("href"))
        print(f"Id institucional: {id_institucional} \nId IU Conecta: {id_legado}")
        self.get_anexos_org_iu_conecta(id_legado)
        driver.close()


    def get_anexos_org_iu_conecta(self, id_legado):

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        s = Service(self._caminho_driver)
        print("Iniciando robo...")
        driver = webdriver.Chrome(options=options, service=s)
        driver.get(f"https://login.salesforce.com/lightning/r/CombinedAttachment/{id_legado}/related/CombinedAttachments/view")
        driver.find_element(By.XPATH, value='//*[@id="username"]').send_keys("987302014@iuconecta.com")
        driver.find_element(By.XPATH, value='//*[@id="password"]').send_keys("Thi181907")
        driver.find_element(By.XPATH, value='//*[@id="Login"]').click()

        time.sleep(15)
        anexo = driver.find_element(By.XPATH, value="//span[contains(@class,'countSortedByFilteredBy')]").text

        quantidade_encontrada = anexo.find('itens')
        qtd_found = anexo[:quantidade_encontrada - 1]
        quantidade_de_Anexos = int(qtd_found)
        print("TIPO DE DADO: {}".format(type(quantidade_de_Anexos)))
        print("Quantidade de anexos: {}".format(quantidade_de_Anexos))

        list_ids_anexos = []

        for i in range(1, quantidade_de_Anexos+1):
            time.sleep(5)
            id_anexo = driver.find_element(By.XPATH, value=f'//*[@id="brandBand_2"]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/table/tbody/tr[{i}]/th/span/a').get_property("href")
            list_ids_anexos.append(id_anexo)
            print("Anexo posicao {}: ".format(list_ids_anexos))

        for i in range(len(list_ids_anexos)):
            driver.get(list_ids_anexos[i])
            time.sleep(10)
            driver.find_element(By.XPATH, value='//*[@id="brandBand_2"]/div/div/div/div/div[1]/div/div[1]/div/header/div[2]/div/div[2]/ul/li[1]/a').click()

        driver.close()

        self.envia_arquivos_org_institucional("a0l3j00000KNPYPAA5", "C:\\Users\\tsgldaz\\Downloads\\")


    def envia_arquivos_org_institucional(self, id_objeto, caminho_arquivos):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        s = Service(self._caminho_driver)
        print("Iniciando robo...")
        driver = webdriver.Chrome(options=options, service=s)
        driver.get(f"https://login.salesforce.com/{id_objeto}")
        driver.find_element(By.XPATH, value='//*[@id="username"]').send_keys("thiago.a.santos-gomes@institucionais.com.br")
        driver.find_element(By.XPATH, value='//*[@id="password"]').send_keys("Thi12071995")
        driver.find_element(By.XPATH, value='//*[@id="Login"]').click()
        time.sleep(10)
        arquivos_diretorio = os.listdir(caminho_arquivos)
        codigo_input_file = driver.find_element(By.XPATH, value="//*[contains(@id, 'input-file')]").get_property("id")
        print(f"Código input file encontrato. {codigo_input_file}")
        elemento = driver.find_element(By.XPATH, value=f'//*[@id="{codigo_input_file}"]')

        for i in range(len(arquivos_diretorio)):
            if(len(arquivos_diretorio)) > 1:
                arquivo = arquivos_diretorio[i]
                print(f"Arquivos {arquivo}")
                elemento_salvo = elemento.send_keys(caminho_arquivos + arquivo)
                print(elemento_salvo)
                time.sleep(10)
                os.remove(caminho_arquivos + arquivo)
                time.sleep(10)
                driver.find_element(By.XPATH, value='/html/body/div[4]/div[2]/div/div[2]/div/div[3]/div/span[2]/div/button').click()



robo = RoboSalesforce("WV_Retomada__c", "producao", "thiago.a.santos-gomes@institucionais.com.br", "Thi12071995", "C:\\Users\\Thiago\\Documents\\Projeto_Robo_Salesforce\\Robo_SalesForce\\chromedriver.exe")
robo.lista_ids_objeto()

