import os


class DeletaArquivoOculto:

    def __init__(self, caminho_arquivos):
        self.caminho_arquivos = caminho_arquivos




    def deleta_arquivos(self):

        arquivos_diretorio = os.listdir(self.caminho_arquivos)

        for i in range(len(arquivos_diretorio)):
            if (len(arquivos_diretorio)) >= 1:
                arquivo = arquivos_diretorio[i]
            print(f"Arquivos {arquivo}")
            os.remove(self.caminho_arquivos + arquivo)


deleta = DeletaArquivoOculto('C:\\Users\\Thiago\\Downloads\\')
deleta.deleta_arquivos()